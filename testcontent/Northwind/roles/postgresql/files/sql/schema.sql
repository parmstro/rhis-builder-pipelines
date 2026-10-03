-- Northwind Database Schema
-- Based on the classic Northwind sample database
-- Adapted for PostgreSQL on RHEL

BEGIN;

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE,
    contact_name VARCHAR(100),
    contact_title VARCHAR(50),
    address VARCHAR(200),
    city VARCHAR(50),
    region VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    phone VARCHAR(30),
    fax VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    supplier_id INTEGER REFERENCES suppliers(id),
    category_id INTEGER REFERENCES categories(id),
    quantity_per_unit VARCHAR(50),
    unit_price DECIMAL(10,2) DEFAULT 0,
    units_in_stock INTEGER DEFAULT 0,
    units_on_order INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 0,
    discontinued BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE,
    contact_name VARCHAR(100),
    contact_title VARCHAR(50),
    address VARCHAR(200),
    city VARCHAR(50),
    region VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    phone VARCHAR(30),
    fax VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS shippers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    shipper_id INTEGER REFERENCES shippers(id),
    freight DECIMAL(10,2) DEFAULT 0,
    ship_name VARCHAR(100),
    ship_address VARCHAR(200),
    ship_city VARCHAR(50),
    ship_region VARCHAR(50),
    ship_postal_code VARCHAR(20),
    ship_country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    discount DECIMAL(4,2) DEFAULT 0
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_supplier ON products(supplier_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_order_details_order ON order_details(order_id);
CREATE INDEX IF NOT EXISTS idx_order_details_product ON order_details(product_id);

COMMIT;
