import streamlit as st
import pandas as pd
import plotly.express as px

# The raw GitHub URL to the Excel file
url = "https://raw.githubusercontent.com/kingsleyeyo24/West_Africa_Terrorism_Data_App/main/new_crime_WA.xlsx"

# Ensure Date column is datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Extract year
df["Year"] = df["Date"].dt.year

# Convert fatalities & injured to numeric
df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce")
df["injured"] = pd.to_numeric(df["injured"], errors="coerce")

# Sidebar Filters
st.sidebar.header("Filter Data")

country = st.sidebar.multiselect("Select Country", df["Country"].unique(), default=["Nigeria", "Cameroon", "Ghana", "Niger", "Chad", "Benin"])
#month = st.sidebar.multiselect("Select Month", df["Month"].unique(), default=["December"])
year = st.sidebar.multiselect("Select Year", df["Year"].sort_values().unique(), default=[2020])

# Apply Filters
filtered = df[
    (df["Country"].isin(country)) &
   # (df["Month"].isin(month)) &
    (df["Year"].isin(year))
]

# Title and description
st.title("West Africa Terrorism Data Dashboard")
st.markdown("Terrorism incidents by country, group, and impact. Data filtered by year, and country.")

# Data Table Preview
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered)

# Horizontal Bar Chart - Incidents by Country
st.subheader("🌍 Incidents by Country")

# Prepare data correctly
country_chart = (
    filtered["Country"]
    .value_counts()
    .reset_index()
)
country_chart.columns = ["Country", "Number of Incidents"]  # Apply correct names

# Create bar chart
fig = px.bar(
    country_chart,
    x="Number of Incidents",
    y="Country",
    orientation="h",
    title="Terrorism Incidents by Country",
    color="Number of Incidents",
    color_continuous_scale="Reds",
    height=400 + len(country_chart) * 20  # ensure all countries are visible
)

st.plotly_chart(fig)


# Incidents by City
st.subheader("Incidents by City")
city_chart = filtered["City"].value_counts().reset_index()
city_chart.columns = ["City", "Number of Incidents"]
st.plotly_chart(px.bar(city_chart, x="City", y="Number of Incidents"))

# Perpetrator Groups
# Set a threshold for "very low" percentages
threshold = 4.0  # Percentage

# Group values below threshold into "Others"
group_counts = filtered['Perpetrator_group'].value_counts(normalize=True) * 100
low_groups = group_counts[group_counts < threshold].index
filtered['Perpetrator_group'] = filtered['Perpetrator_group'].replace(low_groups, 'Others')

# Perpetrator Groups
st.subheader("Perpetrator Groups")
group_chart = filtered["Perpetrator_group"].value_counts().reset_index()
group_chart.columns = ["Group", "Incidents"]
st.plotly_chart(px.pie(group_chart, names="Group", values="Incidents"))


# Fatalities vs Injured
st.subheader("Fatalities vs Injured")
scatter = px.scatter(
    filtered, x="fatalities", y="injured", color="Perpetrator_group",
    title="Fatalities vs Injured per Attack", size_max=10
)
st.plotly_chart(scatter)

#  Line Chart - Incidents by Month
st.subheader("Incidents by Month")

# Correct month order
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Count and order
monthly_chart = (
    filtered["Month"]
    .value_counts()
    .reindex(month_order)  # Ensure proper order
    .dropna()
    .reset_index()
)

monthly_chart.columns = ["Month", "Number of Incidents"]

# Plot
fig = px.line(
    monthly_chart,
    x="Month",
    y="Number of Incidents",
    title="Monthly Trend of Terrorism Incidents",
    markers=True,
    line_shape="linear"
)

st.plotly_chart(fig)


# Endnote and follow up
st.markdown("""
---
**Dashboard developed by Kingsley Eyo**  
[LinkedIn](https://www.linkedin.com/in/kingsley-eyo-5a4611230/)  
[GitHub](https://github.com/kingsleyeyo24)
""")
