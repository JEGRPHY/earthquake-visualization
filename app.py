import streamlit as st
import folium
import pandas as pd
import requests
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def save_map_as_image(m, output_path="latest_map.png"):
    # Save the map as an HTML file temporarily
    m.save("temp_map.html")
    
    # Set up Selenium to open the HTML file and take a screenshot
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver using Service and executable_path arguments correctly
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the HTML map file and take a screenshot
    driver.get("file://" + io.os.path.abspath("temp_map.html"))
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    
    # Open the screenshot with PIL and crop it as needed
    image = Image.open(io.BytesIO(screenshot))
    # Adjust cropping dimensions as needed
    image_cropped = image.crop((0, 0, image.width, image.height))
    image_cropped.save(output_path)


# Fetch earthquake data with error handling
@st.cache_data
def fetch_earthquake_data(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date_str}&endtime={end_date_str}'
    response = requests.get(url)
    
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
            return pd.DataFrame()
    else:
        st.error("Error: Could not retrieve data from USGS API. Please check your connection or try again later.")
        return pd.DataFrame()

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

        # Save the latest map image
        if st.button("Save Latest Map Image"):
            save_map_as_image(m)
            st.success("Map image saved as 'latest_map.png'.")

        st.subheader("Summary Statistics")
        st.write(f"Total Earthquakes: {len(df)}")
        st.write(f"Average Magnitude: {df['Magnitude'].mean():.2f}")
        st.write(f"Max Magnitude: {df['Magnitude'].max():.2f}")
        st.write(f"Min Magnitude: {df['Magnitude'].min():.2f}")

        st.subheader("Magnitude Distribution")
        plt.figure(figsize=(8, 6))
        sns.histplot(df['Magnitude'], bins=[4.0, 4.5, 5.0, float('inf')], kde=False)
        plt.xlabel("Magnitude Range")
        plt.ylabel("Frequency")
        plt.title("Earthquake Frequency by Magnitude")
        st.pyplot(plt)
