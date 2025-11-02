import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.subheader("4. Geographical Visualizations")

# Wczytanie danych
dt = pd.read_csv("cities_data/otodom_apartments_demo.csv", sep=";", encoding="utf-8-sig")
dt = dt[dt["city"] != "nieznane"]

###########################
# 1️⃣ Choropleth – Polska wg województw
###########################

st.markdown("### Choropleth - średnia cena za m² wg województw")

# Średnia cena per m² po regionach
avg_region_price = dt.groupby("region")["price_per_m2"].mean().reset_index()

# Wczytanie geojson województw
with open("geojson-wojewodztwa/wojewodztwa-medium.geojson", "r", encoding="utf-8") as f:
    voivodeships = json.load(f)

# Sprawdzenie jak nazywa się pole z nazwą województwa w geojson
# print(voivodeships['features'][0]['properties'])

# Dopasuj nazwę pola z geojson do swojej struktury np. 'wojewodztwo'
feature_key = "properties.wojewodztwo"  # <- zmień jeśli w Twoim pliku jest inaczej

fig_choropleth = px.choropleth(
    avg_region_price,
    geojson=voivodeships,
    locations="region",
    featureidkey=feature_key,
    color="price_per_m2",
    color_continuous_scale="Blues",
    title="Average price per m² by region",
    labels={"price_per_m2": "Price per m² (PLN)"},
    hover_data={"price_per_m2": ":.2f"}
)

fig_choropleth.update_geos(
    fitbounds="locations",  # dopasowuje mapę do geojson
    visible=False           # usuwa ramkę świata
)

fig_choropleth.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
st.plotly_chart(fig_choropleth, use_container_width=True)


###########################
# 2️⃣ Bubble Map – miasta
###########################

st.markdown("### Bubble Map - miasta wg średniej ceny za m²")

# Sprawdzenie czy w CSV są kolumny latitude i longitude
if "latitude" in dt.columns and "longitude" in dt.columns:
    avg_city_price = dt.groupby(["city", "latitude", "longitude"])["price_per_m2"].mean().reset_index()

    fig_bubble = px.scatter_mapbox(
        avg_city_price,
        lat="latitude",
        lon="longitude",
        size="price_per_m2",
        color="price_per_m2",
        hover_name="city",
        color_continuous_scale="Blues",
        size_max=25,
        zoom=5,
        mapbox_style="carto-positron",
        title="Average price per m² by city"
    )

    st.plotly_chart(fig_bubble, use_container_width=True)
else:
    st.warning("Brak kolumn latitude/longitude w danych. Bubble Map nie może zostać wygenerowana.")
