import folium
import streamlit as st
from streamlit_folium import folium_static

def create_earthquake_map(df):
    center_lat, center_lon = df['Latitude'].mean(), df['Longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=8,
            color="red" if row["Magnitude"] > 7 else "orange",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    
    return m

def save_map_as_html(m):
    html_data = m._repr_html_()
    st.download_button("Download Map as HTML", data=html_data, file_name="earthquake_map.html", mime="text/html")
