import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config("📦 E-Commerce KPI Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    df["DeliveryDays"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("📌 Filters")
selected_region = st.sidebar.selectbox("Select Region", df["Region"].unique())
df_filtered = df[df["Region"] == selected_region]

# Title
st.title("📦 E-Commerce KPI Dashboard")

# Optional raw data
with st.expander("🧾 Show raw data"):
    st.dataframe(df_filtered)

# === Row 1: Global KPIs ===
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_margin = (total_profit / total_sales) * 100 if total_sales else 0
global_delivery = df["DeliveryDays"].mean()

g1, g2, g3, g4, g5 = st.columns(5)
g1.metric("💰 Total Sales", f"${total_sales:,.2f}")
g2.metric("📈 Total Profit", f"${total_profit:,.2f}")
g3.metric("🛒 Total Orders", total_orders)
g4.metric("📊 Profit Margin", f"{total_margin:.2f}%")
g5.metric("🚚 Avg. Delivery Days", f"{global_delivery:.2f}")

# === Row 2: Regional KPIs ===
st.subheader(f"📍 KPIs for Region: {selected_region}")

regional_sales = df_filtered["Sales"].sum()
regional_profit = df_filtered["Profit"].sum()
regional_orders = df_filtered["Order ID"].nunique()
regional_margin = (regional_profit / regional_sales) * 100 if regional_sales else 0
regional_delivery = df_filtered["DeliveryDays"].mean()

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("💰 Regional Sales", f"${regional_sales:,.2f}")
r2.metric("📈 Regional Profit", f"${regional_profit:,.2f}")
r3.metric("🛒 Regional Orders", regional_orders)
r4.metric("📊 Regional Margin", f"{regional_margin:.2f}%")
r5.metric("🚚 Regional Delivery Days", f"{regional_delivery:.2f}")

# === Row 3: Sales Overview ===
st.markdown("### 📊 Sales Overview (Filtered Region)")

# Sales by Category
fig_cat = px.bar(
    df_filtered.groupby("Category")["Sales"].sum().reset_index(),
    x="Category", y="Sales",
    title="Sales by Category", text_auto=True
)

# Monthly Sales Trend
df_filtered["Month"] = df_filtered["Order Date"].dt.to_period("M").dt.to_timestamp()
monthly_sales = df_filtered.groupby("Month")["Sales"].sum().reset_index()

fig_time = px.line(
    monthly_sales,
    x="Month", y="Sales",
    title="Monthly Sales Trend"
)

c1, c2 = st.columns(2)
c1.plotly_chart(fig_cat, use_container_width=True)
c2.plotly_chart(fig_time, use_container_width=True)

# === Row 4: Deep Dive Visualizations ===
st.markdown("### 🔍 Deep Dive Visualizations")

# Sales by Sub-Category
subcat_sales = df_filtered.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
fig_subcat = px.bar(
    subcat_sales,
    x="Sub-Category", y="Sales",
    title="Sales by Sub-Category", text_auto=True
)

# Profit by Region (Global)
region_profit = df.groupby("Region")["Profit"].sum().reset_index().sort_values("Profit", ascending=True)
fig_region_profit = px.bar(
    region_profit,
    x="Profit", y="Region", orientation='h',
    title="Profit by Region"
)

d1, d2 = st.columns(2)
d1.plotly_chart(fig_subcat, use_container_width=True)
d2.plotly_chart(fig_region_profit, use_container_width=True)

# === Row 5: Delivery Analysis ===
st.markdown("### 🚚 Delivery Performance")

# Regional Delivery Table
st.markdown("#### 📍 Avg. Delivery Days per City (Selected Region)")
city_delivery = df_filtered.groupby("City")["DeliveryDays"].mean().reset_index().sort_values("DeliveryDays")
st.dataframe(city_delivery, use_container_width=True)

# Global City Delivery Chart
global_city_delivery = df.groupby("City")["DeliveryDays"].mean().reset_index().sort_values("DeliveryDays", ascending=True)
fig_city_delivery = px.bar(
    global_city_delivery,
    x="DeliveryDays", y="City", orientation="h",
    title="Avg. Delivery Days per City (Global)",
    labels={"DeliveryDays": "Avg. Days"}
)
st.plotly_chart(fig_city_delivery, use_container_width=True)
