# =============================================================================
# OLIST E-COMMERCE | CUSTOMER SATISFACTION ANALYSIS
# Analyst: Victor Otobo
# Dataset: Brazilian E-Commerce Public Dataset by Olist (Kaggle)
# Objective: Identify the primary drivers of customer dissatisfaction and
#            produce prioritised recommendations for leadership.
# =============================================================================
# NOTEBOOK STRUCTURE
#   0. Setup & Imports
#   1. Data Loading & Merge
#   2. Data Quality & Caveats
#   3. KPI Definition
#   4. Delivery Performance Analysis        [Key Finding 1]
#   5. Product Category Analysis            [Key Finding 2]
#   6. Seller Performance Analysis          [Key Finding 3]
#   7. Regional Analysis                    [Key Finding 4]
#   8. Key Driver Summary
#   9. Export for Dashboard
# =============================================================================


# ── 0. SETUP & IMPORTS ───────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Visual style ──────────────────────────────────────────────────────────────
OLIST_GREEN  = "#00B37E"
OLIST_DARK   = "#1A1A2E"
OLIST_GREY   = "#6B7280"
OLIST_RED    = "#EF4444"
OLIST_AMBER  = "#F59E0B"
OLIST_BLUE   = "#3B82F6"
OLIST_LIGHT  = "#F9FAFB"

plt.rcParams.update({
    "figure.facecolor":  OLIST_LIGHT,
    "axes.facecolor":    OLIST_LIGHT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.labelcolor":   OLIST_DARK,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "font.family":       "DejaVu Sans",
    "text.color":        OLIST_DARK,
})

FIGSIZE_WIDE  = (12, 5)
FIGSIZE_TALL  = (10, 7)
FIGSIZE_SMALL = (8, 4)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(name):
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{name}.png", dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  ✓ Saved: {name}.png")


# ── 1. DATA LOADING & MERGE ──────────────────────────────────────────────────
# Adjust DATA_DIR to the folder where you extracted the Kaggle CSVs.

DATA_DIR = "data/"

orders    = pd.read_csv(DATA_DIR + "olist_orders_dataset.csv",
                        parse_dates=["order_purchase_timestamp",
                                     "order_approved_at",
                                     "order_delivered_carrier_date",
                                     "order_delivered_customer_date",
                                     "order_estimated_delivery_date"])

items     = pd.read_csv(DATA_DIR + "olist_order_items_dataset.csv")
customers = pd.read_csv(DATA_DIR + "olist_customers_dataset.csv")
products  = pd.read_csv(DATA_DIR + "olist_products_dataset.csv")
sellers   = pd.read_csv(DATA_DIR + "olist_sellers_dataset.csv")
reviews   = pd.read_csv(DATA_DIR + "olist_order_reviews_dataset.csv",
                        parse_dates=["review_creation_date",
                                     "review_answer_timestamp"])
payments  = pd.read_csv(DATA_DIR + "olist_order_payments_dataset.csv")
category_trans = pd.read_csv(DATA_DIR + "product_category_name_translation.csv")

print("Tables loaded:")
for name, df in [("orders", orders), ("items", items), ("customers", customers),
                  ("products", products), ("sellers", sellers),
                  ("reviews", reviews), ("payments", payments)]:
    print(f"  {name:<12} {len(df):>7,} rows | {df.shape[1]} cols")


# ── Build master analytical table ────────────────────────────────────────────

# Translate category names to English
products = products.merge(category_trans, on="product_category_name", how="left")
products["category_en"] = products["product_category_name_english"].fillna("Unknown")

# One review per order (take max score if duplicates exist)
reviews_dedup = reviews.sort_values("review_score", ascending=False)\
                        .drop_duplicates("order_id", keep="first")

# Aggregate items to order level
items_agg = items.groupby("order_id").agg(
    total_items        = ("order_item_id", "count"),
    total_price        = ("price", "sum"),
    total_freight      = ("freight_value", "sum"),
    unique_sellers     = ("seller_id", "nunique"),
    primary_seller_id  = ("seller_id", "first"),
    primary_product_id = ("product_id", "first"),
).reset_index()

