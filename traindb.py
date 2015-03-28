import sqlite3
from uzbooking import CLASS_LETTERS_UK

def get_train_seats(number, departure_datetime):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
            'SELECT class1_seats,class2_seats,class3_seats FROM trains '
            'WHERE number=? AND departure_date=?',
            (number, departure_datetime))
    row = cursor.fetchone()
    result_seats = {
            'class1':row[0],
            'class2':row[1],
            'class3':row[2]}
    connection.close()
    return result_seats

def update_train_seats(number, departure_datetime, seats):
    for c in CLASS_LETTERS_UK.values():
        if c not in seats:
            seats[c] = 0

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
            'UPDATE trains SET class1_seats=?, class2_seats=?, class3_seats=?'
            'WHERE number=? AND departure_date=?',
            (seats['class1'], seats['class2'], seats['class3'],
            number, departure_datetime))
    if cursor.rowcount==0:
        cursor.execute(
                'INSERT INTO trains(number, departure_date,'
                'class1_seats, class2_seats, class3_seats)'
                'VALUES (?,?,?,?,?)',
                (number, departure_datetime, seats['class1'], seats['class2'], seats['class3']))
    connection.commit()
    connection.close()

if __name__=='__main__':
    import datetime
    number = '143K'
    departure_date = datetime.datetime(2015, 4, 12, 18, 40)
    seats = {
            'class1':10,
            'class2':20,
            'class3':30}
    update_train_seats(number, departure_date, seats)
    print(get_train_seats(number, departure_date))