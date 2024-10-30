import requests
import pandas as pd
import streamlit as st

@st.cache_data
def fetch_earthquake_data(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date_str}&endtime={end_date_str}'
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            earthquakes = [
                {
                    "Latitude": feature['geometry']['coordinates'][1],
                    "Longitude": feature['geometry']['coordinates'][0],
                    "Magnitude": feature['properties']['mag'],
                    "Time": feature['properties']['time']
                }
                for feature in data['features'] if feature['properties']['mag'] > 4.0
            ]
            return pd.DataFrame(earthquakes)
        except ValueError:
            st.error("Error: Failed to parse earthquake data. Please check the date range and try again.")
            return pd.DataFrame()
    else:
        st.error("Error: Could not retrieve data from USGS API. Please check your connection or try again later.")
        return pd.DataFrame()