# Master table
df = (orders
      .query("order_status == 'delivered'")
      .merge(reviews_dedup[["order_id", "review_score", "review_comment_message"]],
             on="order_id", how="inner")
      .merge(items_agg,       on="order_id", how="left")
      .merge(customers[["customer_id","customer_city","customer_state"]],
             on="customer_id", how="left")
      .merge(sellers[["seller_id","seller_city","seller_state"]],
             left_on="primary_seller_id", right_on="seller_id", how="left")
      .merge(products[["product_id","category_en"]],
             left_on="primary_product_id", right_on="product_id", how="left")
     )

print(f"\nMaster table: {len(df):,} rows")


# ── 2. DATA QUALITY & CAVEATS ────────────────────────────────────────────────

print("\n── DATA QUALITY REPORT ──────────────────────────────────────────────")

# Delivery timestamp completeness
ts_missing = df["order_delivered_customer_date"].isna().sum()
print(f"  Missing actual delivery date : {ts_missing:,}  ({ts_missing/len(df):.1%}) — excluded from delivery analysis")

# Estimated delivery completeness
est_missing = df["order_estimated_delivery_date"].isna().sum()
print(f"  Missing estimated delivery   : {est_missing:,}")

# Category completeness
cat_missing = (df["category_en"] == "Unknown").sum()
print(f"  Unknown product category     : {cat_missing:,}  ({cat_missing/len(df):.1%})")

# Date range
print(f"\n  Order date range: {df['order_purchase_timestamp'].min().date()} "
      f"→ {df['order_purchase_timestamp'].max().date()}")
print(f"  Total delivered orders with reviews: {len(df):,}")


# ── 3. KPI DEFINITIONS ───────────────────────────────────────────────────────

# Delivery delta: negative = early, positive = late
df_delivery = df.dropna(subset=["order_delivered_customer_date",
                                  "order_estimated_delivery_date"]).copy()

df_delivery["delivery_delta"] = (
    df_delivery["order_delivered_customer_date"]
    - df_delivery["order_estimated_delivery_date"]
).dt.days

df_delivery["is_late"] = df_delivery["delivery_delta"] > 0

df_delivery["delivery_bracket"] = pd.cut(
    df_delivery["delivery_delta"],
    bins    = [-999, -4, 0, 3, 7, 999],
    labels  = ["3+ days early", "On time / early", "1–3 days late",
               "4–7 days late", "7+ days late"]
)

df_delivery["actual_delivery_days"] = (
    df_delivery["order_delivered_customer_date"]
    - df_delivery["order_purchase_timestamp"]
).dt.days

# Platform-level KPIs
kpi_overall_score      = df["review_score"].mean()
kpi_late_rate          = df_delivery["is_late"].mean()
kpi_negative_rate      = (df["review_score"] <= 2).mean()
kpi_five_star_rate     = (df["review_score"] == 5).mean()
kpi_total_gmv          = (df["total_price"].fillna(0) + df["total_freight"].fillna(0)).sum()

print(f"\n── PLATFORM KPIs ─────────────────────────────────────────────────────")
print(f"  Overall avg review score   : {kpi_overall_score:.2f} / 5.0")
print(f"  Late delivery rate         : {kpi_late_rate:.1%}")
print(f"  Negative review rate (≤2)  : {kpi_negative_rate:.1%}")
print(f"  5-star review rate         : {kpi_five_star_rate:.1%}")
print(f"  Total GMV (BRL)            : R$ {kpi_total_gmv:,.0f}")


# ── 4. DELIVERY PERFORMANCE ANALYSIS — KEY FINDING 1 ────────────────────────

print("\n\n═══════════════════════════════════════════════════════════════════════")
print("  FINDING 1 — LATE DELIVERY IS THE #1 DRIVER OF POOR REVIEWS")
print("═══════════════════════════════════════════════════════════════════════")

bracket_summary = (df_delivery
    .groupby("delivery_bracket", observed=True)
    .agg(
        order_count   = ("order_id",     "count"),
        avg_score     = ("review_score", "mean"),
        pct_negative  = ("review_score", lambda x: (x <= 2).mean()),
    )
    .round(3)
)
bracket_summary["pct_of_orders"] = bracket_summary["order_count"] / bracket_summary["order_count"].sum()
print(bracket_summary.to_string())

# Headline number
late_7plus = df_delivery[df_delivery["delivery_bracket"] == "7+ days late"]
ontime     = df_delivery[df_delivery["delivery_bracket"] == "On time / early"]
print(f"\n  ★ Orders 7+ days late     → avg score: {late_7plus['review_score'].mean():.2f}")
print(f"  ★ Orders on time / early  → avg score: {ontime['review_score'].mean():.2f}")
print(f"  ★ Score gap               : {ontime['review_score'].mean() - late_7plus['review_score'].mean():.2f} points")


