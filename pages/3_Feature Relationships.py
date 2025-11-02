import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np

# Wczytanie danych
dt = pd.read_csv("cities_data/otodom_apartments_demo.csv", sep=";", encoding="utf-8-sig")
dt = dt[dt["city"] != "nieznane"]

st.header("3. Feature Relationships // Pairplot")


st.subheader("Select visualization type")

chart_type = st.radio(
    "Choose chart type:",
    ["Pairplot", "Heatmap", ],
    horizontal=True
)

if chart_type == "Pairplot":
    numeric_cols = ["price", "price_per_m2", "area", "rooms", "floor"]
    
    selected_city = st.selectbox("Filter by city (optional):", ["All"] + sorted(dt["city"].unique()))
    df_filtered = dt if selected_city == "All" else dt[dt["city"] == selected_city]
    
    # Tworzenie pairplotu
    fig = sns.pairplot(df_filtered[numeric_cols], diag_kind="kde", plot_kws={"alpha":0.6, "s":40})
    plt.suptitle(f"Pairplot of numeric features {'for ' + selected_city if selected_city != 'All' else ''}", y=1.02)
    
    st.pyplot(fig)

##############################
# HEATMAP
##############################


elif chart_type == "Heatmap":
    st.subheader("Feature correlation // Heatmap")
    st.write("It helps you see which features have the strongest impact on price.")

    numeric_cols = ["price", "price_per_m2", "area", "rooms", "floor"]
    corr = dt[numeric_cols].corr()

    fig = ff.create_annotated_heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.columns),
        annotation_text=np.round(corr.values, 2),
        colorscale="Blues"
    )

    # 🔹 Dostosowanie layoutu
    fig.update_layout(
        title="Correlation heatmap of numerical features",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
