# Chapter 4 — Developing Insights

## Objective

Following the completion of the data quality assessment, this chapter investigates the operational and commercial factors associated with customer satisfaction across the Olist marketplace.

The analysis focuses on three areas where the available evidence can support practical business decisions:

1. Delivery performance
2. Product category performance
3. Seller performance

The purpose is not simply to describe customer ratings, but to understand where dissatisfaction is concentrated and identify areas where operational improvements may have the greatest effect.

---

## Investigation 1 — Does Delivery Performance Influence Customer Satisfaction?

### Business Question

Is delivery performance associated with customer review scores?

### Why This Matters

Delivery is one of the most visible stages of the customer journey. Delays may reduce customer confidence, affect their perception of the marketplace and lead to poorer reviews.

Understanding this relationship can help the Operations and Customer Experience teams determine whether delivery reliability should be treated as a priority area.

### Results

| Delivery Bracket | Orders | Average Review Score | Percentage of Orders |
|------------------|-------:|---------------------:|---------------------:|
| Arrived 3+ days early | 83,922 | 4.30 | 87.10% |
| Arrived on time or early | 6,022 | 4.11 | 6.25% |
| 1–3 days late | 1,856 | 3.29 | 1.93% |
| 4–7 days late | 1,756 | 2.10 | 1.82% |
| More than 7 days late | 2,797 | 1.70 | 2.90% |

### Finding

Average review scores declined consistently as delivery delays increased.

Orders arriving at least three days early received an average review score of **4.30**, while orders arriving more than seven days late received an average score of only **1.70**.

The largest decline occurred once deliveries exceeded the estimated date by more than three days.

### Business Interpretation

The results demonstrate a strong negative association between delivery delays and customer satisfaction.

Although the analysis does not prove that delays alone caused the poor reviews, the consistent decline across every delivery bracket suggests that delivery reliability is a major operational factor associated with the customer experience.

### Recommendation

Olist should prioritise orders predicted to exceed their estimated delivery dates, particularly where delays are expected to exceed three days.

Possible actions include:

- Introducing early-warning monitoring for at-risk orders
- Escalating repeated delays to the relevant sellers or logistics partners
- Providing proactive customer communication when delays are unavoidable
- Tracking late-delivery rates as a seller and logistics performance indicator

---

## Investigation 2 — Do Product Categories Influence Customer Satisfaction?

### Business Question

Are poor customer experiences concentrated within particular product categories?

### Why This Matters

Product categories may differ in product quality, fulfilment complexity, customer expectations and delivery requirements.

Understanding category-level performance can help the Product and Seller Success teams identify where further investigation or intervention may be required.

### Lowest-Rated Categories

| Product Category | Orders | Average Review Score | Negative Reviews | Negative Review Rate |
|------------------|-------:|---------------------:|-----------------:|---------------------:|
| Office Furniture | 1,244 | 3.52 | 423 | 25.42% |
| Fixed Telephony | 209 | 3.76 | 58 | 22.92% |
| Men's Fashion | 105 | 3.76 | 31 | 25.00% |
| Audio | 345 | 3.83 | 78 | 21.73% |
| Home Comfort | 390 | 3.85 | 85 | 19.77% |

### High-Volume Category Risk

Some categories did not record the lowest average ratings but generated large numbers of negative reviews because of their sales volume.

For example:

| Product Category | Orders | Average Review Score | Negative Reviews |
|------------------|-------:|---------------------:|-----------------:|
| Bed, Bath and Table | 9,177 | 3.92 | 2,011 |
| Furniture and Decoration | 6,260 | 3.95 | 1,484 |
| Computer Accessories | 6,499 | 3.98 | 1,312 |

### Finding

Customer satisfaction varies meaningfully across product categories.

Office Furniture recorded the lowest average review score and one of the highest negative-review rates. However, high-volume categories such as Bed, Bath and Table generated substantially more dissatisfied customers in absolute terms.

### Business Interpretation

