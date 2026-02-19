USE instacart;

-- Query 1: How frequently do users place orders?
SELECT
    CASE
        WHEN days_since_prior <= 7 THEN 'once_a_week'
        WHEN days_since_prior > 7 AND days_since_prior <= 14 THEN 'once_2_weeks'
        WHEN days_since_prior >= 30 THEN 'once_a_month'
        WHEN days_since_prior > 14 AND days_since_prior < 30 THEN 'once_3_weeks'
    END AS order_frequency,
    COUNT(DISTINCT user_id) AS number_of_users,
    COUNT(order_id) AS number_of_orders
FROM orders
WHERE days_since_prior IS NOT NULL
GROUP BY order_frequency
ORDER BY number_of_users DESC;

CREATE OR REPLACE VIEW user_frequency AS
SELECT
    user_id,
    CASE
        WHEN AVG(days_since_prior) <= 7 THEN 'once_a_week'
        WHEN AVG(days_since_prior) >= 30 THEN 'once_a_month'
        ELSE 'other'
    END AS frequency_category
FROM orders
WHERE days_since_prior IS NOT NULL
GROUP BY user_id;

-- Query 2: Calculate average products per order for each user category
SELECT
      frequency_category,
      COUNT(DISTINCT order_frequency.order_id) AS total_orders,
      COUNT(op.product_id) AS total_products,
      ROUND(COUNT(op.product_id) / COUNT(DISTINCT order_frequency.order_id),
   2) AS avg_products_per_order
  FROM (
      SELECT
          o.order_id,
          o.user_id,
          CASE
              WHEN o.days_since_prior <= 7 THEN 'once_a_week'
              WHEN o.days_since_prior >= 30 THEN 'once_a_month'
          END AS frequency_category
      FROM orders o
      WHERE o.days_since_prior IS NOT NULL
  ) AS order_frequency
  JOIN order_products op ON order_frequency.order_id = op.order_id
  WHERE frequency_category IN ('once_a_week', 'once_a_month')
  GROUP BY frequency_category;

-- Query 3: Top 5 products reordered by weekly users
SELECT
    p.product_id,
    p.product_name,
    COUNT(*) AS reorder_count
FROM user_frequency uf
JOIN orders o ON uf.user_id = o.user_id
JOIN order_products op ON o.order_id = op.order_id
JOIN products p ON op.product_id = p.product_id
WHERE uf.frequency_category = 'once_a_week'
  AND op.reordered = '1'
GROUP BY p.product_id, p.product_name
ORDER BY reorder_count DESC
LIMIT 5;


-- Query 4: Relationship between reorder count and add_to_cart_order
SELECT 
    p.product_id,
    p.product_name,
    COUNT(*) AS reorder_count,
    ROUND(AVG(op.add_to_cart_order), 2) AS avg_add_to_cart_order
FROM products p 
JOIN order_products op ON p.product_id = op.product_id
WHERE op.reordered = '1'
    AND p.product_id % 100 = 0  -- Sample every 100th product
GROUP BY p.product_id, p.product_name
ORDER BY reorder_count DESC;


-- Query 5: Segment users by average reorder interval (5 segments)
SELECT
      user_segment,
      COUNT(user_id) AS number_of_users
  FROM (
      SELECT
          user_id,
          AVG(days_since_prior) AS avg_days,
          CASE
              WHEN AVG(days_since_prior) <= 7 THEN '1-7 days'
              WHEN AVG(days_since_prior) > 7 AND AVG(days_since_prior) <= 12
   THEN '8-12 days'
              WHEN AVG(days_since_prior) > 12 AND AVG(days_since_prior) <=
  18 THEN '13-18 days'
              WHEN AVG(days_since_prior) > 18 AND AVG(days_since_prior) <=
  24 THEN '19-24 days'
              WHEN AVG(days_since_prior) > 24 THEN '25+ days'
          END AS user_segment
      FROM orders
      WHERE days_since_prior IS NOT NULL
      GROUP BY user_id
  ) AS user_segments
  GROUP BY user_segment
  ORDER BY
      CASE user_segment
          WHEN '1-7 days' THEN 1
          WHEN '8-12 days' THEN 2
          WHEN '13-18 days' THEN 3
          WHEN '19-24 days' THEN 4
          WHEN '25+ days' THEN 5
      END;


