create database helper;
use helper;

DROP TABLE IF EXISTS ANSWER;
DROP TABLE IF EXISTS QUESTION;
DROP TABLE IF EXISTS TOPIC;


CREATE TABLE TOPIC
(
    Id           INTEGER auto_increment,
    Description  TEXT     NOT NULL,
    CreationDate DATETIME NOT NULL,
    PRIMARY KEY (Id)
);


CREATE TABLE QUESTION
(
    Id           INTEGER auto_increment,
    Description  TEXT     NOT NULL,
    CreationDate DATETIME NOT NULL,
    TopicId      INTEGER  NULL,
    Primary Key (Id),
    Foreign Key (TopicId) REFERENCES TOPIC (Id)
);

CREATE TABLE ANSWER
(
    QuestionId  INTEGER,
    Description TEXT     NOT NULL,
    AnswerDate  DATETIME NOT NULL,
    Primary Key (QuestionId),
