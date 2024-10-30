import streamlit as st

def display_statistics(df):
    st.subheader("Summary Statistics")
    st.write(f"Total Earthquakes: {len(df)}")
    st.write(f"Average Magnitude: {df['Magnitude'].mean():.2f}")
    st.write(f"Max Magnitude: {df['Magnitude'].max():.2f}")
    st.write(f"Min Magnitude: {df['Magnitude'].min():.2f}")
