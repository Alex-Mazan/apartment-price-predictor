import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. General Analysis
st.header("1. General Analysis")

# Wczytanie danych
dt = pd.read_csv("cities_data/otodom_apartments_demo.csv", sep=";", encoding="utf-8-sig")
dt = dt[dt["city"] != "nieznane"]

st.write("Available columns: ",", ".join((dt.columns)))

# Przygotowanie danych do wykresu słupkowego
city_counts = dt["city"].value_counts()
city_df = pd.DataFrame({
    "city": city_counts.index,
    "count": city_counts.values
})

# --- COL1: Bar Plot ---
st.subheader("Amount of apartments per city // Barplot")

plt.figure(figsize=(12, 8))
sns.barplot(x="city", y="count", data=city_df, palette="mako")
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Amount of apartments")
plt.title("Amount of apartments per city")
plt.tight_layout()
st.pyplot(plt)

# --- COL2: Histogram ---
st.subheader("Distribution of apartment sizes // Histogram")

plt.figure(figsize=(12, 8))
sns.histplot(
    data=dt,
    x="area",
    bins=10,
    kde=False,
    color="#4B5563"
)

plt.xlabel("Apartment area (m²)")
plt.ylabel("Number of apartments")
plt.title("Number of apartments by area range")
plt.grid(True, linestyle="--", alpha=0.4)
st.pyplot(plt)

# --- COL3: Pie Chart ---
st.subheader("Private offers vs. real estate agencies // PieChart")

offers_counts = dt["type"].value_counts()

plt.figure(figsize=(3, 3))
plt.pie(
    offers_counts.values,
    labels=offers_counts.index,
    autopct="%1.1f%%",
    startangle=190,
    shadow=False
)
plt.title("Private offers vs. real estate agencies")
st.pyplot(plt)
