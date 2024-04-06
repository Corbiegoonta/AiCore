-- SELECT country_code AS country, COUNT(country_code) AS total_no_stores FROM dim_store_details GROUP BY country_code ORDER BY total_no_stores DESC
-- SELECT locality, COUNT(locality) as total_no_stores FROM dim_store_details GROUP BY locality ORDER BY total_no_stores DESC
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(8,2)) AS total_sales, month FROM (SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products) GROUP BY month ORDER BY total_sales DESC
-- SELECT COUNT(store_code) AS numbers_of_sales, SUM(product_quantity) AS product_quantity_count, CASE WHEN store_code = 'WEB-1388012W' THEN 'Web' ELSE 'Offline' END AS location FROM (SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products) GROUP BY location ORDER BY numbers_of_sales ASC
-- SELECT store_type, CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, CAST(100 * SUM(product_quantity * product_price)/(SELECT CAST((SUM(product_quantity * product_price)) AS DECIMAL(9,2)) FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products ) AS DECIMAL(4,2)) AS "percentage_total(%)" FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY store_type ORDER BY total_sales DESC
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, year, month FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY year, month ORDER BY total_sales DESC LIMIT 10
-- SELECT SUM(staff_numbers) AS total_staff_numbers, country_code FROM dim_store_details GROUP BY country_code ORDER BY total_staff_numbers DESC
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, store_type, country_code FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products WHERE country_code = 'DE' GROUP BY store_type, country_code ORDER BY total_sales ASC
-- WITH date_times AS (
-- SELECT
-- year,
-- month,
-- day,
-- timestamp,
-- TO_TIMESTAMP(CONCAT(year, '/', month, '/', day, '/', timestamp), 'YYYY/MM/DD/HH24:MI:ss') as times

-- 			   FROM dim_date_times d
-- 					 JOIN orders_table o
-- 					 ON d.date_uuid = o.date_uuid
-- 					 JOIN dim_store_details s
-- 					 ON o.store_code = s.store_code
-- 			   ORDER BY times DESC),		   	


-- next_times AS(
-- SELECT year,
-- timestamp,
-- times,
-- LEAD(times) OVER(ORDER BY times DESC) AS next_times
-- FROM date_times),

-- avg_times AS(
-- SELECT year,
-- (AVG(times - next_times)) AS avg_times
-- FROM next_times
-- GROUP BY year
-- ORDER BY avg_times DESC)

-- SELECT year,
-- -- concat('hours: ', cast(round(avg(EXTRACT(HOUR FROM avg_times))) as text),
-- -- 	   ', minutes: ', cast(round(avg(EXTRACT(MINUTE FROM avg_times))) as text),
-- -- 	   ', seconds: ', cast(round(avg(EXTRACT(SECOND FROM avg_times))) as text))
-- -- 	   as actual_time_taken

-- 	CONCAT('"Hours": ', (EXTRACT(HOUR FROM avg_times)),','
-- 	' "minutes" :', (EXTRACT(MINUTE FROM avg_times)),','
--     ' "seconds" :', ROUND(EXTRACT(SECOND FROM avg_times)),','
--      ' "milliseconds" :', ROUND((EXTRACT( SECOND FROM avg_times)- FLOOR(EXTRACT(SECOND FROM avg_times)))*100))
	
--    as actual_time_taken


-- FROM avg_times
-- GROUP BY year, avg_times
-- ORDER BY avg_times DESC
-- LIMIT 5;

