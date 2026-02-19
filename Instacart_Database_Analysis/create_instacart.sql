SET SESSION max_execution_time = 0;
SET SESSION wait_timeout = 288000;
SET SESSION interactive_timeout = 288000;
SET SESSION net_read_timeout = 36000;
SET SESSION net_write_timeout = 36000;

-- Additional timeout and performance settings for large index creation
SET GLOBAL innodb_lock_wait_timeout = 3000;
SET GLOBAL connect_timeout = 3000;
SET GLOBAL max_allowed_packet = 1073741824;     -- 1GB

-- Increase memory for index creation 
SET SESSION sort_buffer_size = 268435456;        -- 256MB
SET SESSION read_buffer_size = 8388608;          -- 8MB
SET SESSION read_rnd_buffer_size = 16777216;     -- 16MB
SET SESSION bulk_insert_buffer_size = 268435456; -- 256MB

-- Disable unique checks and foreign key checks during bulk operations
SET SESSION unique_checks = 0;
SET SESSION foreign_key_checks = 0;

-- Disable autocommit for faster bulk operations
SET SESSION autocommit = 0;

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS instacart;
USE instacart;

-- Drop tables individually
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS order_products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS aisles;
DROP TABLE IF EXISTS departments;

SET FOREIGN_KEY_CHECKS = 1;
create table departments
	(department_id INT not null,
    department varchar(100) not null,
    primary key (department_id));

create table aisles
	(aisle_id INT not null,
    aisle varchar(255) not null, 
    primary key (aisle_id));

create table products
	(product_id INT not null,
    product_name varchar(255) not null,
    aisle_id INT not null,
    department_id INT not null,
    primary key (product_id));
    
create table orders
	(order_id INT not null,
    user_id	INT not null,
    eval_set varchar(10),
    order_number INT,
    order_dow INT,
    order_hour_of_day INT,
    days_since_prior INT,
    primary key (order_id));

create table order_products
	(order_id INT not null,
    product_id INT not null,
    add_to_cart_order INT,
    reordered char(1),
    primary key (order_id, product_id));
        
show tables;

/* before loading the .csv files to these tables, you need to check your file loading permission*/

SHOW VARIABLES LIKE "secure_file_priv";

SHOW VARIABLES LIKE 'local_infile'; 

SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'local_infile';

-- load data
-- Department table
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/departments.csv'
INTO TABLE Departments
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- aisles table
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/aisles.csv'
INTO TABLE aisles
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- products table
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- orders table
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- order_products table
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/order_products.csv'
INTO TABLE order_products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- load the order_products_prior table into the order_products
LOAD DATA LOCAL INFILE '/Users/laurenmitchek/Desktop/MIS 502/Final Project/order_products_prior.csv'
INTO TABLE order_products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/***Create indexes - optimized for large datasets***/

-- Indexes for products table (small table, fast)
CREATE INDEX idx_products_aisle ON products(aisle_id);
CREATE INDEX idx_products_department ON products(department_id);

-- Indexes for orders table
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_dow ON orders(order_dow);
CREATE INDEX idx_orders_hour ON orders(order_hour_of_day);
CREATE INDEX idx_orders_days_since_prior ON orders(days_since_prior);

CREATE INDEX idx_order_products_product
ON order_products(product_id)
ALGORITHM=INPLACE LOCK=NONE;

CREATE INDEX idx_order_products_reordered
ON order_products(reordered)
ALGORITHM=INPLACE LOCK=NONE;

/***Now add foreign key constraints - much faster with indexes in place***/
ALTER TABLE products
ADD CONSTRAINT fk_products_aisle
FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id);

ALTER TABLE products
ADD CONSTRAINT fk_products_department
FOREIGN KEY (department_id) REFERENCES departments(department_id);

ALTER TABLE order_products
ADD CONSTRAINT fk_order_products_order
FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_products
ADD CONSTRAINT fk_order_products_product
FOREIGN KEY (product_id) REFERENCES products(product_id);

COMMIT;

SET SESSION unique_checks = 1;
SET SESSION foreign_key_checks = 1;
SET SESSION autocommit = 1;
