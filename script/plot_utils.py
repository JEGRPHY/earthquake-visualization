import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_magnitude_distribution(df):
    st.subheader("Magnitude Distribution")
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Magnitude'], bins=[4.0, 4.5, 5.0, float('inf')], kde=False)
    plt.xlabel("Magnitude Range")
    plt.ylabel("Frequency")
    plt.title("Earthquake Frequency by Magnitude")
    st.pyplot(plt)
