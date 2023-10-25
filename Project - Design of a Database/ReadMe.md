# Airbnb Database Simulation
This project is a database simulation of the popular vacation rental platform,
Airbnb, using the PostgreSQL database management system on DataGrip IDE by 
JetBrains. The purpose of this simulation is to provide a way to analyze and 
query Airbnb's data, as well as to explore the relationships between different 
aspects of the platform.

## Getting Started

### Requirements
To use this database simulation, you will need to have a PostgreSQL server 
installed on your machine. You can download and install PostgreSQL from the 
official website: https://www.postgresql.org/download/.

### Recommendation
The use of DataGrip is totally optional yet it turns up to be one of the 
best if not the best IDE for databases and it's free for students. You can 
download and install DataGrip from the official website: 
https://www.jetbrains.com/datagrip/download.

Once you have PostgreSQL installed, you will need to create a new database 
in which to run the simulation. You can do this by running the following 
command in your PostgreSQL terminal:

## Creating the database

The first step will be to specify the users, that will be using our database :

```shell 
-- Creating Users
DROP USER IF EXISTS superuser;
CREATE USER superuser WITH PASSWORD 'superuser007';

DROP USER IF EXISTS guest;
CREATE USER guest WITH PASSWORD 'guest321';

DROP USER IF EXISTS host;
CREATE USER host WITH PASSWORD 'host123';
```

Then, we'll head on to create the database :
```shell
-- Initiating a new database called "AIRBNB"
DROP DATABASE IF EXISTS AIRBNB;
```


After getting done creating users, we'll create a schema, name it "Main" and 
create the tables of our database :

