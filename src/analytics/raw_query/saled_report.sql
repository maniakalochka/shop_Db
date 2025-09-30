SELECT p.name AS product_name,
       rc.name AS top_level_category,
       SUM(oi.quantity) AS total_qty
FROM products p
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o ON o.id = oi.order_id
JOIN categories c ON c.id = p.category_id
LEFT JOIN categories rc ON rc.id = c.parent_id
WHERE o.created_at >= :date_from
  /* если не sliding: AND o.created_at < :date_to */
GROUP BY p.id, p.name, rc.name
ORDER BY SUM(oi.quantity) DESC
LIMIT 5;