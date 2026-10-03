-- Northwind Seed Data
-- Minimal but recognizable dataset from the classic Northwind database

BEGIN;

-- Categories
INSERT INTO categories (name, description) VALUES
    ('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
    ('Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
    ('Confections', 'Desserts, candies, and sweet breads'),
    ('Dairy Products', 'Cheeses'),
    ('Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
    ('Meat/Poultry', 'Prepared meats'),
    ('Produce', 'Dried fruit and bean curd'),
    ('Seafood', 'Seaweed and fish')
ON CONFLICT DO NOTHING;

-- Shippers
INSERT INTO shippers (company_name, phone) VALUES
    ('Speedy Express', '(503) 555-9831'),
    ('United Package', '(503) 555-3199'),
    ('Federal Shipping', '(503) 555-9931')
ON CONFLICT DO NOTHING;

-- Suppliers
INSERT INTO suppliers (company_name, contact_name, contact_title, city, country, phone) VALUES
    ('Exotic Liquids', 'Charlotte Cooper', 'Purchasing Manager', 'London', 'UK', '(171) 555-2222'),
    ('New Orleans Cajun Delights', 'Shelley Burke', 'Order Administrator', 'New Orleans', 'USA', '(100) 555-4822'),
    ('Grandma Kelly''s Homestead', 'Regina Murphy', 'Sales Representative', 'Ann Arbor', 'USA', '(313) 555-5735'),
    ('Tokyo Traders', 'Yoshi Nagase', 'Marketing Manager', 'Tokyo', 'Japan', '(03) 3555-5011'),
    ('Cooperativa de Quesos ''Las Cabras''', 'Antonio del Valle Saavedra', 'Export Administrator', 'Oviedo', 'Spain', '(98) 598 76 54'),
    ('Mayumi''s', 'Mayumi Ohno', 'Marketing Representative', 'Osaka', 'Japan', '(06) 431-7877'),
    ('Pavlova, Ltd.', 'Ian Devling', 'Marketing Manager', 'Melbourne', 'Australia', '(03) 444-2343'),
    ('Specialty Biscuits, Ltd.', 'Peter Wilson', 'Sales Representative', 'Manchester', 'UK', '(161) 555-4448')
ON CONFLICT DO NOTHING;

-- Products
INSERT INTO products (name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, discontinued) VALUES
    ('Chai', 1, 1, '10 boxes x 20 bags', 18.00, 39, FALSE),
    ('Chang', 1, 1, '24 - 12 oz bottles', 19.00, 17, FALSE),
    ('Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10.00, 13, FALSE),
    ('Chef Anton''s Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.00, 53, FALSE),
    ('Grandma''s Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25.00, 120, FALSE),
    ('Uncle Bob''s Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30.00, 15, FALSE),
    ('Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40.00, 6, FALSE),
    ('Ikura', 4, 8, '12 - 200 ml jars', 31.00, 31, FALSE),
    ('Queso Cabrales', 5, 4, '1 kg pkg.', 21.00, 22, FALSE),
    ('Queso Manchego La Pastora', 5, 4, '10 - 500 g pkgs.', 38.00, 86, FALSE),
    ('Konbu', 6, 8, '2 kg box', 6.00, 24, FALSE),
    ('Tofu', 6, 7, '40 - 100 g pkgs.', 23.25, 35, FALSE),
    ('Pavlova', 7, 3, '32 - 500 g boxes', 17.45, 29, FALSE),
    ('Alice Mutton', 7, 6, '20 - 1 kg tins', 39.00, 0, TRUE),
    ('Teatime Chocolate Biscuits', 8, 3, '10 boxes x 12 pieces', 9.20, 25, FALSE)
ON CONFLICT DO NOTHING;

-- Sample customers
INSERT INTO customers (company_name, contact_name, contact_title, address, city, region, postal_code, country, phone) VALUES
    ('Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany', '030-0074321'),
    ('Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', NULL, 'WA1 1DP', 'UK', '(171) 555-7788'),
    ('Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Berguvsvägen 8', 'Luleå', NULL, 'S-958 22', 'Sweden', '0921-12 34 65'),
    ('Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Accounting Manager', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada', '(604) 555-4729'),
    ('Eastern Connection', 'Ann Devon', 'Sales Agent', '35 King George', 'London', NULL, 'WX3 6FW', 'UK', '(171) 555-0297')
ON CONFLICT DO NOTHING;

COMMIT;