Category performance should not be judged using average review scores alone.

Two different forms of risk are present:

1. **Performance risk:** categories with low average ratings and high negative-review rates
2. **Volume risk:** popular categories that generate large numbers of negative experiences despite having less severe average ratings

### Recommendation

Olist should use a combined category-prioritisation framework based on:

- Average review score
- Negative-review percentage
- Total number of negative reviews
- Order volume

Low-rated categories should be investigated for recurring product-quality, seller or fulfilment issues. High-volume categories should also be prioritised because small improvements could positively affect a large number of customers.

---

## Investigation 3 — Are Poor Customer Experiences Concentrated Among Particular Sellers?

### Business Question

Are some sellers consistently associated with poor customer satisfaction and delivery performance?

### Why This Matters

Olist operates as a marketplace connecting customers with independent sellers. Poor performance by a relatively small group of sellers can damage the customer experience and affect trust in the wider platform.

Seller-level analysis can help the Seller Success and Operations teams target interventions rather than applying broad marketplace-wide measures.

### Examples of Underperforming Sellers

| Seller Orders | Average Review Score | Negative Reviews | Late Delivery Rate |
|--------------:|---------------------:|-----------------:|-------------------:|
| 107 | 2.27 | 80 | 22.43% |
| 184 | 2.81 | 93 | 14.67% |
| 79 | 2.96 | 37 | 12.66% |
| 96 | 2.97 | 45 | 27.08% |
| 47 | 3.00 | 25 | 29.79% |

### Finding

Seller performance varies considerably across the marketplace.

Several sellers recorded average review scores below 3.00 alongside elevated late-delivery rates. The results also showed that revenue performance does not always correspond with a strong customer experience: some high-revenue sellers continued to record relatively weak review scores and substantial numbers of negative reviews.

### Business Interpretation

Customer dissatisfaction is not distributed evenly across all sellers.

This indicates that a targeted seller-management approach may be more effective than applying general interventions across the entire marketplace.

Seller performance should be assessed using a combination of:

- Average review score
- Negative-review volume
- Late-delivery rate
- Order volume
- Revenue contribution

### Recommendation

Olist should introduce a seller performance-monitoring framework that identifies sellers with repeated customer experience problems.

Possible interventions include:

- Seller performance scorecards
- Minimum service-level expectations
- Targeted logistics and fulfilment support
- Improvement plans for recurring underperformance
- Escalation or restriction for sellers that repeatedly fail to improve

High-revenue sellers should not be exempt from customer experience standards.

---

## Combined Insight

The evidence suggests that customer dissatisfaction is associated with three connected areas:

- Delivery delays
- Uneven performance across product categories
- Concentrated underperformance among particular sellers

Delivery appears to be the clearest operational factor. Review scores fall sharply once orders exceed their estimated delivery date, while category and seller results show where those poor experiences may be concentrated.

These findings suggest that Olist should avoid treating customer dissatisfaction as one general marketplace problem. A more effective response would combine delivery-risk monitoring, category prioritisation and targeted seller management.

---

## Recommended Business Priorities

### Priority 1 — Reduce Severe Delivery Delays

Focus on orders expected to exceed the estimated delivery date by more than three days.

### Priority 2 — Target High-Risk Product Categories

Prioritise categories using both negative-review rates and total negative-review volumes.

### Priority 3 — Introduce Seller Performance Monitoring

Identify sellers with consistently low review scores, high late-delivery rates and significant customer impact.

---

## Analytical Caveats

- The analysis identifies associations and does not establish direct causation.
- Review scores may reflect factors not available within the dataset, including product quality, product-description accuracy and customer support interactions.
- Category results may be influenced by differences in order volume.
- Seller comparisons should consider minimum order thresholds to avoid drawing conclusions from very small samples.
- Orders containing multiple items or sellers may require additional treatment during more detailed analysis.

---

## Next Step

The next stage will translate these findings into clear visuals, an executive dashboard and evidence-based recommendations for the final chapter.