# ── Chart 1: Average review score by delivery bracket ────────────────────────

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

# Left: avg score by bracket
brackets = bracket_summary.index.tolist()
scores   = bracket_summary["avg_score"].values
colors   = [OLIST_GREEN if s >= 4.0 else OLIST_AMBER if s >= 3.0 else OLIST_RED for s in scores]

bars = axes[0].bar(brackets, scores, color=colors, width=0.6, edgecolor="white", linewidth=0.8)
axes[0].set_ylim(1, 5.2)
axes[0].axhline(kpi_overall_score, color=OLIST_GREY, linestyle="--", linewidth=1, alpha=0.6)
axes[0].text(4.5, kpi_overall_score + 0.08, f"Platform avg: {kpi_overall_score:.2f}",
             fontsize=8, color=OLIST_GREY)
for bar, score in zip(bars, scores):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{score:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
axes[0].set_title("Avg Review Score by Delivery Timing")
axes[0].set_ylabel("Average Review Score (1–5)")
axes[0].set_xlabel("")
axes[0].tick_params(axis='x', rotation=15)

# Right: % negative reviews by bracket
neg_rates = (bracket_summary["pct_negative"] * 100).values
bars2 = axes[1].bar(brackets, neg_rates, color=colors, width=0.6, edgecolor="white", linewidth=0.8)
for bar, rate in zip(bars2, neg_rates):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{rate:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
axes[1].set_title("% Negative Reviews (Score ≤ 2) by Delivery Timing")
axes[1].set_ylabel("% Negative Reviews")
axes[1].tick_params(axis='x', rotation=15)

legend_patches = [
    mpatches.Patch(color=OLIST_GREEN, label="Score ≥ 4.0 (Healthy)"),
    mpatches.Patch(color=OLIST_AMBER, label="Score 3.0–3.9 (Watch)"),
    mpatches.Patch(color=OLIST_RED,   label="Score < 3.0 (Critical)"),
]
fig.legend(handles=legend_patches, loc="lower center", ncol=3, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.05))

fig.suptitle("Finding 1: Delivery timing is the strongest predictor of review score",
             fontsize=14, fontweight="bold", y=1.02)

save("finding1_delivery_vs_reviews")


# ── Chart 2: Delivery delta distribution ─────────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)
ax.hist(df_delivery["delivery_delta"].clip(-15, 30), bins=50,
        color=OLIST_BLUE, alpha=0.75, edgecolor="white", linewidth=0.4)
ax.axvline(0, color=OLIST_RED, linewidth=1.5, linestyle="--", label="Estimated date")
ax.axvline(df_delivery["delivery_delta"].median(), color=OLIST_GREEN,
           linewidth=1.5, linestyle="-", label=f"Median ({df_delivery['delivery_delta'].median():.0f} days)")
ax.set_xlabel("Days vs Estimated Delivery (negative = early)")
ax.set_ylabel("Number of Orders")
ax.set_title("Distribution of Delivery Delta\n(Most orders arrive before estimated date)")
ax.legend(frameon=False, fontsize=9)
save("finding1_delivery_delta_distribution")


# ── 5. PRODUCT CATEGORY ANALYSIS — KEY FINDING 2 ────────────────────────────

print("\n\n═══════════════════════════════════════════════════════════════════════")
print("  FINDING 2 — HIGH-VOLUME CATEGORIES WITH LOW SCORES = HIGHEST RISK")
print("═══════════════════════════════════════════════════════════════════════")

cat_summary = (df
    .groupby("category_en")
    .agg(
        order_count  = ("order_id",     "count"),
        avg_score    = ("review_score", "mean"),
        pct_negative = ("review_score", lambda x: (x <= 2).mean()),
    )
    .query("order_count >= 50")
    .round(3)
    .sort_values("avg_score")
)

print("\n  Bottom 10 categories by avg review score:")
print(cat_summary.head(10).to_string())
print("\n  Top 10 categories by avg review score:")
print(cat_summary.tail(10).to_string())


# ── Chart 3: Volume vs Score scatter (the priority quadrant chart) ────────────

fig, ax = plt.subplots(figsize=(11, 7))

scatter = ax.scatter(
    cat_summary["order_count"],
    cat_summary["avg_score"],
    s       = cat_summary["pct_negative"] * 2000,
    c       = cat_summary["avg_score"],
    cmap    = "RdYlGn",
    alpha   = 0.75,
    edgecolors = "white",
    linewidths = 0.8,
    vmin=3.0, vmax=4.8
)

# Quadrant lines
median_vol   = cat_summary["order_count"].median()
platform_avg = cat_summary["avg_score"].mean()
ax.axvline(median_vol,   color=OLIST_GREY, linestyle="--", linewidth=0.8, alpha=0.5)
ax.axhline(platform_avg, color=OLIST_GREY, linestyle="--", linewidth=0.8, alpha=0.5)

# Quadrant labels
ax.text(cat_summary["order_count"].max() * 0.85, 3.1,
        "⚠ HIGH PRIORITY\nHigh volume, low score", fontsize=8,
        color=OLIST_RED, ha="center", fontweight="bold")
ax.text(cat_summary["order_count"].max() * 0.85, 4.7,
        "✓ MAINTAIN\nHigh volume, good score", fontsize=8,
        color=OLIST_GREEN, ha="center")

# Label worst-performing high-volume categories
worst = cat_summary.query("order_count > @median_vol and avg_score < @platform_avg").head(6)
for _, row in worst.iterrows():
    ax.annotate(row.name,
                xy=(row["order_count"], row["avg_score"]),
                xytext=(8, 6), textcoords="offset points",
                fontsize=7.5, color=OLIST_DARK,
                arrowprops=dict(arrowstyle="-", color=OLIST_GREY, lw=0.5))

cbar = plt.colorbar(scatter, ax=ax, shrink=0.6)
cbar.set_label("Avg Review Score", fontsize=9)

ax.set_xlabel("Order Volume (orders in dataset)")
ax.set_ylabel("Average Review Score")
ax.set_title("Finding 2: Product Category Risk Matrix\n"
             "Bubble size = % negative reviews. Top-right = high volume & high score (ideal).",
             fontsize=13)

save("finding2_category_risk_matrix")


# ── Chart 4: Bottom 10 categories bar chart ───────────────────────────────────

bottom10 = cat_summary.head(10).sort_values("avg_score")

fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)
colors_b10 = [OLIST_RED if s < 3.5 else OLIST_AMBER for s in bottom10["avg_score"]]
bars = ax.barh(bottom10.index, bottom10["avg_score"], color=colors_b10,
               edgecolor="white", linewidth=0.6)