```shell
-- Creating a new schema called "Main"
CREATE SCHEMA MAIN

    CREATE TABLE HOSTS
    (
        HOST_ID      SERIAL  NOT NULL UNIQUE, -- Unique identifier for every host.
        FIRST_NAME   VARCHAR NOT NULL,        -- The first name of the host.
        LAST_NAME    VARCHAR NOT NULL,        -- The last name of the host.
        EMAIL        VARCHAR NOT NULL,        -- The email of the host.
        PHONE_NUMBER VARCHAR NOT NULL,        -- The phone number of the host.
        HOST_TYPE    VARCHAR NOT NULL,        -- It can either be a particular or professional host.
        HOST_STATUS  VARCHAR NOT NULL,        -- It can be regular, super or plus host.
        PRIMARY KEY (HOST_ID)
    )

    CREATE TABLE GUESTS
    (
        GUEST_ID          SERIAL  NOT NULL UNIQUE, -- Unique identifier for every guest.
        FIRST_NAME        VARCHAR NOT NULL,        -- The first name of the guest.
        LAST_NAME         VARCHAR NOT NULL,        -- The last name of the guest.
        EMAIL             VARCHAR NOT NULL,        -- The email of the guest.
        PHONE_NUMBER      VARCHAR NOT NULL,        -- The phone number of the guest.
        FACEBOOK_ACCOUNT  VARCHAR,                 -- Link to the facebook account of the guest, could be left empty.
        GOOGLE_ACCOUNT    VARCHAR,                 -- Link to the google account of the guest, could be left empty.
        INSTAGRAM_ACCOUNT VARCHAR,                 -- Link to the instagram account of the guest, could be left empty.
        PRIMARY KEY (GUEST_ID)
    )

    CREATE TABLE HOSTS_LANGUAGES
    (
        ID              SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        FIRST_LANGUAGE  VARCHAR  NOT NULL,        -- The main language spoken by the host.
        SECOND_LANGUAGE VARCHAR,                  -- Secondary language spoken by the host, could be left empty.
        THIRD_LANGUAGE  VARCHAR,                  -- Secondary language spoken by the host, could be left empty.
        FOURTH_LANGUAGE VARCHAR,                  -- Secondary language spoken by the host, could be left empty.
        FIFTH_LANGUAGE  VARCHAR,                  -- Secondary language spoken by the host, could be left empty.
        HOST_ID         SMALLINT NOT NULL,        -- Identifier referring to the host.
        PRIMARY KEY (ID),
        FOREIGN KEY (HOST_ID)
            REFERENCES HOSTS (HOST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE HOSTS_REVIEWS
    (
        HOST_REVIEW_ID SERIAL    NOT NULL UNIQUE, -- Unique identifier of a host's review.
        RANKING        SMALLINT  NOT NULL,        -- On a scale 1 to 10, 1 stands for poor and 10 for extraordinary.
        REVIEW         TEXT      NOT NULL,        -- The host's thoughts about the guest.
        REVIEW_DATE    TIMESTAMP NOT NULL,        -- The date, when the review was submitted.
        HOST_ID        SMALLINT  NOT NULL,        -- Identifier referring to the booking.
        PRIMARY KEY (HOST_REVIEW_ID),
        FOREIGN KEY (HOST_ID)
            REFERENCES HOSTS (HOST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE GUESTS_REVIEWS
    (
        GUEST_REVIEW_ID SERIAL    NOT NULL UNIQUE, -- Unique identifier of a guest's review.
        RANKING         SMALLINT  NOT NULL,        -- On a scale 1 to 10, 1 stands for poor and 10 for extraordinary.
        REVIEW          TEXT      NOT NULL,        -- The guest's thoughts about the stay
        REVIEW_DATE     TIMESTAMP NOT NULL,        -- The date, when the review was submitted.
        GUEST_ID        SMALLINT  NOT NULL,        -- Identifier referring to the guest.
        PRIMARY KEY (GUEST_REVIEW_ID),
        FOREIGN KEY (GUEST_ID)
            REFERENCES GUESTS (GUEST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE ADMINS
    (
        ADMIN_ID   SERIAL  NOT NULL UNIQUE, -- Unique identifier for an administrator.
        FIRST_NAME VARCHAR NOT NULL,        -- The first name of the administrator.
        LAST_NAME  VARCHAR NOT NULL,        -- The last name of the administrator.
        EMAIL      VARCHAR NOT NULL,        -- The email of the administrator.
        PRIMARY KEY (ADMIN_ID)
    )

    CREATE TABLE HOSTS_SUPPORT_REQUESTS
    (
        HOST_REQUEST_ID SERIAL   NOT NULL UNIQUE,-- Unique identifier of a support request made by hosts.
        REQUEST_OBJECT  VARCHAR  NOT NULL,       -- The object of the request.
        DESCRIPTION     TEXT     NOT NULL,       -- Full description of the request.
        HOST_ID         SMALLINT NOT NULL,       -- Identifier referring to the host.
        ADMIN_ID        SMALLINT NOT NULL,       -- Identifier referring to the administrator received the request.
        PRIMARY KEY (HOST_REQUEST_ID),
        FOREIGN KEY (HOST_ID)
            REFERENCES HOSTS (HOST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ADMIN_ID)
            REFERENCES ADMINS (ADMIN_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE GUESTS_SUPPORT_REQUESTS
    (
        GUEST_REQUEST_ID SERIAL   NOT NULL UNIQUE, -- Unique identifier of a support request made by guests.
        REQUEST_OBJECT   VARCHAR  NOT NULL,        -- The object of the request.
        DESCRIPTION      TEXT     NOT NULL,        -- Full description of the request.
        GUEST_ID         SMALLINT NOT NULL,        -- Identifier referring to the guest.
        ADMIN_ID         SMALLINT NOT NULL,        -- Identifier referring to the administrator handling the request.
        PRIMARY KEY (GUEST_REQUEST_ID),
        FOREIGN KEY (GUEST_ID)
            REFERENCES GUESTS (GUEST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ADMIN_ID)
            REFERENCES ADMINS (ADMIN_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE CONVERSATIONS
    (
        CONVERSATION_ID SERIAL   NOT NULL UNIQUE, -- Unique identifier of a conversation.
        GUEST_ID        SMALLINT NOT NULL,        -- Identifier referring to the guest.
        HOST_ID         SMALLINT NOT NULL,        -- Identifier referring to the host.
        PRIMARY KEY (CONVERSATION_ID),
        FOREIGN KEY (GUEST_ID)
            REFERENCES GUESTS (GUEST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (HOST_ID)
            REFERENCES HOSTS (HOST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE HOSTS_MAILBOX
    (
        HOST_MESSAGE_ID   SERIAL    NOT NULL UNIQUE, -- Unique identifier of a message.
        MESSAGE_CORP      TEXT      NOT NULL,        -- The message responding to a potential guest.
        MESSAGE_TIMESTAMP TIMESTAMP NOT NULL,        -- The timestamp of the message.
        CONVERSATION_ID   SMALLINT  NOT NULL,        -- Identifier referring to the conversation.
        PRIMARY KEY (HOST_MESSAGE_ID),
        FOREIGN KEY (CONVERSATION_ID)
            REFERENCES CONVERSATIONS (CONVERSATION_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE GUESTS_MAILBOX
    (
        GUEST_MESSAGE_ID  SERIAL    NOT NULL UNIQUE, -- Unique identifier of a message.
        MESSAGE_CORP      TEXT      NOT NULL,        -- The message of a potential guest.
        MESSAGE_TIMESTAMP TIMESTAMP NOT NULL,        -- The timestamp of the message.
        CONVERSATION_ID   SMALLINT  NOT NULL,        -- Identifier referring to the conversation.
        PRIMARY KEY (GUEST_MESSAGE_ID),
        FOREIGN KEY (CONVERSATION_ID)
            REFERENCES CONVERSATIONS (CONVERSATION_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE CITIES
    (
        CITY_ID   SERIAL  NOT NULL UNIQUE, -- Unique identifier of every city.
        CITY      VARCHAR NOT NULL,        -- Name of the city.
        COUNTRY   VARCHAR NOT NULL,        -- The country where the city is located.
        CONTINENT VARCHAR NOT NULL,        -- The continent where the city is located.
        PRIMARY KEY (CITY_ID)
    )

    CREATE TABLE ADDRESSES
    (
        ADDRESS_ID   SERIAL   NOT NULL UNIQUE, -- Unique identifier for every address.
        ADDRESS_LINE VARCHAR  NOT NULL,        -- Contains the number and street where the property is located.
        ZIP_CODE     VARCHAR  NOT NULL,        -- Zip code of the property.
        CITY_ID      SMALLINT NOT NULL,        -- Identifier referring to the city where the property is located.
        PRIMARY KEY (ADDRESS_ID),
        FOREIGN KEY (CITY_ID)
            REFERENCES CITIES (CITY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTIES
    (
        PROPERTY_ID   SERIAL   NOT NULL UNIQUE, -- Unique identifier for every property.
        PROPERTY_NAME VARCHAR  NOT NULL,        -- The name of the property.
        PROPERTY_TYPE VARCHAR  NOT NULL,        -- The type of the property, like a house, apartment or hotel.
        RENTED_PLACE  VARCHAR  NOT NULL,        -- It could be the entire place or just a private room.
        ADDRESS_ID    SMALLINT NOT NULL,        -- Identifier referring to the address where the property is located.
        HOST_ID       SMALLINT NOT NULL,        -- Identifier referring to the host owning the property.
        PRIMARY KEY (PROPERTY_ID),
        FOREIGN KEY (ADDRESS_ID)
            REFERENCES ADDRESSES (ADDRESS_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (HOST_ID)
            REFERENCES HOSTS (HOST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE BEDS_AND_ROOMS
    (
        ID                  SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        NUMBER_OF_BEDS      SMALLINT NOT NULL,        -- Number of beds in the property.
        NUMBER_OF_BEDROOMS  SMALLINT NOT NULL,        -- Number of bedrooms in the property.
        NUMBER_OF_BATHROOMS SMALLINT NOT NULL,        -- Number of bathrooms in the property.
        PROPERTY_ID         SMALLINT NOT NULL,        -- Identifier referring to the property.
        PRIMARY KEY (ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTIES_CAPACITIES
    (
        CAPACITY_ID SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        ADULTS      SMALLINT NOT NULL,        -- Number of adults that could be accommodated.
        CHILDREN    SMALLINT DEFAULT 0,       -- Number of children that could be accommodated.
        INFANTS     SMALLINT DEFAULT 0,       -- Number of infants that could be accommodated.
        PETS        SMALLINT DEFAULT 0,       -- Number of pets that could be accommodated.
        PROPERTY_ID SMALLINT NOT NULL,        -- Identifier referring to the property.
        PRIMARY KEY (CAPACITY_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTIES_ESSENTIALS
    (
        ESSENTIAL_ID        SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        WIFI                BOOLEAN DEFAULT FALSE,    -- True if the property includes wifi, otherwise, False.
        WASHER              BOOLEAN DEFAULT FALSE,    -- True if the property includes a washer, otherwise, False.
        AIR_CONDITIONING    BOOLEAN DEFAULT FALSE,    -- True if the property includes an air conditioner, otherwise, False.
        DEDICATED_WORKPLACE BOOLEAN DEFAULT FALSE,    -- True if the property includes a dedicated workplace, otherwise, False.
        IRON                BOOLEAN DEFAULT FALSE,    -- True if the property includes this option, otherwise, False.
        KITCHEN             BOOLEAN DEFAULT FALSE,    -- True if the property includes a kitchen, otherwise, False.
        TV                  BOOLEAN DEFAULT FALSE,    -- True if the property includes a TV, otherwise, False.
        DRYER               BOOLEAN DEFAULT FALSE,    -- True if the property includes a dryer, otherwise, False.
        HEATING             BOOLEAN DEFAULT FALSE,    -- True if the property includes heating, otherwise, False.
        PROPERTY_ID         SMALLINT NOT NULL,        -- Identifier referring to the property.
        PRIMARY KEY (ESSENTIAL_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTIES_FEATURES
    (
        FEATURE_ID       SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        GYM              BOOLEAN DEFAULT FALSE,    -- True if the property includes a gym access on premises, otherwise, False.
        POOL             BOOLEAN DEFAULT FALSE,    -- True if the property includes a pool access on premises, otherwise, False.
        PARKING          BOOLEAN DEFAULT FALSE,    -- True if the property includes a parking on premises, otherwise, False.
        BREAKFAST        BOOLEAN DEFAULT FALSE,    -- True if the property offers a breakfast, otherwise, False.
        INDOOR_FIREPLACE BOOLEAN DEFAULT FALSE,    -- True if the property includes an indoor fireplace, otherwise, False.
        PETS_ALLOWED     BOOLEAN DEFAULT FALSE,    -- True if the pets are allowed in the property, otherwise, False.
        SMOKING_ALLOWED  BOOLEAN DEFAULT FALSE,    -- True if smoking is allowed in the property, otherwise, False.
        PROPERTY_ID      SMALLINT NOT NULL,        -- Identifier referring to the property.
        PRIMARY KEY (FEATURE_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTIES_FEES
    (
        FEES_ID       SERIAL   NOT NULL UNIQUE, -- Unique identifier for every specification.
        STAY_FEES     DECIMAL  NOT NULL,        -- The fees for a one night stay.
        CLEANING_FEES DECIMAL  NOT NULL,        -- The fees for cleaning services.
        SERVICE_FEES  DECIMAL  NOT NULL,        -- The fees for the service provided.
        PROPERTY_ID   SMALLINT NOT NULL,        -- Identifier referring to the property.
        PRIMARY KEY (FEES_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PROPERTY_IMAGES
    (
        IMAGE_ID    SERIAL   NOT NULL UNIQUE, -- A unique identifier for each image
        IMAGE_LINK  VARCHAR  NOT NULL,        -- A link to the image located in servers
        PROPERTY_ID SMALLINT NOT NULL,        -- Identifier referring to the property
        PRIMARY KEY (IMAGE_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE RESERVATIONS
    (
        RESERVATION_ID SERIAL   NOT NULL UNIQUE, -- Unique identifier of a reservation.
        CHECK_IN       DATE     NOT NULL,        -- The date, when the guest arrives to the property.
        CHECK_OUT      DATE     NOT NULL,        -- The date, when the guest leaves the property.
        CONFIRMED      BOOLEAN DEFAULT FALSE,    -- True if the guest finds the accommodation as described, otherwise, False.
        PROPERTY_ID    SMALLINT NOT NULL,        -- Identifier referring to the property.
        GUEST_ID       SMALLINT NOT NULL,        -- Identifier referring to the guest.
        PRIMARY KEY (RESERVATION_ID),
        FOREIGN KEY (PROPERTY_ID)
            REFERENCES PROPERTIES (PROPERTY_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (GUEST_ID)
            REFERENCES GUESTS (GUEST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        CHECK (CHECK_IN < CHECK_OUT)
    )

    CREATE TABLE BOOKINGS_CONFIRMATION
    (
        BOOKING_ID     SERIAL   NOT NULL UNIQUE, -- Unique identifier of a booking.
        RESERVATION_ID SMALLINT NOT NULL,        -- Identifier referring to the reservation.
        PRIMARY KEY (BOOKING_ID),
        FOREIGN KEY (RESERVATION_ID)
            REFERENCES RESERVATIONS (RESERVATION_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE PLATFORM_REVENUE
    (
        REVENUE_ID        SERIAL   NOT NULL UNIQUE, -- Unique identifier for every revenue.
        FROM_HOST         DECIMAL  NOT NULL,        -- The fees paid from the host for the service.
        FROM_GUEST        DECIMAL  NOT NULL,        -- The fees paid from the guest for the service.
        TOTAL_PER_BOOKING DECIMAL  NOT NULL,        -- The total fees paid to the service per booking.
        BOOKING_ID        SMALLINT NOT NULL,        -- Identifier referring to the booking.
        PRIMARY KEY (REVENUE_ID),
        FOREIGN KEY (BOOKING_ID)
            REFERENCES BOOKINGS_CONFIRMATION (BOOKING_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE HOSTS_PAYOUT
    (
        PAYOUT_ID  SERIAL   NOT NULL UNIQUE, -- Unique identifier for every payout.
        PAYOUT     DECIMAL  NOT NULL,        -- The fees paid from the guest for the stay, the service fees is deducted from the platform.
        BOOKING_ID SMALLINT NOT NULL,        -- Identifier referring to the booking.
        PRIMARY KEY (PAYOUT_ID),
        FOREIGN KEY (BOOKING_ID)
            REFERENCES BOOKINGS_CONFIRMATION (BOOKING_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE GUESTS_PAYMENTS
    (
        PAYMENT_ID SERIAL   NOT NULL UNIQUE, -- Unique identifier for every payment.
        TOTAL_PAY  DECIMAL  NOT NULL,        -- The total fees, the guest has to pay for the whole stay.
        BOOKING_ID SMALLINT NOT NULL,        -- Identifier referring to the booking.
        PRIMARY KEY (PAYMENT_ID),
        FOREIGN KEY (BOOKING_ID)
            REFERENCES BOOKINGS_CONFIRMATION (BOOKING_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    )

    CREATE TABLE BOOKINGS_HISTORY
    (
        ARCHIVE_ID      SERIAL   NOT NULL UNIQUE, -- Unique identifier for every past booking.
        GUEST_REVIEW_ID SMALLINT NOT NULL,        -- Identifier referring to a guest's review.
        HOST_REVIEW_ID  SMALLINT NOT NULL,        -- Identifier referring to a host's review.
        BOOKING_ID      SMALLINT NOT NULL,        -- Identifier referring to the booking.
        PRIMARY KEY (ARCHIVE_ID),
        FOREIGN KEY (GUEST_REVIEW_ID)
            REFERENCES GUESTS_REVIEWS (GUEST_REVIEW_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (HOST_REVIEW_ID)
            REFERENCES HOSTS_REVIEWS (HOST_REVIEW_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (BOOKING_ID)
            REFERENCES BOOKINGS_CONFIRMATION (BOOKING_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
    );
```


