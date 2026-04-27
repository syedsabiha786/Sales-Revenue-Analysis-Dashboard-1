import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

df = pd.read_csv("data.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.title("Sales & Revenue Analysis Dashboard")

region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]

total_revenue = filtered_df["Revenue"].sum()
total_sales = filtered_df["Units Sold"].sum()
top_product = filtered_df.groupby("Product")["Revenue"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", total_revenue)
col2.metric("Total Units Sold", total_sales)
col3.metric("Top Product", top_product)

revenue_trend = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
fig1 = px.line(revenue_trend, x="Date", y="Revenue", title="Revenue Trend")
st.plotly_chart(fig1, use_container_width=True)

product_sales = filtered_df.groupby("Product")["Revenue"].sum().reset_index()
fig2 = px.bar(product_sales, x="Product", y="Revenue", title="Revenue by Product")
st.plotly_chart(fig2, use_container_width=True)

region_sales = filtered_df.groupby("Region")["Revenue"].sum().reset_index()
fig3 = px.pie(region_sales, names="Region", values="Revenue", title="Revenue by Region")
st.plotly_chart(fig3, use_container_width=True)
