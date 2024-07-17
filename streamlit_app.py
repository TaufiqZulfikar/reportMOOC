import streamlit as st
import requests
import pandas as pd

# URLs for each month
urls = [
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=1",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=2",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=3",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=4",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=5",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=6",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=7",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=8",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=9",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=10",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=11",
    "https://binus.ac.id/mooc/wp-json/api/v1/info/query?year=2024&month=12",
]

# Fetch data from each URL and combine it into a single list
all_data = []
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("data", {}).get("results", [])
        all_data.extend(results)
    else:
        st.error(f"Failed to fetch data from {url}")

# Create a DataFrame to process the data
df = pd.DataFrame(all_data)

# Convert 'TotalCourse' to integers
df['TotalCourse'] = df['TotalCourse'].astype(int)

# Group data by DepartmentID and DepartmentName, and summarize by month
df['month'] = pd.to_datetime(df['PublishDate']).dt.month
monthly_summary = df.pivot_table(index=['DepartmendID', 'DepartmentName'], columns='month', values='TotalCourse', aggfunc='sum', fill_value=0)

# Ensure all months from 1 to 12 are present
all_months = range(1, 13)
monthly_summary = monthly_summary.reindex(columns=all_months, fill_value=0)

# Add a 'total' column for each department
monthly_summary['total'] = monthly_summary.sum(axis=1)

# Reformat the DataFrame for the summary table
summary_table = monthly_summary.reset_index()
summary_table = summary_table[['DepartmendID', 'DepartmentName', 'total']]

# Display the first summary table
st.title("Binus MOOC Info Summary for 2024")
st.write("Summary Table 1:")
st.dataframe(summary_table)

# Display a separator or text to distinguish between tables
st.write("---")

# Group data by DepartmentID and DepartmentName, and summarize by month
# Note: You can remove this duplicated code and just use the summary_table DataFrame if it's the same data you want to display.
monthly_summary = df.pivot_table(index=['DepartmendID', 'DepartmentName'], columns='month', values='TotalCourse', aggfunc='sum', fill_value=0)

# Ensure all months from 1 to 12 are present
all_months = range(1, 13)
monthly_summary = monthly_summary.reindex(columns=all_months, fill_value=0)

# Add a 'total' column for each department
monthly_summary['total'] = monthly_summary.sum(axis=1)

# Rename the columns to include the month names
monthly_summary.columns = [f"Bulan {col}" if isinstance(col, int) else col for col in monthly_summary.columns]

# Display the second summary table
st.title("Binus MOOC Info Summary for 2024")
st.write("Summary Table 2:")
st.dataframe(monthly_summary.reset_index())