ax.axvline(kpi_overall_score, color=OLIST_GREEN, linestyle="--",
           linewidth=1.2, label=f"Platform avg: {kpi_overall_score:.2f}")
for bar, val in zip(bars, bottom10["avg_score"]):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            f"{val:.2f}", va="center", fontsize=9)
ax.set_xlim(1, 5)
ax.set_xlabel("Average Review Score")
ax.set_title("Bottom 10 Product Categories by Review Score\n(min. 50 orders)")
ax.legend(frameon=False, fontsize=9)
save("finding2_bottom_categories")


# ── 6. SELLER PERFORMANCE ANALYSIS — KEY FINDING 3 ───────────────────────────

print("\n\n═══════════════════════════════════════════════════════════════════════")
print("  FINDING 3 — A SMALL NUMBER OF SELLERS GENERATE DISPROPORTIONATE RISK")
print("═══════════════════════════════════════════════════════════════════════")

seller_stats = (df_delivery
    .groupby("primary_seller_id")
    .agg(
        order_count      = ("order_id",       "count"),
        avg_score        = ("review_score",    "mean"),
        pct_negative     = ("review_score",    lambda x: (x <= 2).mean()),
        total_revenue    = ("total_price",     "sum"),
        late_delivery_pct = ("is_late",        "mean"),
    )
    .query("order_count >= 30")
    .round(3)
)

# At-risk seller definition: score < 3.5 OR late delivery > 30%
seller_stats["at_risk"] = (
    (seller_stats["avg_score"] < 3.5) |
    (seller_stats["late_delivery_pct"] > 0.30)
)

at_risk_count    = seller_stats["at_risk"].sum()
at_risk_orders   = seller_stats.loc[seller_stats["at_risk"], "order_count"].sum()
at_risk_revenue  = seller_stats.loc[seller_stats["at_risk"], "total_revenue"].sum()
total_revenue_s  = seller_stats["total_revenue"].sum()

