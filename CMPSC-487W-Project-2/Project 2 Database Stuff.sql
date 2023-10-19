CREATE DATABASE websystem;

CREATE TABLE items(
    ID int NOT NULL AUTO_INCREMENT,
    name varchar(30) NOT NULL,
    description varchar(255),
    image varchar(50),
    PRIMARY KEY (ID)
);