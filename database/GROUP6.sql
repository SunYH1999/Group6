-- Create database
CREATE DATABASE IF NOT EXISTS GROUP6;
USE GROUP6;

-- Administrator Table (Unregisterable)
CREATE TABLE administrators (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- VendorList Table
CREATE TABLE vendors (
    vendor_id INT PRIMARY KEY AUTO_INCREMENT,
    business_name VARCHAR(255) NOT NULL,
    feedback_score DECIMAL(3,2) DEFAULT 0.00,
    location VARCHAR(255)
);

-- Product Table
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    tags JSON,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- Customers Table (Registrable)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    contact_number VARCHAR(20),
    shipping_address TEXT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Order Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    status ENUM('pending', 'shipped') DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- OrderDetails Table
CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    vendor_id INT,
    quantity INT DEFAULT 1,
    PRIMARY KEY (order_id, product_id, vendor_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- Rating Table
CREATE TABLE ratings (
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    score TINYINT CHECK (score BETWEEN 1 AND 5),
    rating_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE KEY unique_rating (customer_id, product_id)
);