print(f"\n  At-risk sellers (score<3.5 OR late rate>30%): {at_risk_count}")
print(f"  Orders from at-risk sellers                 : {at_risk_orders:,}")
print(f"  Revenue from at-risk sellers (BRL)          : R$ {at_risk_revenue:,.0f}")
print(f"  At-risk revenue as % of qualifying total    : {at_risk_revenue/total_revenue_s:.1%}")


# ── Chart 5: Seller score distribution ───────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

# Histogram of seller avg scores
axes[0].hist(seller_stats["avg_score"], bins=30, color=OLIST_BLUE,
             alpha=0.75, edgecolor="white", linewidth=0.4)
axes[0].axvline(3.5, color=OLIST_RED, linewidth=1.5, linestyle="--",
                label="At-risk threshold (3.5)")
axes[0].axvline(seller_stats["avg_score"].mean(), color=OLIST_GREEN,
                linewidth=1.5, linestyle="-",
                label=f"Mean: {seller_stats['avg_score'].mean():.2f}")
axes[0].set_xlabel("Avg Review Score (per seller)")
axes[0].set_ylabel("Number of Sellers")
axes[0].set_title("Distribution of Seller Review Scores\n(sellers with ≥30 orders)")
axes[0].legend(frameon=False, fontsize=9)

# Scatter: seller score vs late delivery rate, sized by order count
sc = axes[1].scatter(
    seller_stats["late_delivery_pct"] * 100,
    seller_stats["avg_score"],
    s       = seller_stats["order_count"] / 2,
    c       = seller_stats["at_risk"].astype(int),
    cmap    = "RdYlGn_r",
    alpha   = 0.5,
    edgecolors = "white",
    linewidths = 0.4
)
axes[1].axhline(3.5, color=OLIST_RED,   linestyle="--", linewidth=1, alpha=0.7, label="Score threshold")
axes[1].axvline(30,  color=OLIST_AMBER, linestyle="--", linewidth=1, alpha=0.7, label="Late rate threshold")
axes[1].set_xlabel("Late Delivery Rate (%)")
axes[1].set_ylabel("Avg Review Score")
axes[1].set_title("Finding 3: Seller Risk Quadrant\nBubble size = order volume")
axes[1].legend(frameon=False, fontsize=9)

save("finding3_seller_performance")


# ── 7. REGIONAL ANALYSIS — KEY FINDING 4 ────────────────────────────────────

print("\n\n═══════════════════════════════════════════════════════════════════════")
print("  FINDING 4 — NORTHERN STATES FACE SIGNIFICANTLY LONGER DELIVERY TIMES")
print("═══════════════════════════════════════════════════════════════════════")

regional = (df_delivery
    .groupby("customer_state")
    .agg(
        order_count          = ("order_id",               "count"),
        avg_review_score     = ("review_score",           "mean"),
        avg_delivery_days    = ("actual_delivery_days",   "mean"),
        late_delivery_rate   = ("is_late",                "mean"),
    )
    .query("order_count >= 100")
    .round(2)
    .sort_values("avg_review_score")
)

print("\n  States with lowest avg review score:")
print(regional.head(8).to_string())
print("\n  States with highest avg review score:")
print(regional.tail(5).to_string())


# ── Chart 6: State performance ────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

# Bottom 10 states by score
bottom_states = regional.head(10).sort_values("avg_review_score")
colors_s = [OLIST_RED if s < 3.8 else OLIST_AMBER for s in bottom_states["avg_review_score"]]
axes[0].barh(bottom_states.index, bottom_states["avg_review_score"],
             color=colors_s, edgecolor="white", linewidth=0.6)
axes[0].axvline(kpi_overall_score, color=OLIST_GREEN, linestyle="--",
                linewidth=1.2, label=f"Platform avg: {kpi_overall_score:.2f}")
axes[0].set_xlim(3, 5)
axes[0].set_xlabel("Avg Review Score")
axes[0].set_title("States with Lowest Avg Review Score\n(min. 100 orders)")
axes[0].legend(frameon=False, fontsize=9)

# Late delivery rate vs avg score by state
sc2 = axes[1].scatter(
    regional["avg_delivery_days"],
    regional["avg_review_score"],
    s          = regional["order_count"] / 5,
    c          = regional["late_delivery_rate"],
    cmap       = "RdYlGn_r",
    alpha      = 0.75,
    edgecolors = "white",
    linewidths = 0.6
)
for state, row in regional.iterrows():
    if row["avg_review_score"] < 3.85 or row["avg_delivery_days"] > 25:
        axes[1].annotate(state,
                         xy=(row["avg_delivery_days"], row["avg_review_score"]),
                         xytext=(4, 2), textcoords="offset points",
                         fontsize=7.5, color=OLIST_DARK)
