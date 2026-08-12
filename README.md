# Olist Customer Satisfaction Analytics Case Study

An end-to-end business analytics case study investigating the operational factors associated with customer satisfaction across the Olist Brazilian e-commerce marketplace.

Using SQL Server and Tableau, I connected customer reviews with delivery performance, product categories and seller activity to answer one central business question:

> **Where is customer dissatisfaction concentrated, what operational signals are associated with it, and where should the business focus its attention?**

---

## Project Overview

Customer review scores provide a useful measure of satisfaction, but an overall marketplace average does not explain why poor experiences occur or where management should intervene.

This project moves beyond reporting customer ratings by investigating three operational areas:

- Delivery performance
- Product category risk
- Seller performance

The analysis follows a five-chapter workflow, progressing from business understanding and data validation to insight development, dashboard design and evidence-based recommendations.

---

## Executive Summary

The analysis identified three major findings.

### 1. Delivery reliability showed the strongest satisfaction pattern

Customer review scores declined progressively as delivery delays increased.

| Delivery Performance | Avg. Review Score |
|---|---:|
| Arrived 3+ days early | **4.30** |
| Arrived on time / early | **4.11** |
| 1–3 days late | **3.29** |
| 4–7 days late | **2.10** |
| 7+ days late | **1.70** |

Orders arriving seven or more days late averaged only **1.70/5**, compared with **4.30/5** among orders arriving at least three days early.

This was the strongest operational customer-satisfaction signal identified in the analysis.

### 2. Product category risk depends on severity and scale

The categories with the highest negative-review percentages were not always responsible for the greatest number of poor customer experiences.

For example, `fashion_roupa_masculina` recorded a **25.00% negative-review rate across 105 orders**, while `cama_mesa_banho` recorded an **18.31% negative-review rate across 9,177 orders**, generating **2,011 negative reviews**.

This demonstrated why category prioritisation should consider both the **severity of dissatisfaction and the number of customers affected**.

### 3. Marketplace averages can conceal seller-level risk

Seller-level analysis revealed meaningful variation in customer satisfaction and delivery reliability.

To reduce the influence of very small transaction histories, the main seller comparison included sellers with at least **30 delivered orders** and evaluated performance using:

- Average review score
- Negative reviews
- Late-delivery rate
- Order volume
- Revenue

This provided a more balanced view of seller risk than ranking sellers using review score alone.

---

## Executive KPIs

The final executive analysis produced the following marketplace-level indicators:

| KPI | Result |
|---|---:|
| Delivered Orders | **95,824** |
| Overall Average Review Score | **4.08 / 5** |
| GMV | **R$15.36M** |
| Late Delivery Rate | **8.93%** |
| Negative Review Rate | **14.79%** |
| Average Freight Cost | **R$19.93** |

These KPIs provide overall marketplace context. The deeper analysis identifies where customer experience differs beneath those averages.

---

## Executive Dashboard

The final Tableau dashboard brings together marketplace KPIs and the three major analytical views:

- Delivery Performance
- Product Category Risk
- Seller Performance

The dashboard was designed as a decision-support tool rather than a collection of every chart produced during the analysis.

**Dashboard preview available in the `Images` and `dashboard` folders.**

---

## Business Recommendations

### 1. Protect the Delivery Promise

Treat delivery reliability against the promised delivery date as a core customer-experience KPI.

Rather than monitoring only the overall late-delivery percentage, Olist should identify persistent and severe delivery underperformance and investigate where orders repeatedly fail to meet customer expectations.

### 2. Introduce a Category Risk Watchlist

Prioritise product categories using a combination of:

- Negative-review rate
- Negative-review volume
- Average review score
- Order volume

This prevents small categories with extreme percentages from automatically receiving greater attention than high-volume categories affecting substantially more customers.

### 3. Build a Multi-Metric Seller Monitoring Framework

Monitor sellers using customer satisfaction, delivery reliability, transaction volume and commercial context.

A practical intervention framework could move sellers through:

**Monitor → Review → Intervention**

depending on the persistence and severity of their performance indicators.

---

## Case Study Structure

| Chapter | Focus | Status |
|---|---|---|
| Chapter 1 | Business Understanding | ✅ Complete |
| Chapter 2 | Understanding the Data Landscape | ✅ Complete |
| Chapter 3 | Exploring and Validating the Evidence | ✅ Complete |
| Chapter 4 | Developing the Insights | ✅ Complete |
| Chapter 5 | From Insight to Business Action | ✅ Complete |

---

## Project Methodology

![Project Roadmap](Images/Analytics%20Case%20Study%20Roadmap.png)

The project followed a structured analytical process:

**Business Problem → Data Understanding → Data Validation → Evidence → Insight → Decision Support**

Each stage built on evidence established during the previous stage so that the final recommendations could be traced back to validated analytical findings.

---

## Chapter 1: Business Understanding

### Objective

Define the customer-satisfaction problem before beginning technical analysis.

Rather than starting with available columns and asking what could be calculated, the project began by identifying the business decisions the analysis needed to support.

### Deliverables

- Business problem definition
- Stakeholder analysis
- Business question matrix
- Analytical scope
- Success criteria

### Outcome

The business problem was translated into three analytical areas: delivery performance, product category risk and seller performance.

---

