# Data Inventory

## Dataset Overview
The Olist Brazilian E-Commerce Public Dataset contains transactional data from a Brazilian online marketplace covering customer orders, products, sellers, payments, reviews and logistics.

The dataset consists of nine related tables representing different stages of the customer purchasing journey.

---

| Table | Description | Role |
|---------|-------------|------|
| olist_orders_dataset | Customer orders | Core transactional table |
| olist_customers_dataset | Customer information | Dimension |
| olist_order_items_dataset | Products within each order | Transaction |
| olist_products_dataset | Product catalogue | Dimension |
| olist_order_payments_dataset | Payment information | Transaction |
| olist_order_reviews_dataset | Customer reviews | Transaction |
| olist_sellers_dataset | Seller information | Dimension |
| olist_geolocation_dataset | Geographic reference | Supporting |
| product_category_name_translation | Product category translation | Supporting |

## olist_orders_dataset

### Business Purpose

Represents the complete lifecycle of customer orders placed through the Olist marketplace, from purchase through delivery.

### Granularity

One row represents one customer order.

### Likely Primary Key

order_id

### Likely Foreign Key

customer_id

### Key Business Attributes

- Order status
- Purchase timestamp
- Approval timestamp
- Carrier dispatch date
- Customer delivery date
- Estimated delivery date

### Business Process

Customer places an order → Order approved → Carrier receives order → Customer receives order

### Potential Analytical Value

This table provides the foundation for analysing:

- Delivery performance
- Order fulfilment
- Operational efficiency
- Delivery delays
- Customer purchasing activity
