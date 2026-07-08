-- =============================================================================
-- OLIST E-COMMERCE | BUSINESS QUESTIONS — SQL EXPLORATION
-- Analyst: Victor Otobo
-- Purpose: Answer the core business questions that will feed into
--          the Python analysis and executive summary.
--          Each query maps to a specific stakeholder question.
-- =============================================================================


-- ------------------------------------------------------------
-- BQ-01: DOES LATE DELIVERY CAUSE POOR REVIEWS?
-- Stakeholder: Customer Experience Team, COO
-- Finding will become the headline insight of this project.
-- ------------------------------------------------------------

SELECT
    CASE
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) < -3  THEN '1. Arrived 3+ days early'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN -3 AND 0
                                                        THEN '2. Arrived on time / early'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN 1 AND 3
                                                        THEN '3. 1–3 days late'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN 4 AND 7
                                                        THEN '4. 4–7 days late'
        ELSE                                                 '5. 7+ days late'
    END                                             AS delivery_bracket,

    COUNT(*)                                        AS order_count,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2)   AS avg_review_score,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_orders

FROM olist_orders_dataset o
INNER JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY
    CASE
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) < -3  THEN '1. Arrived 3+ days early'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN -3 AND 0
                                                        THEN '2. Arrived on time / early'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN 1 AND 3
                                                        THEN '3. 1–3 days late'
        WHEN DATEDIFF(DAY,
                o.order_estimated_delivery_date,
                o.order_delivered_customer_date) BETWEEN 4 AND 7
                                                        THEN '4. 4–7 days late'
        ELSE                                                 '5. 7+ days late'
    END
ORDER BY delivery_bracket;


-- ------------------------------------------------------------
-- BQ-02: WHICH PRODUCT CATEGORIES HAVE THE WORST REVIEWS?
-- Stakeholder: Product Team, Seller Success Team
-- Identifies where satisfaction problems are concentrated.
-- ------------------------------------------------------------

SELECT
    COALESCE(p.product_category_name, 'Unknown')   AS category,
    COUNT(DISTINCT oi.order_id)                    AS order_count,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2)   AS avg_review_score,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END)
                                                   AS negative_review_count,
    ROUND(
        SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2)                             AS pct_negative_reviews

FROM olist_order_items_dataset oi
INNER JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
INNER JOIN olist_order_reviews_dataset r
    ON oi.order_id = r.order_id
INNER JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id
WHERE
    o.order_status = 'delivered'

GROUP BY
    COALESCE(p.product_category_name, 'Unknown')

HAVING COUNT(DISTINCT oi.order_id) >= 50   -- Exclude low-volume categories
ORDER BY avg_review_score ASC;


-- ------------------------------------------------------------
-- BQ-03: WHICH SELLERS ARE CONSISTENTLY UNDERPERFORMING?
-- Stakeholder: Seller Success Team
-- Identifies at-risk sellers before they damage platform reputation.
-- ------------------------------------------------------------

SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id)                    AS total_orders,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2)   AS avg_review_score,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END)
                                                   AS negative_reviews,
    ROUND(SUM(oi.price), 2)                        AS total_revenue_brl,

    -- Late delivery rate for this seller
    ROUND(
        SUM(CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 1 ELSE 0 END) * 100.0
        / COUNT(DISTINCT oi.order_id), 2)          AS late_delivery_rate_pct

FROM olist_sellers_dataset s
INNER JOIN olist_order_items_dataset oi
    ON s.seller_id = oi.seller_id
INNER JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id
INNER JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL

GROUP BY
    s.seller_id, s.seller_city, s.seller_state

HAVING COUNT(DISTINCT oi.order_id) >= 30   -- Minimum volume for reliability

ORDER BY avg_review_score ASC, total_orders DESC;


-- ------------------------------------------------------------
-- BQ-04: WHICH STATES HAVE THE WORST DELIVERY PERFORMANCE?
-- Stakeholder: Operations Team, Logistics
-- Pinpoints where logistics investment is most needed.
-- ------------------------------------------------------------

SELECT
    c.customer_state                               AS state,
    COUNT(DISTINCT o.order_id)                     AS total_orders,

    ROUND(AVG(
        DATEDIFF(DAY,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date)
    ), 1)                                          AS avg_actual_delivery_days,

    ROUND(AVG(
        DATEDIFF(DAY,
            o.order_purchase_timestamp,
            o.order_estimated_delivery_date)
    ), 1)                                          AS avg_estimated_delivery_days,

    ROUND(
        SUM(CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2)                             AS late_delivery_rate_pct,

    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2)   AS avg_review_score

FROM olist_orders_dataset o
INNER JOIN olist_customers_dataset c
    ON o.customer_id = c.customer_id
INNER JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL

GROUP BY c.customer_state
ORDER BY late_delivery_rate_pct DESC;


-- ------------------------------------------------------------
-- BQ-05: OVERALL PLATFORM KPIs — EXECUTIVE SUMMARY INPUTS
-- Stakeholder: COO, CFO, Executive Leadership
-- These numbers appear in the Executive Summary section.
-- ------------------------------------------------------------

SELECT
    COUNT(DISTINCT o.order_id)                     AS total_delivered_orders,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2)   AS overall_avg_review_score,
    ROUND(SUM(oi.price + oi.freight_value), 2)     AS total_gmv_brl,

    -- Late delivery rate
    ROUND(
        SUM(CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 1 ELSE 0 END) * 100.0
        / COUNT(DISTINCT o.order_id), 2)           AS platform_late_delivery_pct,

    -- % of orders with negative review
    ROUND(
        SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2)                             AS pct_negative_reviews,

    -- Average freight cost
    ROUND(AVG(oi.freight_value), 2)                AS avg_freight_cost_brl

FROM olist_orders_dataset o
INNER JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
INNER JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL;


-- ------------------------------------------------------------
-- BQ-06: QUARTERLY TREND — REVIEW SCORES OVER TIME
-- Stakeholder: COO, Customer Experience
-- Shows whether satisfaction is improving or worsening.
-- This feeds the trend line in the Executive dashboard page.
-- ------------------------------------------------------------

SELECT
    YEAR(o.order_purchase_timestamp)               AS order_year,
    DATEPART(QUARTER, o.order_purchase_timestamp)  AS order_quarter,
    COUNT(DISTINCT o.order_id)                     AS order_count,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 3)   AS avg_review_score,
    ROUND(
        SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2)                             AS pct_negative_reviews,
    ROUND(
        SUM(CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 1 ELSE 0 END) * 100.0
        / COUNT(DISTINCT o.order_id), 2)           AS late_delivery_rate_pct

FROM olist_orders_dataset o
INNER JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL

GROUP BY
    YEAR(o.order_purchase_timestamp),
    DATEPART(QUARTER, o.order_purchase_timestamp)

ORDER BY order_year, order_quarter;
