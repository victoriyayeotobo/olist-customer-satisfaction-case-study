# Chapter 4 — Developing Insights

## Objective

Having established that the Olist dataset is sufficiently complete and reliable for analysis, this chapter investigates the operational and commercial factors associated with customer satisfaction.

Each investigation is designed to answer a specific business question using evidence derived from SQL analysis. Rather than describing the data, the objective is to identify meaningful relationships that can support practical business recommendations.

---

## Investigations

- Investigation 1 — Does delivery performance influence customer satisfaction?
- Investigation 2 — Do product categories influence customer satisfaction?
- Investigation 3 — Does freight cost influence customer satisfaction?
- Investigation 4 — Do payment methods influence customer satisfaction?
- Investigation 5 — Are some sellers consistently associated with poor customer experiences?
  

## Investigation 1 — Does Delivery Performance Influence Customer Satisfaction?

### Business Question

Does the timing of delivery influence customer satisfaction?

### Why this matters

Delivery is one of the final stages of the customer journey and represents a critical touchpoint between the customer and the marketplace. Understanding whether delivery performance is associated with customer satisfaction can help prioritise operational improvements.

### Findings

Orders delivered ahead of schedule received the highest average customer review score (**4.30**).

Average review scores declined consistently as delivery delays increased.

Orders delivered more than seven days after the estimated delivery date received an average review score of just **1.70**, representing the lowest customer satisfaction across all delivery groups.

### Business Insight

A strong negative relationship exists between delivery delays and customer satisfaction.

Although this analysis does not establish causation, the consistent decline in review scores suggests that delivery performance is a significant operational factor associated with customer experience.

### Recommendation

Reduce delivery delays through improved logistics monitoring and proactive intervention for orders projected to exceed their estimated delivery date.

Improving delivery performance has the potential to improve overall customer satisfaction across the marketplace.


## Investigation 2 — Do Product Categories Influence Customer Satisfaction?

### Business Question

Do certain product categories consistently receive lower customer review scores than others?

### Why this matters

Understanding customer satisfaction at the product category level enables Olist to identify areas where quality issues, fulfilment challenges or customer expectations may differ across the marketplace.

### Findings

Customer satisfaction varies across product categories.

Office Furniture recorded the lowest average review score (3.52), followed by Men's Fashion (3.76), Fixed Telephony (3.76) and Audio (3.83).

Although some categories recorded relatively modest average review scores, high-volume categories such as Bed, Bath & Table generated a substantial number of negative reviews due to the scale of customer purchases.

### Business Insight

Customer satisfaction is not evenly distributed across product categories.

The results suggest that some categories experience consistently poorer customer experiences, while others contribute large volumes of dissatisfaction because of their popularity.

### Recommendation

Prioritise detailed investigation into categories with both low average review scores and high volumes of negative reviews.

Improving customer experience within high-volume categories may produce the greatest overall improvement in marketplace satisfaction.
