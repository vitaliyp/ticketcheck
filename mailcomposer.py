import smtplib
from email.mime.text import MIMEText
from uzbooking import CLASS_LETTERS_UK

classes = {v:k for k, v in CLASS_LETTERS_UK.items()}

class MailComposer:
    serverHostname = 'mail.hpcc.kpi.ua:587'
    username = 'dmytro.timofeev@hpcc.kpi.ua'
    password = ''
    recipients = []
    
    def __init__(self, server, username, password, recipient):
        self._trains = [] 
        self._server = server
        self._username = username
        self._password = password
        self._recipient = recipient

    def add_trains(self, monitor, trains):
        self._trains.append((monitor, trains))
    
    def _compose_message_body(self):
        strlist = []
        datetime_format = '%Y.%m.%d %H:%M'
        for monitor, trains in self._trains:
            strlist.append("%s %s -> %s\n"%(
                monitor['departure_date'].strftime('%Y.%m.%d'),
                monitor['departure_station_name'],
                monitor['destination_station_name'])) 
            for train in trains:
                strlist.append('\t%s %s - %s\n'%(
                    train['number'],
                    train['departure_station_name'],
                    train['destination_station_name']))
                strlist.append('\t\tDeparture: %s | Arrival: %s\n'%(
                    train['departure_datetime'].strftime(datetime_format),
                    train['arrival_datetime'].strftime(datetime_format)))
                strlist.append('\t\t%s:%s %s:%s %s:%s\n'%(
                    classes[1],train['seats'][1],
                    classes[2],train['seats'][2],
                    classes[3],train['seats'][3]))

        return ''.join(strlist)
    
    def send_mail(self):
        msg_body = self._compose_message_body()
        
        msg = MIMEText(msg_body)
        msg['From'] = self._username
        msg['To'] = self._recipient
        msg['Subject'] = 'Railroad tickets available'
        
        server = smtplib.SMTP(self._server)
        server.starttls()
        server.login(self._username, self._password)
        server.sendmail(self._username, self._recipient, msg.as_string())
        server.quit()

if __name__=='__main__':
    pass

