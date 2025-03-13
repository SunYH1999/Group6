USE GROUP6;

-- Insert administrator data
INSERT INTO administrators (username, password)
VALUES
    ('admin1', '123456');

-- Insert vendors data
INSERT INTO vendors (business_name, feedback_score, location)
VALUES
    ('Apple', 4.80, 'US'),
    ('Samsung', 4.70, 'KR'),
    ('Nike', 4.60, 'US'),
    ('Xiaomi', 4.65, 'CN'),
    ('Haier', 4.60, 'CN'),
    ('Starbucks', 4.30, 'US'),
    ('Adidas', 4.50, 'DE'),
    ('McDonalds', 4.20, 'US');

-- Insert customers data
INSERT INTO customers (contact_number, shipping_address, username, password)
VALUES
    ('13812345678', 'Shanghai', 'Zhangsan', '000000'),
    ('13987654321', 'Guangzhou', 'Lisi', '000000'),
    ('15811112222', 'HongKong', 'Xiaoming', '000000');

-- Insert products data
INSERT INTO products (vendor_id, name, price, tags)
VALUES
    (1, 'iPhone15', 999.99, '["Smartphone", "Electronics"]'),
    (1, 'MacBook Pro', 2399.99, '["Laptop", "Electronics"]'),
    (2, 'Galaxy S24', 899.99, '["Smartphone", "Electronics"]'),
    (2, 'Samsung QLED 8K TV', 3499.99, '["Television", "Electronics"]'),
    (3, 'Air Jordan 1', 179.99, '["Sneakers", "Footwear"]'),
    (3, 'Nike Dri - Fit T - Shirt', 29.99, '["Apparel", "Sportswear"]'),
    (4, 'Xiaomi 14', 599.99, '["Smartphone", "Electronics"]'),
    (4, 'Xiaomi Mi Pad 6', 299.99, '["Tablet", "Electronics"]'),
    (5, 'Haier Refrigerator', 1299.99, '["Appliance", "Home"]'),
    (5, 'Haier Air Conditioner', 1599.99, '["Appliance", "Home"]'),
    (6, 'Starbucks Blonde Roast Ground Coffee', 11.99, '["Beverage", "Coffee"]'),
    (6, 'Starbucks Cold Brew Coffee Concentrate', 14.99, '["Beverage", "Coffee"]'),
    (7, 'Adidas Ultraboost Running Shoes', 179.99, '["Sneakers", "Footwear"]'),
    (7, 'Adidas Soccer Ball', 29.99, '["Sports Equipment", "Ball"]'),
    (8, 'Big Mac Meal', 10.99, '["Food", "Fast Food"]'),
    (8, 'McChicken Sandwich', 3.99, '["Food", "Fast Food"]'),
    (8, 'Fries (Large)', 2.49, '["Food", "Fast Food"]');

-- Insert orders data
INSERT INTO orders (customer_id, total_amount, status)
VALUES
    (1, 299.99, 'pending'),
    (2, 2399.99, 'shipped'),
    (3, 13.48, 'pending');

-- Insert order_details data
INSERT INTO order_details (order_id, product_id, vendor_id, quantity)
VALUES
    (1, 8, 4, 1),
    (2, 2, 1, 1),
    (3, 15, 8, 2),
    (3, 17, 8, 1);

-- 插入评分数据
INSERT INTO ratings (customer_id, product_id, score)
VALUES
    (1, 1, 4),
    (2, 2, 5),
    (3, 3, 3),
    (1, 4, 4);