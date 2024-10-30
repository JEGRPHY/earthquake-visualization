import streamlit as st
import pandas as pd
from script.data_fetcher import fetch_earthquake_data
from script.map_utils import create_earthquake_map, save_map_as_html
from script.stats import display_statistics
from script.plot_utils import plot_magnitude_distribution
from streamlit_folium import folium_static

# Streamlit app configuration
st.title("Earthquake Visualization")
st.sidebar.header("Filter Options")

# Date range selection
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-10-02"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-10-09"))

# Magnitude filter selection
min_magnitude = st.sidebar.slider("Minimum Magnitude", min_value=4.0, max_value=10.0, value=4.0, step=0.1)

if start_date > end_date:
    st.error("Error: Start Date must be before End Date.")
else:
    # Fetch data with start and end date
    df = fetch_earthquake_data(start_date=start_date, end_date=end_date)

    # Filter data based on minimum magnitude
    df = df[df['Magnitude'] >= min_magnitude]

    if df.empty:
        st.write("No earthquake data available for this period and magnitude threshold.")
    else:
        # Map Visualization
        m = create_earthquake_map(df)
        folium_static(m)
        save_map_as_html(m)

        # Statistics and Plotting
        display_statistics(df)
        plot_magnitude_distribution(df)
