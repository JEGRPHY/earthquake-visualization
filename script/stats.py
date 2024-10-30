import streamlit as st

def display_statistics(df):
    st.subheader("Summary Statistics")

    # Organize statistics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Display each metric in separate columns for a cleaner layout
    col1.metric("Total Earthquakes", f"{len(df)}")
    col2.metric("Average Magnitude", f"{df['Magnitude'].mean():.2f}")
    col3.metric("Max Magnitude", f"{df['Magnitude'].max():.2f}")
    col4.metric("Min Magnitude", f"{df['Magnitude'].min():.2f}")

    # Optional additional details or explanation
    st.caption("Earthquake data summarized for the selected period and magnitude threshold.")
