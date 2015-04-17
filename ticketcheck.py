import uzbooking
import traindb
import json
import logging
import datetime
import mailcomposer

def parse_monitor_config(filename):
    with open(filename, 'r', encoding='utf8') as f:
        raw_monitors = json.loads(f.read())

    monitors = []
    for raw_monitor in raw_monitors:
        monitor = {}

        try:
            monitor['departure_date'] = datetime.datetime.strptime(
                    raw_monitor['departure_date'],'%Y.%m.%d')
        except ValueError:
            logging.error('Invalid departure date')
            continue

        departure_station_id = uzbooking.get_station_id(raw_monitor['departure_station'])
        if not departure_station_id:
            logging.error('Wrong departure station')
            continue
        monitor['departure_station_id'] = departure_station_id
        monitor['departure_station_name'] = raw_monitor['departure_station']

        destination_station_id = uzbooking.get_station_id(raw_monitor['destination_station'])
        if not destination_station_id:
            logging.error('Wrong destination station')
            continue
        monitor['destination_station_id'] = destination_station_id
        monitor['destination_station_name'] = raw_monitor['destination_station']

        try:
            classes = raw_monitor['classes']
        except KeyError:
            logging.info('No classes specified. Monitoring all.')
            classes = [1,2,3]
        monitor['classes'] = classes

        try:
            monitor['email'] = raw_monitor['email']
        except KeyError:
            logging.error('No email address specified.')
            continue
        
        monitors.append(monitor)

    return monitors

def parse_settings(filename):
    with open(filename, 'r', encoding='utf8') as f:
        settings = json.loads(f.read())
    return settings

rides_to_update = []

def check_for_new_tickets(monitor):
    global rides_to_update

    trains = uzbooking.get_trains(
            departure_date = monitor['departure_date'],
            departure_station_id = monitor['departure_station_id'],
            destination_station_id = monitor['destination_station_id'])
    
    trains_with_new_tickets = []
    for train in trains:
        # Check tis train in db
        seats_in_db = traindb.get_seats(
                train['number'],
                monitor['departure_station_name'],
                train['departure_datetime'],
                monitor['destination_station_name'])
        for c in monitor['classes']:
            if seats_in_db[c] ==0 and train['seats'][c]>0:
                trains_with_new_tickets.append(train)
                break
        # add ride to update queue
        rides_to_update.append((train,monitor))
    return trains_with_new_tickets


if __name__=='__main__':
    logging.basicConfig(filename='ticketcheck.log', level=logging.INFO)
    logging.info("Script started")

    monitors = parse_monitor_config('monitors.json')
    settings = parse_settings('settings.json')

    for monitor in monitors:
        trains = check_for_new_tickets(monitor)
        logging.info('Found %s trains'%len(trains))
        if trains:
            composer = mailcomposer.MailComposer(recipient=monitor['email'],**settings['email'])
            composer.add_trains(monitor, trains)
            composer.send_mail()        

    # update_rides
    traindb.clear_rides()
    for train, monitor in rides_to_update:
        traindb.update_seats(
                train['number'],
                monitor['departure_station_name'],
                train['departure_datetime'],
                monitor['destination_station_name'],
                train['seats'])
