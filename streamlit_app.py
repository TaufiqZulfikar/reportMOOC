import streamlit as st
import requests
import pandas as pd
import base64
from st_aggrid import AgGrid, GridOptionsBuilder

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

# Check if the DataFrame is empty
if df.empty:
    st.write("No data fetched. Please check the URLs or the data fetching logic.")
else:
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

    # Rename the columns to include the month names
    monthly_summary.columns = [f"Bulan {col}" if isinstance(col, int) else col for col in monthly_summary.columns]

    # Convert monthly_summary to a DataFrame
    monthly_summary_df = monthly_summary.reset_index()

    # Create AgGrid table with frozen columns and additional features
    st.title("Binus MOOC Info Summary for 2024")
    st.write("Summary Table:")

    # Configure the grid options to freeze the first two columns and enable fullscreen and search
    gb = GridOptionsBuilder.from_dataframe(monthly_summary_df)
    gb.configure_column("DepartmendID", pinned=True)
    gb.configure_column("DepartmentName", pinned=True)
    #gb.configure_pagination(paginationAutoPageSize=True)  # Auto page size based on content
    gb.configure_grid_options(domLayout='normal', enableFullScreen=True, enableFilter=True)  # Enable fullscreen mode and search/filter
    gridOptions = gb.build()

    # Display AgGrid table
    AgGrid(monthly_summary_df, gridOptions=gridOptions)

    # Add option to download CSV
    if st.button("Download CSV"):
        csv = monthly_summary_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="binus_mooc_summary.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

# To run the app, save this file and execute the following command in the terminal:
# streamlit run app.py