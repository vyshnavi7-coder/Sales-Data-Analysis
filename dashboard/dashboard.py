import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel("data/ecommerce_sales.xlsx")

df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = df["Quantity Sold"] * df["Price"]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📌 Dashboard Filters")

category = st.sidebar.selectbox(
    "Product Category",
    ["All"] + list(df["Product Category"].unique())
)

if "Region" in df.columns:
    region = st.sidebar.selectbox(
        "Region",
        ["All"] + list(df["Region"].unique())
    )
else:
    region = "All"

if category != "All":
    df = df[df["Product Category"] == category]

if region != "All":
    df = df[df["Region"] == region]

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📊 Sales Insights Dashboard")
st.markdown("### Retail Sales Performance & Business Analytics")

st.markdown("---")

# -----------------------------
# KPI Cards
# -----------------------------
total_revenue = df["Revenue"].sum()
total_orders = len(df)
total_products = df["Product Name"].nunique()
total_quantity = df["Quantity Sold"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🛒 Orders", total_orders)
col3.metric("📦 Products", total_products)
col4.metric("📈 Quantity Sold", total_quantity)

st.markdown("---")

# -----------------------------
# Top Selling Products
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top 5 Best Selling Products")

    top_products = (
        df.groupby("Product Name")["Quantity Sold"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    fig, ax = plt.subplots(figsize=(7,4))
    top_products.plot(kind="bar", ax=ax)
    ax.set_ylabel("Quantity Sold")
    ax.set_xlabel("")
    st.pyplot(fig)

# -----------------------------
# Revenue by Category
# -----------------------------
with col2:

    st.subheader("📂 Revenue by Category")

    revenue_category = df.groupby("Product Category")["Revenue"].sum()

    fig, ax = plt.subplots(figsize=(6,6))
    revenue_category.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

st.markdown("---")

# -----------------------------
# Sales Trend
# -----------------------------
st.subheader("📈 Revenue Trend")

sales_trend = df.groupby("Date")["Revenue"].sum()

fig, ax = plt.subplots(figsize=(12,5))
sales_trend.plot(ax=ax)
ax.set_ylabel("Revenue")
ax.set_xlabel("Date")
st.pyplot(fig)

# -----------------------------
# Revenue by Region
# -----------------------------
if "Region" in df.columns:

    st.markdown("---")

    st.subheader("🌍 Revenue by Region")

    region_sales = df.groupby("Region")["Revenue"].sum()

    fig, ax = plt.subplots(figsize=(8,4))
    region_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

# -----------------------------
# Dataset Preview
# -----------------------------
st.markdown("---")

st.subheader("📄 Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

# -----------------------------
# Download Button
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "sales_data.csv",
    "text/csv"
)

st.markdown("---")

st.success("✅ Dashboard Loaded Successfully")