plt.colorbar(sc2, ax=axes[1], label="Late Delivery Rate")
axes[1].set_xlabel("Avg Actual Delivery Days")
axes[1].set_ylabel("Avg Review Score")
axes[1].set_title("Finding 4: Longer delivery times correlate\nwith lower review scores by state")

save("finding4_regional_performance")


# ── 8. KEY DRIVER SUMMARY ────────────────────────────────────────────────────

print("\n\n═══════════════════════════════════════════════════════════════════════")
print("  KEY DRIVER SUMMARY — WHAT HURTS SATISFACTION MOST?")
print("═══════════════════════════════════════════════════════════════════════")

# Score comparison: late vs on-time
late_score   = df_delivery.loc[df_delivery["is_late"],    "review_score"].mean()
ontime_score = df_delivery.loc[~df_delivery["is_late"],   "review_score"].mean()

# Score for bottom vs top category
top_cat_score = cat_summary.tail(1)["avg_score"].values[0]
bot_cat_score = cat_summary.head(1)["avg_score"].values[0]

print(f"""
  Factor                          | Low Group Score | High Group Score | Gap
  ─────────────────────────────────┼─────────────────┼──────────────────┼──────
  Delivery timing (late vs on-time)| {late_score:.2f}            | {ontime_score:.2f}             | {ontime_score-late_score:.2f}
  Product category (worst vs best) | {bot_cat_score:.2f}            | {top_cat_score:.2f}             | {top_cat_score-bot_cat_score:.2f}
  Seller performance               | (see seller analysis above)
  Regional variance                | (see regional analysis above)
""")


# ── Chart 7: Executive summary KPI card visual ────────────────────────────────

fig, axes = plt.subplots(1, 4, figsize=(14, 3))
fig.patch.set_facecolor(OLIST_LIGHT)

kpis = [
    ("Overall Avg\nReview Score",  f"{kpi_overall_score:.2f}",  "/5.0",     OLIST_GREEN),
    ("Late Delivery\nRate",        f"{kpi_late_rate:.1%}",       "of orders", OLIST_RED),
    ("Negative Review\nRate",      f"{kpi_negative_rate:.1%}",   "score ≤ 2", OLIST_AMBER),
    ("5-Star Review\nRate",        f"{kpi_five_star_rate:.1%}",  "of reviews", OLIST_BLUE),
]

for ax, (label, value, sub, color) in zip(axes, kpis):
    ax.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.72, value,  ha="center", va="center", fontsize=26,
            fontweight="bold", color=color)
    ax.text(0.5, 0.42, sub,    ha="center", va="center", fontsize=9, color=OLIST_GREY)
    ax.text(0.5, 0.18, label,  ha="center", va="center", fontsize=10,
            color=OLIST_DARK, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.patch.set_linewidth(1)
    ax.patch.set_edgecolor(color)
    ax.patch.set_visible(True)

fig.suptitle("Olist — Customer Satisfaction Dashboard | Key Platform Metrics",
             fontsize=13, fontweight="bold", y=1.08)

save("executive_kpi_cards")


# ── 9. EXPORT FOR DASHBOARD ───────────────────────────────────────────────────

# These CSVs feed directly into Tableau

df_delivery[["order_id", "customer_state", "delivery_bracket",
             "delivery_delta", "actual_delivery_days", "review_score",
             "is_late", "category_en", "total_price", "total_freight"]]\
    .to_csv(f"{OUTPUT_DIR}/tableau_orders_delivery.csv", index=False)

cat_summary.reset_index().to_csv(f"{OUTPUT_DIR}/tableau_category_summary.csv", index=False)

seller_stats.reset_index().rename(columns={"primary_seller_id":"seller_id"})\
    .to_csv(f"{OUTPUT_DIR}/tableau_seller_summary.csv", index=False)

regional.reset_index().to_csv(f"{OUTPUT_DIR}/tableau_regional_summary.csv", index=False)

print("\n✓ All outputs exported to /outputs/")
print("  → Import tableau_*.csv files into Tableau for dashboard build")
print("\n  Files exported:")
for f in os.listdir(OUTPUT_DIR):
    print(f"    {f}")
