import streamlit as st
import pandas as pd
from script.data_fetcher import fetch_earthquake_data
from script.map_utils import create_earthquake_map, save_map_as_html
from script.stats import display_statistics
from script.plot_utils import plot_magnitude_distribution

# Streamlit app configuration
st.title("Earthquake Visualization")
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-10-02"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-10-09"))

if start_date > end_date:
    st.error("Error: Start Date must be before End Date.")
else:
    df = fetch_earthquake_data(start_date=start_date, end_date=end_date)

    if df.empty:
        st.write("No earthquake data available for this period.")
    else:
        # Map Visualization
        m = create_earthquake_map(df)
        folium_static(m)
        save_map_as_html(m)

        # Statistics and Plotting
        display_statistics(df)
        plot_magnitude_distribution(df)
