from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("lab14_postgres_demo.db")


def setup_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        );

        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
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
        """
    )
    connection.commit()


def print_query(title: str, connection: sqlite3.Connection, sql: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    cursor = connection.execute(sql)
    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    for row in cursor.fetchall():
        print(" | ".join(str(item) for item in row))


def main() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        setup_database(connection)
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)"
        )

        print_query(
            "Orders with totals",
            connection,
            """
            SELECT
                o.order_id,
                u.full_name,
                o.order_date,
                o.status,
                SUM(oi.quantity * oi.unit_price) AS total_amount
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY o.order_id, u.full_name, o.order_date, o.status
            ORDER BY total_amount DESC
            """,
        )

        print_query(
            "Revenue by category (> 10000)",
            connection,
            """
            SELECT
                p.category,
                SUM(oi.quantity) AS total_sold,
                SUM(oi.quantity * oi.unit_price) AS total_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.category
            HAVING SUM(oi.quantity * oi.unit_price) > 10000
            ORDER BY total_revenue DESC
            """,
        )

        print_query(
            "Top-3 users by spending",
            connection,
            """
            WITH user_totals AS (
                SELECT
                    u.user_id,
                    u.full_name,
                    SUM(oi.quantity * oi.unit_price) AS total_spent
                FROM users u
                JOIN orders o ON u.user_id = o.user_id
                JOIN order_items oi ON o.order_id = oi.order_id
                GROUP BY u.user_id, u.full_name
            )
            SELECT *
            FROM user_totals
            ORDER BY total_spent DESC
            LIMIT 3
            """,
        )

        print_query(
            "SQLite execution plan for order lookup",
            connection,
            "EXPLAIN QUERY PLAN SELECT * FROM order_items WHERE order_id = 1",
        )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
