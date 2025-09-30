SELECT c.name AS client_name,
       COALESCE(SUM(oi.quantity * oi.price), 0) AS total_sum
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name
ORDER BY c.name;