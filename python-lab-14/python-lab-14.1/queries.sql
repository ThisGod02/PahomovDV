\echo '1. Orders with totals'
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
ORDER BY total_amount DESC;

\echo '2. Revenue by category (> 10000)'
SELECT
    p.category,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
HAVING SUM(oi.quantity * oi.unit_price) > 10000
ORDER BY total_revenue DESC;

\echo '3. Top-3 users by spending (CTE)'
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
LIMIT 3;

\echo '4. Index and execution plan'
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
EXPLAIN ANALYZE
SELECT *
FROM order_items
WHERE order_id = 1;
