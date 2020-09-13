create database helper DEFAULT CHARACTER SET utf8mb4;
use helper;

DROP TABLE IF EXISTS ANSWER_LANGUAGE;
DROP TABLE IF EXISTS QUESTION_LANGUAGE;
DROP TABLE IF EXISTS PENDINGQUESTION_LANGUAGE;
DROP TABLE IF EXISTS QUESTION;
DROP TABLE IF EXISTS PENDING_QUESTION;
DROP TABLE IF EXISTS ANSWER;
DROP TABLE IF EXISTS TOPIC;
DROP TABLE IF EXISTS LANGUAGE;

CREATE TABLE LANGUAGE
(
    Id   INTEGER,
    Name VARCHAR(30),
    Primary Key (Id),
    Unique (Name)
);

CREATE TABLE TOPIC
(
    Id           INTEGER auto_increment,
    Description  TEXT     NOT NULL,
    CreationDate DATETIME NOT NULL,
    Primary Key (Id)
);

CREATE TABLE ANSWER
(
    Id         INTEGER,
    AnswerDate DATETIME NOT NULL,
    Status     VARCHAR(20),
    Primary Key (Id)
);
CREATE TABLE PENDING_QUESTION
(
    Id           INTEGER auto_increment,
    CreationDate DATETIME NOT NULL,
    Status       VARCHAR(20),
    GroupNo      INTEGER  NULL,
    Primary Key (Id)
);
CREATE TABLE QUESTION
(
    Id                INTEGER auto_increment,
    CreationDate      DATETIME NOT NULL,
    Status            VARCHAR(20),
    TopicId           INTEGER  NULL,
    AnswerId          INTEGER  NULL,
    PendingQuestionId INTEGER  NULL,
    Primary Key (Id),
    Foreign Key (TopicId) REFERENCES TOPIC (Id),
    Foreign Key (AnswerId) REFERENCES ANSWER (Id),
    Foreign key (PendingQuestionId) REFERENCES PENDING_QUESTION (Id)
);

CREATE TABLE PENDINGQUESTION_LANGUAGE
(
    PendingQuestionId INTEGER,
    LanguageId        INTEGER,
    Primary Key (PendingQuestionId, LanguageId),
    Foreign Key (PendingQuestionId) REFERENCES PENDING_QUESTION (Id),
    Foreign Key (LanguageId) REFERENCES LANGUAGE (Id)
);

CREATE TABLE QUESTION_LANGUAGE
(
    QuestionId INTEGER,
    LanguageId INTEGER,
    Primary Key (QuestionId, LanguageId),
    Foreign Key (QuestionId) REFERENCES QUESTION (Id),
    Foreign Key (LanguageId) REFERENCES LANGUAGE (Id)
);

CREATE TABLE ANSWER_LANGUAGE
(
    AnswerId   INTEGER,
    LanguageId INTEGER,
    Primary Key (AnswerId, LanguageId),
    Foreign Key (AnswerId) REFERENCES ANSWER (Id),
    Foreign Key (LanguageId) REFERENCES LANGUAGE (Id)
);