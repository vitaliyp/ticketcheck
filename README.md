# ticketcheck
Script that monitors Ukrainian Railroad (Укрзалізниця) booking site (http://booking.uz.gov.ua)
and sends email notification when desired tickets are available.

## Configuration
File `settints.json` contains application settings:
```json
{
  "email":{
    "server":"smtp.example.org:port",
    "username":"username@example.org",
    "password":"secretpassword"
  }
}
```

File `monitors.json` contains a list of objects. Each object specifies departure station,
departure date, and destination station. Every time the script is executed, it iterates over
all of this objects and checks if tickets with specified parameters have became available.
```json
[{
  "departure_date":"2015.4.2",
  "departure_station":"Київ",
  "destination_station":"Івано-Франківськ",
  "classes":[3],
  "email":"user@example.org"
}]
```
`classes` field is a list and specifies seats classes which should be monitored
i.e. `1` represents the first class.
`email` in an address which is used to send notifications.

In order to run script, proper sqlite3 database should be created:
```
$ sqlite3 db.sqlite3 < createdb.sql
```

## Running script
```
$ python3 ticketcheck.py
```
