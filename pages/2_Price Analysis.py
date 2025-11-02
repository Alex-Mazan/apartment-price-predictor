import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

# 2. Price Analysis
st.header("2. Price Analysis")

# Wczytanie danych
dt = pd.read_csv("cities_data/otodom_apartments_demo.csv", sep=";", encoding="utf-8-sig")
dt = dt[dt["city"] != "nieznane"]

st.subheader("Select visualization type")

chart_type = st.radio(
    "Choose chart type:",
    ["📦 Boxplot", "🎻 Violinplot", "💸 Scatterplot", "📊 Barplot", "🔥 Heatmap"],
    horizontal=True
)

##############################
# BOXPLOT
##############################


if chart_type == "📦 Boxplot":
    st.subheader("Price range // Boxplot")
    st.write("The most classic way to compare prices between categories")

    valid_pairs = {
        "type": ["price", "price_per_m2", "area"],
        "district": ["price", "price_per_m2"],
        "city": ["price", "price_per_m2"],
        "region": ["price_per_m2"],
        "rooms": ["price", "price_per_m2"],
        "floor": ["price_per_m2"]
    }

    # 🔹 Wybór osi
    x = st.selectbox("Select a category (X-axis):", list(valid_pairs.keys()))
    y = st.selectbox("Select a numeric variable (Y-axis):", valid_pairs[x])

    # 🔹 Filtrowanie miasta, jeśli wybrano "district"
    filtered_dt = dt.copy()
    if x == "district":
        available_cities = sorted(dt["city"].unique())
        selected_city = st.selectbox("Select a city:", available_cities)
        filtered_dt = dt[dt["city"] == selected_city]
        st.info(f"Only districts from **{selected_city}** are shown.")

    # 🔹 Generowanie boxplota
    fig = px.box(
        filtered_dt,
        x=x,
        y=y,
        color=x,
        points=False,
        title=f"Distribution of {y.replace('_', ' ')} relative to {x}",
        template="plotly_white",
    )

    fig.update_layout(
        xaxis_title=x.capitalize(),
        yaxis_title=y.replace("_", " ").capitalize(),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


##############################
# VIOLINPLOT
##############################


elif chart_type == "🎻 Violinplot":
    st.subheader("Price range // Violinplot")
    st.write("Better than a box plot when you want to show differences in distribution (e.g., two peaks)")

    valid_pairs_violin = {
        "city": ["price_per_m2"],
        "district": ["price_per_m2"],
        "type": ["price"],
        "rooms": ["price_per_m2"],
        "floor": ["price_per_m2"],
        "region": ["price_per_m2"]
    }

    x_violin = st.selectbox("Select a category (X-axis):", list(valid_pairs_violin.keys()))
    y_violin = st.selectbox("Select a numeric variable (Y-axis):", valid_pairs_violin[x_violin])

    filtered_dt_violin = dt.copy()

    # Filtrowanie miasta dla dzielnic (analogicznie jak wyżej)
    if x_violin == "district":
        available_cities_violin = sorted(dt["city"].unique())
        selected_city_violin = st.selectbox("Select a city for violinplot:", available_cities_violin)
        filtered_dt_violin = dt[dt["city"] == selected_city_violin]
        st.info(f"Showing violinplot for districts in **{selected_city_violin}**.")

    # 🔹 Generowanie violinplota
    fig_violin = px.violin(
        filtered_dt_violin,
        x=x_violin,
        y=y_violin,
        color=x_violin,
        box=True,  # dodaje boxplot wewnątrz
        points=False,
        title=f"Distribution of {y_violin.replace('_', ' ')} relative to {x_violin}",
        template="plotly_white"
    )

    fig_violin.update_layout(
        xaxis_title=x_violin.capitalize(),
        yaxis_title=y_violin.replace("_", " ").capitalize(),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig_violin, use_container_width=True)

elif chart_type == "💸 Scatterplot":
    st.subheader("Relationship between area and price // Scatterplot")
    st.write("It shows whether larger apartments are proportionally more expensive.")

    y_option = st.selectbox(
        "Select price type: ",
        ["price", "price_per_m2"]
    )

    color_option = st.selectbox(
        "Color points by:",
        ["city","type","rooms"]
    )

    selected_city = st.selectbox("Filter by city:", ["All"] + sorted(dt["city"].unique()))
    filtered_dt = dt if selected_city == "All" else dt[dt["city"] == selected_city]

    fig_scatter = px.scatter(
        filtered_dt,
        x="area",
        y=y_option,
        color=color_option,
        size="rooms",
        hover_data=["city", "district", "price", "area"],
        template="plotly_white",
        title=f"Relationship between apartment area and {y_option.replace('_', ' ')}"
    )

    fig_scatter.update_layout(
        xaxis_title = "Apartment area (m²)",
        yaxis_title = y_option.replace("_"," ").capitalize(),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    
##############################
# BARPLOT
##############################


elif chart_type == "📊 Barplot":
    st.subheader("Average price per city // Barplot")
    st.write("Intuitive city overview.")

    avg_city_price = dt.groupby("city")["price_per_m2"].mean().sort_values(ascending=False).reset_index()

    fig_bar = px.bar(
        avg_city_price,
        x="city",
        y="price_per_m2",
        color="price_per_m2",
        color_continuous_scale="Blues",
        title="Average price per m² by city",
        template="plotly_white"
    )

    fig_bar.update_layout(
        xaxis_title = "City",
        yaxis_title = "Average price per m² (PLN)",
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig_bar, use_container_width=True)