-- SELECT COUNT(dim_date_times.month) as total_sales, dim_date_times.month FROM dim_date_times GROUP BY dim_date_times.month ORDER BY dim_date_times.month;
-- SELECT product_price * product_quantity AS total_sales, dim_date_times.month FROM dim_products, orders_table, dim_date_times GROUP BY dim_products.product_price, orders_table.product_quantity, dim_date_times.month
-- SELECT SUM(product_price * (SELECT product_quantity FROM orders_table FULL JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid)) AS total_sales, dim_date_times.month FROM dim_products, dim_date_times GROUP BY dim_date_times.month ORDER BY total_sales DESC 
-- SELECT COUNT(dim_date_times.month) AS total_sales, dim_date_times.month FROM dim_date_times GROUP BY dim_date_times.month ORDER BY total_sales DESC
-- SELECT * FROM dim_date_times WHERE date_uuid IN (SELECT date_ FROM orders_table WHERE product_code IN orders_table.product_code = dim_products.product_code)  
-- (SELECT product_price FROM dim_products WHERE dim_products.product_code = orders_table.product_code) UNION (SELECT product_quanity FROM orders_table WHERE dim_products.product_code = orders_table.product_code)
-- SELECT * FROM dim_products LEFT JOIN orders_table ON dim_products.product_code = orders_table.product_code
-- SELECT * FROM dim_products NATURAL JOIN orders_table
-- SELECT * FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products NATURAL JOIN orders_table)
-- SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(8,2)) AS total_sales, month FROM (SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products) GROUP BY month ORDER BY total_sales DESC
-- SELECT SUM((SELECT product_quantity FROM (SELECT * FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products NATURAL JOIN orders_table)) WHERE product_quantity IN (SELECT product_quantity FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products NATURAL JOIN orders_table))) * (SELECT product_price FROM (SELECT * FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products NATURAL JOIN orders_table)) WHERE product_price IN (SELECT product_price FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products LEFT JOIN orders_table ON dim_products.product_code = orders_table.product_code)))) AS total_sales, (SELECT month FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products LEFT JOIN orders_table ON dim_products.product_code = orders_table.product_code)) GROUP BY (SELECT month FROM dim_date_times NATURAL JOIN (SELECT * FROM dim_products LEFT JOIN orders_table ON dim_products.product_code = orders_table.product_code)) ORDER BY total_sales DESC
-- SELECT COUNT(store_code) AS numbers_of_sales, SUM(product_quantity) AS product_quantity_count, CASE WHEN store_type = 'Web Portal' THEN 'Web' ELSE 'Offline' END AS location FROM (SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products) GROUP BY location ORDER BY numbers_of_sales ASC
-- SELECT * FROM (SELECT * FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products NATURAL JOIN dim_store_details) LEFT JOIN dim_store_details ON (SELECT store_code FROM orders_table NATURAL JOIN dim_date_times NATURAL JOIN dim_products NATURAL JOIN dim_store_details) = dim_store_details.store_code
-- SELECT * FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products
-- SELECT store_type, CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, CAST(100 * SUM(product_quantity * product_price)/(SELECT CAST((SUM(product_quantity * product_price)) AS DECIMAL(9,2)) FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products ) AS DECIMAL(4,2)) AS "percentage_total(%)" FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY store_type ORDER BY total_sales DESC
-- SELECT CAST((SUM(product_quantity * product_price)) AS DECIMAL(9,2)) FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products 
-- SELECT (SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products), DISTINCT(year), DISTINCT(month) FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY year, month
-- SELECT CAST(MAX(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, year FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY year ORDER BY total_sales DESC
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, year, month FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY year, month ORDER BY total_sales DESC LIMIT 10
-- SELECT month FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products
-- SELECT CAST(MAX(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products
-- SELECT (SELECT staff_numbers FROM ((SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products) AS total_staff_numbers, country_code FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products GROUP BY country_code, staff_numbers ORDER BY total_staff_numbers DESC
-- SELECT SUM(staff_numbers) AS total_staff_numbers, country_code FROM dim_store_details GROUP BY country_code ORDER BY total_staff_numbers DESC
-- SELECT CAST(SUM(product_quantity * product_price) AS DECIMAL(9,2)) AS total_sales, store_type, country_code FROM (SELECT * FROM orders_table LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code) NATURAL JOIN dim_date_times NATURAL JOIN dim_products WHERE country_code = 'DE' GROUP BY store_type, country_code ORDER BY total_sales ASC
-- SELECT year, () AS actual_time_taken FROM dim_date_times GROUP BY year ORDER BY actual_time_taken DESC
-- ALTER TABLE dim_date_times
-- ALTER COLUMN month TYPE SMALLINT USING month::SMALLINT;
-- SELECT timestamp, day, month, year FROM dim_date_times ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC
-- SELECT timestamp, (LEAD(timestamp, 1) OVER(ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC)) as timestampl, day, month, year FROM dim_date_times ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC, timestampl ASC
-- SELECT month, day, year, timestamp FROM dim_date_times ORDER BY month, day, year, timestamp
-- SELECT CASE WHEN (LEAD(timestamp, 1) OVER(ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC) > timestamp) THEN ((LEAD(timestamp, 1) OVER(ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC)) - timestamp) ELSE ((timestamp - ('1 hour':: INTERVAL * 24)):: INTERVAL) + (LEAD(timestamp, 1) OVER(ORDER BY year ASC, month ASC, CAST(day AS INT) ASC, timestamp ASC)) END AS time_diff FROM dim_date_times


-- SELECT * FROM dim_store_details
-- SELECT * FROM dim_users
-- SELECT * FROM dim_products
-- SELECT * FROM dim_card_details
-- SELECT * FROM dim_date_times
-- SELECT * FROM orders_table