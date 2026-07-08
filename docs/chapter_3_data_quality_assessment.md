# Chapter 3 — Assessing Data Quality

## Objective

Before beginning exploratory analysis, the Olist dataset was assessed to determine whether it was sufficiently complete, reliable and representative to support an investigation into customer satisfaction.

Rather than assuming the data was ready for analysis, a structured validation process was carried out to assess its completeness, consistency and overall suitability. This ensured that any future findings would be supported by trustworthy data rather than assumptions.

---

# Dataset Overview

The first step was to confirm that all expected datasets had been successfully imported into SQL Server.

| Dataset | Records |
|---------|---------:|
| Orders | 99,441 |
| Order Items | 112,650 |
| Customers | 99,441 |
| Products | 32,951 |
| Sellers | 3,095 |
| Reviews | 99,224 |
| Payments | 103,886 |
| Geolocation | 1,000,163 |

### Observation

The relationships between table sizes were consistent with the expected structure of an e-commerce platform. For example, the Order Items table contains more records than the Orders table, confirming that a single order may contain multiple products.

---

# Order Status Validation

Order status distribution was examined before analysing customer satisfaction.

| Order Status | Orders | Percentage |
|--------------|-------:|-----------:|
| Delivered | 96,478 | 97.02% |
| Shipped | 1,107 | 1.11% |
| Cancelled | 625 | 0.63% |
| Unavailable | 609 | 0.61% |
| Invoiced | 314 | 0.32% |
| Processing | 301 | 0.30% |
| Created | 5 | 0.01% |
| Approved | 2 | <0.01% |

### Observation

Approximately 97% of all orders were successfully delivered, indicating that the dataset is largely composed of completed customer journeys and is suitable for customer experience analysis.

---

# Historical Coverage

The dataset covers the period between **4 September 2016** and **17 October 2018**, representing approximately **773 days** of marketplace activity.

### Observation

The data spans more than two years, providing sufficient historical coverage to investigate customer behaviour and operational performance over time.

---

# Missing Values Investigation

Initial validation identified **2,965** orders without a customer delivery date.

Rather than treating these as data quality issues, a follow-up investigation was performed.

| Order Status | Missing Delivery Dates |
|--------------|----------------------:|
| Shipped | 1,107 |
| Cancelled | 619 |
| Unavailable | 609 |
| Invoiced | 314 |
| Processing | 301 |
| Delivered | 8 |
| Created | 5 |
| Approved | 2 |

### Observation

The missing delivery dates were largely explained by legitimate business processes. Orders that had not completed the delivery lifecycle would not be expected to contain a delivery timestamp.

Only eight delivered orders were missing a delivery date, representing a negligible proportion of the dataset.

---

# Customer Review Assessment

Customer review scores were assessed before investigating the factors influencing customer satisfaction.

| Review Score | Reviews | Percentage |
|-------------|--------:|-----------:|
| ⭐ 1 | 11,424 | 11.51% |
| ⭐ 2 | 3,151 | 3.18% |
| ⭐ 3 | 8,179 | 8.24% |
| ⭐ 4 | 19,142 | 19.29% |
| ⭐ 5 | 57,328 | 57.78% |

### Observation

Customer satisfaction appears generally positive, with almost 58% of customers awarding the highest possible rating.

However, approximately 15% of customers provided ratings of one or two stars, creating a meaningful opportunity to investigate the factors associated with poor customer experiences.

---

# Review Coverage

A comparison between delivered orders and customer reviews showed:

| Metric | Value |
|--------|------:|
| Delivered Orders | 96,478 |
| Orders With Reviews | 95,832 |
| Orders Without Reviews | 646 |

### Observation

More than 99% of delivered orders have an associated customer review, providing confidence that the review data is highly representative of completed customer experiences.

---

# Product Category Completeness

| Metric | Value |
|--------|------:|
| Products | 32,951 |
| Missing Categories | 610 |
| Missing (%) | 1.85% |

### Observation

More than 98% of products have an assigned category, making the dataset suitable for category-level analysis.

---

# SQL Import Challenges

During the SQL Server import process, some datasets required manual adjustment of automatically assigned data types before they could be imported successfully.

For example, certain numeric fields initially assigned smaller numeric data types were updated to more appropriate types (such as `INT` and `FLOAT`) to accommodate the values contained within the dataset.

Although this formed part of the data preparation stage rather than the analysis itself, documenting these changes improves the reproducibility of the project and reflects the practical challenges encountered when preparing real-world datasets.

---

# Overall Assessment

The data quality assessment confirmed that the Olist dataset is suitable for exploratory analysis.

No significant issues were identified that would prevent meaningful investigation of customer satisfaction.

Minor limitations were documented and will be considered during the analytical phase of the project.

The next chapter will begin exploring the operational and commercial factors that influence customer satisfaction using SQL and Python.
