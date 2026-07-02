# Data Discovery Notes

## Objective
Before beginning any analysis, the first task was to understand how the business data is organised.

Rather than asking what insights could be produced, this phase focused on understanding what the dataset actually represents.

---

## Key Observations
- The Orders dataset appears to be the central transactional table.
- Most datasets reference an `order_id`, indicating that the customer order is the primary business event.
- The data represents the complete customer purchasing journey, from purchase through to delivery and customer review.
- Multiple timestamp fields provide opportunities to measure operational performance throughout the order lifecycle.

---

## Initial Hypotheses
The data may help investigate whether customer satisfaction is associated with:

- Delivery performance
- Order fulfilment
- Product categories
- Seller performance
- Geographic location

These hypotheses will be tested during later phases of the project.
