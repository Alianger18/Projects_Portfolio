-- Initiating a new database called "FEDOR_WAREHOUSE"
DROP DATABASE IF EXISTS FEDOR_WAREHOUSE;
CREATE DATABASE FEDOR_WAREHOUSE;

-- Creating the Admin user
DROP USER IF EXISTS Admin;
CREATE USER Admin WITH PASSWORD 'superuser007';

-- Creating the Admin user
DROP USER IF EXISTS Admin;
CREATE USER Admin WITH PASSWORD 'superuser007';

-- Creating a new schema called "master"
DROP SCHEMA IF EXISTS master;
CREATE SCHEMA master;

-- Creating tables inside the 'master' schema
CREATE TABLE mydimdate
(
    DATE_ID      BIGSERIAL UNIQUE,
    DATE         DATE    NOT NULL,
    YEAR         INTEGER NOT NULL,
    QUARTER      INTEGER NOT NULL,
    QUARTER_NAME INTEGER NOT NULL,
    MONTH        INTEGER NOT NULL,
    MONTH_NAME   VARCHAR NOT NULL,
    DAY          INTEGER NOT NULL,
    WEEKDAY      INTEGER NOT NULL,
    WEEKDAY_NAME VARCHAR NOT NULL,
    PRIMARY KEY (DATE_ID)
);

CREATE TABLE mydimaddress
(
    ADDRESS_ID BIGSERIAL UNIQUE,
    ZIP_CODE   VARCHAR NOT NULL,
    STREET     VARCHAR NOT NULL,
    CITY       VARCHAR NOT NULL,
    COUNTRY    VARCHAR NOT NULL,
    LATITUDE   NUMERIC NOT NULL,
    LONGITUDE  NUMERIC NOT NULL,
    PRIMARY KEY (ADDRESS_ID)
);

CREATE TABLE mydimcustomer
(
    CUSTOMER_ID         BIGSERIAL UNIQUE,
    CUSTOMER_FIRST_NAME VARCHAR NOT NULL,
    CUSTOMER_LAST_NAME  VARCHAR NOT NULL,
    CUSTOMER_MAIL       VARCHAR NOT NULL,
    PRIMARY KEY (CUSTOMER_ID)
);

CREATE TABLE mydimproduct
(
    PRODUCT_ID  BIGSERIAL UNIQUE,
    DESCRIPTION VARCHAR NOT NULL,
    UNIT_PRICE  MONEY   NOT NULL,
    PRIMARY KEY (PRODUCT_ID)
);

CREATE TABLE mydiminvoice
(
    INVOICE_ID     BIGSERIAL UNIQUE,
    INVOICE_AMOUNT MONEY NOT NULL,
    PRIMARY KEY (INVOICE_ID)
);

CREATE TABLE myfacttransaction
(
    TRANSACTION_ID     BIGSERIAL UNIQUE,
    PRODUCT_AMOUNT     INTEGER   NOT NULL,
    TRANSACTION_AMOUNT MONEY     NOT NULL,
    DATE_ID            BIGSERIAL NOT NULL,
    PRODUCT_ID         BIGSERIAL NOT NULL,
    ADDRESS_ID         BIGSERIAL NOT NULL,
    INVOICE_ID         BIGSERIAL NOT NULL,
    CUSTOMER_ID        BIGSERIAL NOT NULL,
    PRIMARY KEY (TRANSACTION_ID),
    FOREIGN KEY (DATE_ID) REFERENCES mydimdate,
    FOREIGN KEY (ADDRESS_ID) REFERENCES mydimaddress,
    FOREIGN KEY (PRODUCT_ID) REFERENCES mydimproduct,
    FOREIGN KEY (INVOICE_ID) REFERENCES mydiminvoice,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES mydimcustomer
);
