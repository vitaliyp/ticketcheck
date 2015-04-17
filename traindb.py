import sqlite3
from uzbooking import CLASS_LETTERS_UK

def get_seats(number, dep_station, dep_datetime, dest_station):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT class1_seats,class2_seats,class3_seats,class4_seats,class5_seats,class6_seats FROM rides WHERE number=? AND dep_station=? AND dep_datetime=? AND dest_station=?',(number, dep_station, dep_datetime, dest_station))
            
    row = cursor.fetchone()
    if not row:
        row = (0,0,0,0,0,0)
    result_seats = {
            1:row[0],
            2:row[1],
            3:row[2],
            4:row[3],
            5:row[4],
            6:row[5]}
    connection.close()
    return result_seats

def update_seats(number, dep_station, dep_datetime, dest_station, seats):
    for c in CLASS_LETTERS_UK.values():
        if c not in seats:
            seats[c] = 0

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
            'UPDATE rides SET class1_seats=?,class2_seats=?,class3_seats=?,class4_seats=?,class5_seats=?,class6_seats=? WHERE number=? AND dep_station=? AND dep_datetime=? AND dest_station=?', (seats[1], seats[2], seats[3], seats[4], seats[5], seats[6], number, dep_station, dep_datetime, dest_station))
    if cursor.rowcount==0:
        cursor.execute(
                'INSERT INTO rides(number, dep_station, dep_datetime, dest_station,'
                'class1_seats, class2_seats, class3_seats, class4_seats, class5_seats, class6_seats)'
                'VALUES (?,?,?,?,?,?,?,?,?,?)',
                (number, dep_station, dep_datetime, dest_station, seats[1], seats[2], seats[3], seats[4], seats[5], seats[6]))
    connection.commit()
    connection.close()

def clear_rides():
    with sqlite3.connect('db.sqlite3') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM rides')
        connection.commit()

if __name__=='__main__':
    pass