-- Query 6: Department with most/least products ordered
SELECT
    d.department,
    COUNT(op.product_id) AS total_units_ordered
FROM departments d
JOIN products p ON d.department_id = p.department_id
JOIN order_products op ON p.product_id = op.product_id
GROUP BY d.department
ORDER BY total_units_ordered DESC;

-- Most/least unique products ordered
SELECT
    d.department,
    COUNT(DISTINCT op.product_id) AS unique_products_ordered
FROM departments d
JOIN products p ON d.department_id = p.department_id
JOIN order_products op ON p.product_id = op.product_id
GROUP BY d.department
ORDER BY unique_products_ordered DESC;


-- Query 7: Products that have never been ordered
SELECT
    p.product_id,
    p.product_name,
    a.aisle,
    d.department
FROM products p
LEFT JOIN order_products op ON p.product_id = op.product_id
JOIN aisles a ON p.aisle_id = a.aisle_id
JOIN departments d ON p.department_id = d.department_id
WHERE op.product_id IS NULL;


-- Query 8: Aisle containing most top-selling products
-- Top-selling = top 100 products by number of orders
-- First identify top 100 products
CREATE OR REPLACE VIEW top_100_products AS
SELECT
    product_id,
    COUNT(DISTINCT order_id) AS order_count
FROM order_products
GROUP BY product_id
ORDER BY order_count DESC
LIMIT 100;

-- Find which aisle contains the most top-selling products
SELECT
    p.aisle_id,
    a.aisle,
    COUNT(t.product_id) AS top_products_count
FROM top_100_products t
JOIN products p ON t.product_id = p.product_id
JOIN aisles a ON p.aisle_id = a.aisle_id
GROUP BY p.aisle_id, a.aisle
ORDER BY top_products_count DESC;


-- Query 9: Products ordered only once in the top-selling aisle
SET @top_aisle_id = (
    SELECT
        p.aisle_id
    FROM top_100_products t
    JOIN products p ON t.product_id = p.product_id
    GROUP BY p.aisle_id
    ORDER BY COUNT(t.product_id) DESC
    LIMIT 1
);

-- Products ordered only once in that aisle
SELECT
    p.product_id,
    p.product_name,
    a.aisle
FROM products p
JOIN aisles a ON p.aisle_id = a.aisle_id
JOIN (
    SELECT
        product_id,
        SUM(CASE WHEN reordered = '1' THEN 1 ELSE 0 END) AS reorder_sum
    FROM order_products
    GROUP BY product_id
) AS reorder_stats ON p.product_id = reorder_stats.product_id
WHERE p.aisle_id = @top_aisle_id
  AND reorder_stats.reorder_sum = 0;


-- Query 10: Top 10 products most often first in shopping cart
SELECT
    p.product_id,
    p.product_name,
    d.department,
    COUNT(*) AS first_in_cart_count
FROM order_products op
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
WHERE op.add_to_cart_order = 1  -- No quotes needed, add_to_cart_order is now INT
GROUP BY p.product_id, p.product_name, d.department
ORDER BY first_in_cart_count DESC
LIMIT 10;


-- Query 11: Are top 10 most-ordered products likely to be reordered?
-- Reorder ratio > 60% means likely to be reordered
-- First identify top 10 most-ordered products
CREATE OR REPLACE VIEW top_10_ordered AS
SELECT
    product_id,
    COUNT(order_id) AS total_orders
FROM order_products
GROUP BY product_id
ORDER BY total_orders DESC
LIMIT 10;