Moving on, we'll grant each user its corresponding privileges : 

a) for the super user:
```shell 
-- Setting the database ownership to the administrator
GRANT ALL PRIVILEGES ON DATABASE AIRBNB TO superuser;
```


b) for the guest:
```shell 
-- Granting the corresponding privileges on tables to the guest user
GRANT SELECT, INSERT ON TABLE main.guests TO guest;
GRANT SELECT, INSERT ON TABLE main.guests_mailbox TO guest;
GRANT SELECT, INSERT ON TABLE main.guests_payments TO guest;
GRANT SELECT, INSERT ON TABLE main.guests_reviews TO guest;
GRANT SELECT, INSERT ON TABLE main.guests_support_requests TO guest;
GRANT SELECT, INSERT ON TABLE main.reservations TO guest;
GRANT SELECT, INSERT ON TABLE main.addresses TO guest;
GRANT SELECT, INSERT ON TABLE main.cities TO guest;
GRANT SELECT, INSERT ON TABLE main.beds_and_rooms TO guest;
GRANT SELECT, INSERT ON TABLE main.hosts TO guest;
GRANT SELECT, INSERT ON TABLE main.hosts_languages TO guest;
GRANT SELECT, INSERT ON TABLE main.hosts_reviews TO guest;
GRANT SELECT, INSERT ON TABLE main.properties TO guest;
GRANT SELECT, INSERT ON TABLE main.properties_capacities TO guest;
GRANT SELECT, INSERT ON TABLE main.properties_essentials TO guest;
GRANT SELECT, INSERT ON TABLE main.properties_features TO guest;
GRANT SELECT, INSERT ON TABLE main.properties_fees TO guest;
GRANT SELECT, INSERT ON TABLE main.property_images TO guest;
```


