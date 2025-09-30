-- Оптимизации для повышения производительности при росте данных:
-- 1 Индексация:
--    - индекс по orders.created_at (ускоряет фильтрацию по дате);
--    - составной индекс (order_items.product_id, order_items.quantity) для агрегации.
-- 2 Денормализация:
--    - хранить у товара ссылку сразу на категорию верхнего уровня,
--      чтобы избежать лишнего JOIN с categories.
-- 3 Материализация:
--    - использовать материализованное представление или отдельную
--      агрегирующую таблицу (например, "sales_stats"), которая обновляется
--      раз в сутки/час и хранит количество продаж по товарам.
-- 4 Разделение нагрузки:
--    - вынести отчётные запросы в отдельную БД (OLAP),
--      чтобы не нагружать транзакционную (OLTP).
-- 5 Партиционирование:
--    - использовать партиции по дате в orders и order_items для ускорения фильтрации
--      при больших объёмах данных (тысячи заказов в день).

SELECT p.name AS product_name,
       rc.name AS top_level_category,
       SUM(oi.quantity) AS total_qty
FROM products p
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o ON o.id = oi.order_id
JOIN categories c ON c.id = p.category_id
LEFT JOIN categories rc ON rc.id = c.parent_id
WHERE o.created_at >= :date_from
GROUP BY p.id, p.name, rc.name
ORDER BY SUM(oi.quantity) DESC
LIMIT 5;
