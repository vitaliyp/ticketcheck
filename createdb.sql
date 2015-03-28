CREATE TABLE trains (
    number TEXT NOT NULL,
    departure_date TEXT NOT NULL,
    class1_seats INTEGER NOT NULL DEFAULT 0,
    class2_seats INTEGER NOT NULL DEFAULT 0,
    class3_seats INTEGER NOT NULL DEFAULT 0,
    updated_on TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (number, departure_date)
);

CREATE TRIGGER update_time AFTER UPDATE ON trains FOR EACH ROW
BEGIN
    UPDATE trains SET updated_on=datetime('now') 
        WHERE number=NEW.number AND departure_date=NEW.departure_date;
END;