c) for the host:
```shell 
-- Granting the corresponding privileges on tables to the host user
GRANT SELECT, INSERT ON TABLE main.addresses TO host;
GRANT SELECT, INSERT ON TABLE main.cities TO host;
GRANT SELECT, INSERT ON TABLE main.beds_and_rooms TO host;
GRANT SELECT, INSERT ON TABLE main.hosts TO host;
GRANT SELECT, INSERT ON TABLE main.hosts_languages TO host;
GRANT SELECT, INSERT ON TABLE main.hosts_mailbox TO host;
GRANT SELECT, INSERT ON TABLE main.hosts_payout TO host;
GRANT SELECT, INSERT ON TABLE main.hosts_reviews TO host;
GRANT SELECT, INSERT ON TABLE main.hosts_support_requests TO host;
GRANT SELECT, INSERT ON TABLE main.properties TO host;
GRANT SELECT, INSERT ON TABLE main.properties_capacities TO host;
GRANT SELECT, INSERT ON TABLE main.properties_essentials TO host;
GRANT SELECT, INSERT ON TABLE main.properties_features TO host;
GRANT SELECT, INSERT ON TABLE main.properties_fees TO host;
GRANT SELECT, INSERT ON TABLE main.property_images TO host;
GRANT SELECT, INSERT ON TABLE main.guests TO host;
GRANT SELECT, INSERT ON TABLE main.guests_reviews TO host;
GRANT SELECT, INSERT ON TABLE main.reservations TO host;
```


