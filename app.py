import streamlit as st
import folium
import pandas as pd
import requests
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Fetch earthquake data
# Fetch earthquake data with error handling
@st.cache_data
def fetch_earthquake_data(start_date, end_date):
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}'
    response = requests.get(url)
    
    # Check for a successful response
    if response.status_code == 200:
        try:
            data = response.json()
            earthquakes = []
            for feature in data['features']:
                magnitude = feature['properties']['mag']
                if magnitude > 4.0:
                    earthquakes.append({
                        "Latitude": feature['geometry']['coordinates'][1],
                        "Longitude": feature['geometry']['coordinates'][0],
                        "Magnitude": magnitude,
                        "Time": feature['properties']['time']
                    })
            return pd.DataFrame(earthquakes)
        except ValueError:
            st.error("Error: Failed to parse earthquake data. Please check the date range and try again.")
            return pd.DataFrame()  # Return an empty DataFrame if parsing fails
    else:
        st.error("Error: Could not retrieve data from USGS API. Please check your connection or try again later.")
        return pd.DataFrame()  # Return an empty DataFrame if response fails


# Streamlit app configuration
st.title("Earthquake Visualization")
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-10-02"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-10-09"))

# Fetch data based on user input
df = fetch_earthquake_data(start_date=start_date, end_date=end_date)

if df.empty:
    st.write("No earthquake data available for this period.")
else:
    # Earthquake map
    st.subheader("Earthquake Map")
    center_lat, center_lon = df['Latitude'].mean(), df['Longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=8,
            color="red" if row["Magnitude"] > 5 else "orange",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    
    folium_static(m)

    # Earthquake statistics
    st.subheader("Summary Statistics")
    st.write(f"Total Earthquakes: {len(df)}")
    st.write(f"Average Magnitude: {df['Magnitude'].mean():.2f}")
    st.write(f"Max Magnitude: {df['Magnitude'].max():.2f}")
    st.write(f"Min Magnitude: {df['Magnitude'].min():.2f}")

    # Frequency distribution plot
    st.subheader("Magnitude Distribution")
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Magnitude'], bins=[4.0, 4.5, 5.0, float('inf')], kde=False)
    plt.xlabel("Magnitude Range")
    plt.ylabel("Frequency")
    plt.title("Earthquake Frequency by Magnitude")
    st.pyplot(plt)