-- Calculate reorder ratio for these products
SELECT
    p.product_id,
    p.product_name,
    t.total_orders,
    COUNT(CASE WHEN op.reordered = '1' THEN 1 END) AS reorder_count,
    ROUND(COUNT(CASE WHEN op.reordered = '1' THEN 1 END) / t.total_orders * 100, 2) AS reorder_ratio_percent,
    CASE
        WHEN COUNT(CASE WHEN op.reordered = '1' THEN 1 END) / t.total_orders > 0.60
        THEN 'Yes - Likely to be reordered'
        ELSE 'No - Not likely to be reordered'
    END AS reorder_likelihood
FROM top_10_ordered t
JOIN order_products op ON t.product_id = op.product_id
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id, p.product_name, t.total_orders
ORDER BY reorder_ratio_percent DESC;


-- Query 12: Are organic products sold more than non-organic?
SELECT
    CASE
        WHEN p.product_name LIKE '%Organic%' THEN 'Organic'
        ELSE 'Non-Organic'
    END AS product_type,
    COUNT(DISTINCT p.product_id) AS unique_products,
    COUNT(op.product_id) AS total_units_sold,
    COUNT(DISTINCT op.order_id) AS total_orders
FROM products p
JOIN order_products op ON p.product_id = op.product_id
GROUP BY product_type;


-- Query 13: Top 5 products per department
SELECT
    department,
    product_id,
    product_name,
    order_count,
    dept_rank
FROM (
    SELECT
        d.department,
        p.product_id,
        p.product_name,
        COUNT(DISTINCT op.order_id) AS order_count,
        ROW_NUMBER() OVER (PARTITION BY d.department ORDER BY COUNT(DISTINCT op.order_id) DESC) AS dept_rank
    FROM departments d
    JOIN products p ON d.department_id = p.department_id
    JOIN order_products op ON p.product_id = op.product_id
    GROUP BY d.department, p.product_id, p.product_name
) AS ranked_products
WHERE dept_rank <= 5
ORDER BY department, dept_rank;


-- Query 14: Weekday with highest/lowest number of orders
SELECT
    order_dow,
    CASE order_dow
        WHEN 0 THEN 'Saturday'
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
    END AS day_name,
    COUNT(order_id) AS order_count
FROM orders
GROUP BY order_dow
ORDER BY order_count DESC;


-- Query 15: Top 3 prime times (weekday + hour) for reorders
SELECT
    CASE o.order_dow
        WHEN 0 THEN 'Saturday'
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
    END AS day_name,
    CASE
        WHEN o.order_hour_of_day = 0 THEN '12am'
        WHEN o.order_hour_of_day < 12 THEN CONCAT(o.order_hour_of_day, 'am')
        WHEN o.order_hour_of_day = 12 THEN '12pm'
        ELSE CONCAT(o.order_hour_of_day - 12, 'pm')
    END AS hour_label,
    CONCAT(
        CASE o.order_dow
            WHEN 0 THEN 'Saturday'
            WHEN 1 THEN 'Sunday'
            WHEN 2 THEN 'Monday'
            WHEN 3 THEN 'Tuesday'
            WHEN 4 THEN 'Wednesday'
            WHEN 5 THEN 'Thursday'
            WHEN 6 THEN 'Friday'
        END,
        ' ',
        CASE
            WHEN o.order_hour_of_day = 0 THEN '12am'
            WHEN o.order_hour_of_day < 12 THEN CONCAT(o.order_hour_of_day, 'am')
            WHEN o.order_hour_of_day = 12 THEN '12pm'
            ELSE CONCAT(o.order_hour_of_day - 12, 'pm')
        END
    ) AS prime_time,
    COUNT(DISTINCT o.order_id) AS reorder_count
FROM orders o
JOIN order_products op ON o.order_id = op.order_id
WHERE o.days_since_prior >= 0
  AND op.reordered = '1'
GROUP BY o.order_dow, o.order_hour_of_day
ORDER BY reorder_count DESC
LIMIT 3;