Seeking to optimize data retrieval and sorting, indexes were created : 

 i) for data retrieval :
```shell
-- Creating Indexes for the database
-- Indexes created for columns frequently queried and used in JOIN or WHERE clauses
CREATE INDEX beds_and_rooms_property_id_index ON main.beds_and_rooms (property_id);
CREATE INDEX bookings_confirmation_reservations_id_index ON main.bookings_confirmation (reservation_id);
CREATE INDEX bookings_history_guest_review_id_index ON main.bookings_history (guest_review_id);
CREATE INDEX bookings_history_host_review_id_index ON main.bookings_history (host_review_id);
CREATE INDEX bookings_history_booking_id_index ON main.bookings_history (booking_id);
CREATE INDEX conversations_guest_id_index ON main.conversations (guest_id);
CREATE INDEX conversations_host_id_index ON main.conversations (host_id);
CREATE INDEX guests_mailbox_conversation_id_index ON main.guests_mailbox (conversation_id);
CREATE INDEX guests_payments_booking_id_index ON main.guests_payments (booking_id);
CREATE INDEX guests_reviews_guest_id_index ON main.guests_reviews (guest_id);
CREATE INDEX guests_support_requests_guest_id_index ON main.guests_support_requests (guest_id);
CREATE INDEX guests_support_requests_admin_id_index ON main.guests_support_requests (admin_id);
CREATE INDEX hosts_languages_host_id_index ON main.hosts_languages (host_id);
CREATE INDEX hosts_mailbox_conversation_id_index ON main.hosts_mailbox (conversation_id);
CREATE INDEX hosts_payout_booking_id_index ON main.hosts_payout (booking_id);
CREATE INDEX hosts_reviews_host_id_index ON main.hosts_reviews (host_id);
CREATE INDEX hosts_support_requests_host_id_index ON main.hosts_support_requests (host_id);
CREATE INDEX hosts_support_requests_admin_id_index ON main.hosts_support_requests (admin_id);
CREATE INDEX platform_revenue_booking_id_index ON main.platform_revenue (booking_id);
CREATE INDEX properties_address_id_index ON main.properties (address_id);
CREATE INDEX properties_host_id_index ON main.properties (host_id);
CREATE INDEX properties_capacities_property_id_index ON main.properties_capacities (property_id);
CREATE INDEX properties_essentials_property_id_index ON main.properties_essentials (property_id);
CREATE INDEX properties_features_property_id_index ON main.properties_features (property_id);
CREATE INDEX properties_fees_property_id_index ON main.properties_fees (property_id);
CREATE INDEX property_images_property_id_index ON main.property_images (property_id);
CREATE INDEX reservations_property_id_index ON main.reservations (property_id);
CREATE INDEX reservations_guest_id_index ON main.reservations (guest_id);
```


 ii) for data sorting :
