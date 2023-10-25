-- Test N°1
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

-- Test N°2
SELECT A.property_name, B.address_line, C.city, C.country, C.continent
FROM (SELECT property_id, property_name, address_id
      FROM main.properties) AS A
         JOIN (SELECT address_id, address_line, city_id FROM main.addresses)
    AS B ON A.address_id = B.address_id
         JOIN (SELECT city_id, city, country, continent FROM main.cities)
    AS C ON B.city_id = C.city_id
ORDER BY C.continent;

-- Test N°3
SELECT D.property_name, A.total_per_booking
FROM (SELECT revenue_id, total_per_booking, booking_id
      FROM main.platform_revenue) AS A
         JOIN (SELECT booking_id, reservation_id FROM main.bookings_confirmation)
    AS B ON A.booking_id = B.booking_id
         JOIN (SELECT reservation_id, property_id
               FROM main.reservations
               WHERE check_in > DATE('2023-01-01') AND check_out < DATE('2023-05-01'))
    AS C ON B.reservation_id = C.reservation_id
         JOIN (SELECT property_id, property_name FROM main.properties)
    AS D ON C.property_id = D.property_id
ORDER BY A.total_per_booking DESC;

-- Test N°4
UPDATE main.properties
SET property_name = 'Riyad BARBOU'
WHERE property_id = 29;
SELECT property_id
FROM main.properties
WHERE properties.property_name LIKE 'Riyad BARBOU';

-- Test N°5
DELETE
FROM main.hosts
WHERE host_id = 1;
SELECT *
FROM main.hosts
WHERE host_id = 1;

INSERT INTO main.hosts (first_name, last_name, email, phone_number, host_type, host_status)
VALUES ('Alfred', 'Edinburgh', 'Alfred.bruge@example.com', '+123-789-4561', 'Individual', 'Regular');
SELECT *
FROM hosts
WHERE first_name LIKE 'Alfred';