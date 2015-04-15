CREATE TABLE rides (
    number TEXT NOT NULL,
    dep_datetime TEXT NOT NULL,
    dep_station INTEGER NOT NULL,
    dest_station INTEGER NOT NULL,
    class1_seats INTEGER NOT NULL DEFAULT 0,
    class2_seats INTEGER NOT NULL DEFAULT 0,
    class3_seats INTEGER NOT NULL DEFAULT 0,
    class4_seats INTEGER NOT NULL DEFAULT 0,
    class5_seats INTEGER NOT NULL DEFAULT 0,
    class6_seats INTEGER NOT NULL DEFAULT 0,
    updated_on TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_time AFTER UPDATE ON rides FOR EACH ROW
BEGIN
    UPDATE rides SET updated_on=datetime('now') 
        WHERE number=NEW.number AND dep_datetime=NEW.dep_datetime;
END;

