SELECT c.id,
       c.name,
       COUNT(ch.id) AS child_count
FROM categories c
LEFT JOIN categories ch ON ch.parent_id = c.id
GROUP BY c.id, c.name
ORDER BY c.name;