## Chapter 2: Understanding the Data Landscape

### Objective

Understand how the Olist relational datasets represent the customer journey and establish the relationships required for analysis.

### Deliverables

- Data inventory
- Data discovery notes
- Relationship mapping
- Table-grain assessment
- Initial KPI framework

### Outcome

Orders were connected with reviews, delivery information, products and sellers, establishing the analytical structure required to investigate customer satisfaction without distorting metrics through incorrect joins or aggregation.

---

## Chapter 3: Exploring and Validating the Evidence

### Objective

Determine whether the underlying data was sufficiently reliable for the planned customer-satisfaction analysis.

### Validation Work

- Core table row-count validation
- Order-status assessment
- Historical date-range validation
- Missing delivery-date investigation
- Customer-review assessment
- Review-coverage validation
- Product-category completeness assessment
- SQL import and datatype validation

### Key Validation Finding

Most missing actual-delivery dates were associated with orders that had not completed the delivery lifecycle.

Only **8 orders classified as delivered** were missing an actual-delivery timestamp.

This demonstrated why missing values needed to be investigated in business context rather than automatically treated as data-quality failures.

### Outcome

The dataset was considered sufficiently complete and internally consistent for the planned analysis, provided the documented filtering rules and limitations were respected.

---

## Chapter 4: Developing the Insights

### Objective

Identify operational and commercial patterns associated with customer satisfaction.

### Analysis Completed

- Delivery performance analysis
- Product category risk analysis
- Seller performance analysis
- Volume-adjusted risk assessment

### Key Findings

**Delivery:** Average review score declined from **4.30 to 1.70** as delivery performance moved from significantly early to seven or more days late.

**Categories:** Business risk depended on both dissatisfaction rate and transaction volume.

**Sellers:** Marketplace averages concealed seller-level variation, making multi-metric seller analysis necessary.

### Outcome

The analysis established three evidence-based priorities that could be translated into management action.

---

## Chapter 5: From Insight to Business Action

### Objective

Translate the analytical findings into a practical decision-support framework.

### Deliverables

- Executive KPI summary
- Final Tableau dashboard
- Delivery reliability recommendation
- Category Risk Watchlist
- Seller monitoring framework
- Implementation priorities
- Limitations and responsible interpretation
- Final case study conclusion

### Outcome

The completed analysis recommends that Olist:

1. **Protect the delivery promise**
2. **Prioritise category risk using severity and scale**
3. **Monitor sellers using multiple operational and customer-experience indicators**

---

## Data Quality and Analytical Decisions

Several decisions were made to preserve the meaning of the source data and reduce the risk of misleading conclusions.

- Missing delivery dates were investigated by order status before exclusion.
- Missing reviews were not converted into assumed satisfaction scores.
- Unknown product categories were not assigned invented classifications.
- Table grain was considered during joins and aggregation.
- Delivery analysis required valid delivery timestamps.
- Seller comparisons used a minimum transaction threshold to reduce small-sample distortion.

The guiding principle throughout the project was:

> **No conclusion should be presented unless it can be supported by evidence from the data.**

---

## Tools Used

| Tool | Application |
|---|---|
| **SQL Server** | Database creation, data validation, relational analysis and KPI development |
| **Tableau Public** | Executive dashboard development and data visualisation |
| **Excel / CSV** | Transfer of aggregated analytical outputs where required |
| **GitHub** | Project documentation, SQL organisation and portfolio presentation |

---

## Repository Structure

| Folder | Purpose |
|---|---|
| `Data` | Project data and analytical extracts |
| `Images` | Roadmap, analysis visuals and dashboard images |
| `dashboard` | Tableau dashboard assets |
| `docs` | Complete case study and project documentation |
| `notebooks` | Supporting analytical work |
| `sql` | Data validation, business analysis and KPI queries |

---

## Limitations

The dataset represents historical marketplace activity from **2016 to 2018**. The findings should therefore be interpreted as patterns within the historical Olist dataset rather than claims about Olist's current performance.

The analysis is observational. Relationships identified between operational measures and review scores should not automatically be interpreted as causal.

Review scores may also reflect several parts of the customer experience that cannot be completely isolated using the available data.

---

## Key Takeaway

The strongest conclusion from this project is not simply that late orders receive lower ratings.

The broader finding is that **customer dissatisfaction leaves operational signals that can be identified before they disappear inside marketplace averages**.

Delivery reliability provides the strongest customer-experience signal identified in this analysis. Category volume provides the context needed to prioritise dissatisfaction intelligently. Seller-level monitoring provides a way to locate operational risk more precisely.

Together, these findings provide a framework for moving from:

**measuring customer satisfaction after the fact**

to

**using customer and operational data to identify where improvement should begin.**

---

## Project Deliverables

This repository contains:

- Complete five-chapter analytics case study
- SQL data-quality and validation queries
- Delivery-performance analysis
- Product-category risk analysis
- Seller-performance analysis
- Executive KPI calculations
- Tableau dashboard assets
- Supporting project visuals

---

## About This Project

This portfolio project demonstrates an end-to-end business analytics workflow:

**Business Understanding → Data Validation → SQL Analysis → Data Visualisation → Business Recommendations**

The emphasis is not only on writing technically correct queries or producing visualisations, but on translating analytical evidence into clear, defensible business decisions.
