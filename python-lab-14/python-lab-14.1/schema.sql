DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0)
);

INSERT INTO users (email, full_name) VALUES
    ('alice@example.com', 'Alice Smith'),
    ('bob@example.com', 'Bob Johnson'),
    ('carol@example.com', 'Carol Miller');

INSERT INTO products (name, category, price, stock_quantity) VALUES
    ('Laptop', 'Electronics', 75000.00, 10),
    ('Mouse', 'Electronics', 1500.00, 50),
    ('SQL Book', 'Books', 2500.00, 30),
    ('Keyboard', 'Electronics', 5000.00, 15),
    ('Python Book', 'Books', 3500.00, 20);

INSERT INTO orders (user_id, order_date, status) VALUES
    (1, '2024-02-01 10:00:00', 'completed'),
    (2, '2024-02-02 11:30:00', 'completed'),
    (1, '2024-02-03 17:45:00', 'completed'),
    (3, '2024-02-04 09:15:00', 'pending');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 75000.00),
    (1, 2, 2, 1500.00),
    (2, 3, 1, 2500.00),
    (2, 4, 1, 5000.00),
    (3, 5, 2, 3500.00),
    (3, 2, 1, 1500.00),
    (4, 4, 2, 5000.00);
