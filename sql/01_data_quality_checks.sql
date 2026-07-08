-- =============================================================================
-- OLIST E-COMMERCE | DATA QUALITY & FAMILIARISATION
-- Analyst: Victor Otobo
-- Purpose: Understand the dataset before analysis. Validate completeness,
--          identify nulls, and confirm row counts per table.
-- =============================================================================


-- ------------------------------------------------------------
-- SECTION 1: ROW COUNTS PER TABLE
-- Confirms what we are working with before joining anything.
-- ------------------------------------------------------------

SELECT 'olist_orders'             AS table_name, COUNT(*) AS row_count FROM olist_orders_dataset
UNION ALL
SELECT 'olist_order_items',        COUNT(*) FROM olist_order_items_dataset
UNION ALL
SELECT 'olist_customers',          COUNT(*) FROM olist_customers_dataset
UNION ALL
SELECT 'olist_products',           COUNT(*) FROM olist_products_dataset
UNION ALL
SELECT 'olist_sellers',            COUNT(*) FROM olist_sellers_dataset
UNION ALL
SELECT 'olist_order_reviews',      COUNT(*) FROM olist_order_reviews_dataset
UNION ALL
SELECT 'olist_order_payments',     COUNT(*) FROM olist_order_payments_dataset
UNION ALL
SELECT 'olist_geolocation',        COUNT(*) FROM olist_geolocation_dataset;


-- ------------------------------------------------------------
-- SECTION 2: ORDER STATUS DISTRIBUTION
-- Understanding what proportion of orders were actually delivered
-- is critical — undelivered orders will be excluded from
-- delivery performance analysis.
-- ------------------------------------------------------------

SELECT
    order_status,
    COUNT(*)                                        AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY order_count DESC;


-- ------------------------------------------------------------
-- SECTION 3: DATE RANGE OF THE DATASET
-- Confirms the time window we are working within.
-- ------------------------------------------------------------

SELECT
    MIN(order_purchase_timestamp)   AS earliest_order,
    MAX(order_purchase_timestamp)   AS latest_order,
    DATEDIFF(DAY,
        MIN(order_purchase_timestamp),
        MAX(order_purchase_timestamp))              AS total_days_span
FROM olist_orders_dataset;


-- ------------------------------------------------------------
-- SECTION 4: NULL AUDIT — DELIVERY TIMESTAMPS
-- These timestamps are required to calculate delivery delta.
-- Any order missing them must be excluded and the row count
-- documented in the Caveats section.
-- ------------------------------------------------------------

SELECT
    COUNT(*)                                        AS total_orders,
    SUM(CASE WHEN order_delivered_customer_date IS NULL THEN 1 ELSE 0 END)
                                                    AS missing_actual_delivery,
    SUM(CASE WHEN order_estimated_delivery_date IS NULL THEN 1 ELSE 0 END)
                                                    AS missing_estimated_delivery,
    SUM(CASE WHEN order_purchase_timestamp IS NULL THEN 1 ELSE 0 END)
                                                    AS missing_purchase_date,
    ROUND(
        SUM(CASE WHEN order_delivered_customer_date IS NULL THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2)                      AS pct_missing_actual_delivery
FROM olist_orders_dataset;

---- 
SELECT
    order_status,
    COUNT(*) AS order_count
FROM olist_orders_dataset
WHERE order_delivered_customer_date IS NULL
GROUP BY order_status
ORDER BY order_count DESC;

-- ------------------------------------------------------------
-- SECTION 5: REVIEW SCORE DISTRIBUTION
-- Understanding the shape of review scores upfront.
-- A heavy skew toward 5 is typical — important context
-- when interpreting average scores later.
-- ------------------------------------------------------------

SELECT
    review_score,
    COUNT(*)                                        AS review_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_reviews
FROM olist_order_reviews_dataset
GROUP BY review_score
ORDER BY review_score;


-- ------------------------------------------------------------
-- SECTION 6: ORDERS WITH REVIEWS JOINED
-- Confirms join integrity between orders and reviews.
-- Not every order has a review — document the gap.
-- ------------------------------------------------------------

SELECT
    COUNT(DISTINCT o.order_id)      AS total_delivered_orders,
    COUNT(DISTINCT r.order_id)      AS orders_with_reviews,
    COUNT(DISTINCT o.order_id)
        - COUNT(DISTINCT r.order_id) AS orders_without_reviews
FROM olist_orders_dataset o
LEFT JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered';


-- ------------------------------------------------------------
-- SECTION 7: PRODUCT CATEGORY NULL CHECK
-- Some products are missing a category name.
-- This affects the category performance analysis.
-- ------------------------------------------------------------

SELECT
    COUNT(*)                                        AS total_products,
    SUM(CASE WHEN product_category_name IS NULL THEN 1 ELSE 0 END)
                                                    AS missing_category,
    ROUND(
        SUM(CASE WHEN product_category_name IS NULL THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2)                      AS pct_missing_category
FROM olist_products_dataset;
