create database q_test;
use q_test;

create table parking(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parkingAddress  VARCHAR(100) NOT NULL,
    parkingName  VARCHAR(100) NOT NULL,
    parkingCoordinates  VARCHAR(100) NOT NULL,
    parkingRadious INT NOT NULL,
    capacity INT NOT NULL
);

insert into parking(parkingAddress,parkingName,parkingCoordinates,parkingRadious) values ("ramon corona 223","banco","344536363,335363634",50);

create table registroRAW(
   frame_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   frame_path VARCHAR(100) NOT NULL,
   frame_coordinates VARCHAR(40) NOT NULL,
   creation_date DATETIME,
   parking_id INT NOT NULL,
   INDEX(parking_id),
   FOREIGN KEY (parking_id)
        REFERENCES parking(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

insert into registroRAW(frame_path,frame_coordinates,creation_date,parking_id) values ("path/to/file/file.jpg","45,56,23,66","2019-05-19T16:08:51.809449",1);


create table status_parking(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    occupation INT NOT NULL,
    parking_id INT NOT NULL,
    free_spaces INT NOT NULL,
   INDEX(parking_id),
   FOREIGN KEY (parking_id)
        REFERENCES parking(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

insert into status_parking(occupation,parking_id,free_spaces) values (0,1,35);
UPDATE status_parking set occupation = 1,free_spaces = 34 where parking_id = 1


create table registros(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plate VARCHAR(30) NOT NULL,
    frame_path VARCHAR(100) NOT NULL,
    creation_date DATETIME,
    direction VARCHAR(10) NOT NULL,
    parking_id INT NOT NULL,
    INDEX(parking_id),
    FOREIGN KEY (parking_id)
        REFERENCES parking(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION

);

DELIMITER //

CREATE TRIGGER status_after_registro
AFTER INSERT
   ON registros FOR EACH ROW

BEGIN
-- Insert record into audit 
    IF NEW.direction = "in" THEN
    UPDATE status_parking set free_spaces = free_spaces - 1 where parking_id = NEW.parking_id;
    UPDATE status_parking set occupation = occupation + 1 where parking_id = NEW.parking_id;
    ELSE 
    UPDATE status_parking set free_spaces = free_spaces + 1 where parking_id = NEW.parking_id;
    UPDATE status_parking set occupation = occupation - 1 where parking_id = NEW.parking_id;
     END IF;
END; //

DELIMITER ;

insert into registros(
    plate,
    frame_path,
    creation_date,
    direction,
    parking_id
    )
     values 
    ("JKW5528",
    "img.jpg",
    "2019-05-19T16:08:51.809449",
    "in",
    1);

insert into registros(
    plate,
    frame_path,
    creation_date,
    direction,
    parking_id
    )
     values 
    ("JKW5528",
    "img.jpg",
    "2019-05-19T16:08:51.809449",
    "out",
    1);


