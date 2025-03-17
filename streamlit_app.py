import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore_Sales_utf8.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()  # Remove extra spaces from column names
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])  # Convert to datetime
    return df

df = load_data()

# Sidebar: Category selection
category_selected = st.selectbox("Select a Category:", options=df["Category"].unique())

# Filter Sub-Categories based on selected Category
filtered_subcategories = df[df["Category"] == category_selected]["Sub_Category"].unique()
subcategories_selected = st.multiselect("Select Sub-Categories:", options=filtered_subcategories, default=filtered_subcategories)

# Filter dataset based on selections
filtered_df = df[(df["Category"] == category_selected) & (df["Sub_Category"].isin(subcategories_selected))]

# Display filtered data
st.write(f"### Showing data for Category: **{category_selected}**, Sub-Categories: **{', '.join(subcategories_selected)}**")
st.write(filtered_df.head())  # Show first few rows

# Line chart of Sales over time
if not filtered_df.empty:
    sales_over_time = filtered_df.groupby("Order_Date")["Sales"].sum().reset_index()
    st.line_chart(sales_over_time, x="Order_Date", y="Sales", use_container_width=True)

    # Metrics calculations
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Calculate overall profit margin for delta comparison
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta_profit_margin = profit_margin - overall_profit_margin

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales ($)", f"{total_sales:,.2f}")
    col2.metric("Total Profit ($)", f"{total_profit:,.2f}")
    col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")