``` shell
-- Indexes created for columns frequently GROUP BY clause
CREATE INDEX cities_country_index ON main.cities (country);
CREATE INDEX cities_continent_index ON main.cities (continent);
CREATE INDEX guests_reviews_ranking_index ON main.guests_reviews (ranking);
CREATE INDEX guests_support_requests_request_object_index ON main.guests_support_requests (request_object);
CREATE INDEX hosts_host_type_index ON main.hosts (host_type);
CREATE INDEX hosts_host_status_index ON main.hosts (host_status);
CREATE INDEX hosts_reviews_ranking_index ON main.hosts_reviews (ranking);
CREATE INDEX hosts_support_requests_request_object_index ON main.hosts_support_requests (request_object);
CREATE INDEX properties_property_type_index ON main.properties (property_type);
CREATE INDEX properties_rented_place_index ON main.properties (rented_place);
CREATE INDEX reservations_confirmed_index ON main.reservations (confirmed);
```


All of the statements mentioned before are located in the 'main.sql' file.


## Inserting th sample data

The provided data is not real and is intended for testing purposes only. 
The data is available in the form of a multi-row insert statement, you 
can run the command in your PostgreSQL terminal.

```shell 
\i data_insertion.sql
```

## Using the database 

Once you have the database set up and populated with data, you 
can begin querying the data using SQL commands. Here are a few 
example queries to get you started:


#### See the administrators with the highest number of handled requests
```shell 
SELECT C.first_name,
       C.last_name,
       A.received_hosts_requests,
       B.received_guests_requests,
       SUM(A.received_hosts_requests + B.received_guests_requests) AS total_requests
FROM (SELECT admin_id, COUNT(*) AS received_hosts_requests
      FROM main.hosts_support_requests
      GROUP BY admin_id) AS A
         JOIN (SELECT admin_id, COUNT(*) AS received_guests_requests
               FROM main.guests_support_requests
               GROUP BY admin_id) AS B ON A.admin_id = B.admin_id
         JOIN (SELECT admin_id, first_name, last_name FROM main.admins) AS C ON A.admin_id = C.admin_id
GROUP BY C.first_name, C.last_name, A.received_hosts_requests, B.received_guests_requests
ORDER BY total_requests DESC;
 ```


#### Find the deals in Morocco
```shell 
SELECT A.property_name, B.address_line, C.city, C.country, C.continent
FROM (SELECT property_id, property_name, address_id
      FROM main.properties) AS A
         JOIN (SELECT address_id, address_line, city_id FROM main.addresses)
    AS B ON A.address_id = B.address_id
         JOIN (SELECT city_id, city, country, continent FROM main.cities)
    AS C ON B.city_id = C.city_id
WHERE country = 'Morocco'
ORDER BY C.city;
```


#### Find accommodation in Asia for you and your pet
```shell 
SELECT A.property_name, B.address_line, C.city, C.country, C.continent
FROM (SELECT feature_id, pets_allowed, property_id
      FROM main.properties_features
      WHERE pets_allowed IS TRUE) AS D
         JOIN (SELECT property_id, property_name, address_id
               FROM main.properties) AS A ON A.property_id = D.property_id
         JOIN (SELECT address_id, address_line, city_id FROM main.addresses)
    AS B ON A.address_id = B.address_id
         JOIN (SELECT city_id, city, country, continent FROM main.cities)
    AS C ON B.city_id = C.city_id
WHERE continent = 'Asia'
ORDER BY C.country;
```

## Contributing

If you would like to contribute to this project, please feel free to submit a 
pull request. We welcome contributions of all kinds, including bug fixes, 
feature requests, and code improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

