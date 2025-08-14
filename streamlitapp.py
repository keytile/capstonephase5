import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Kenya Tree Planting (Folium)", layout="wide")
st.title("🌳 Kenya Tree Planting Dashboard — Folium Edition")
st.markdown("Simpler app without GeoPandas, using Folium for mapping.")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data(path="df_gps.csv"):
    df = pd.read_csv(path, header=None, on_bad_lines="skip")
    df.columns = [
        "gps_str", "plantingdate", "seedlingsplanted", "month_year",
        "lat", "lon", "temperature", "rainfall"
    ]
    # Convert types
    df["plantingdate"] = pd.to_datetime(df["plantingdate"], errors="coerce")
    for col in ["seedlingsplanted", "lat", "lon"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Drop rows with missing coords
    df = df.dropna(subset=["lat", "lon"])
    # Filter to Kenya bounds
    kenya_mask = (
        (df["lat"] >= -5.0) & (df["lat"] <= 5.0) &
        (df["lon"] >= 33.0) & (df["lon"] <= 42.0)
    )
    return df[kenya_mask].copy()

df = load_data()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")
season_choice = st.sidebar.radio("Season", ["All", "Rainy", "Dry"], index=0)
rainy_months = {3, 4, 5, 10, 11, 12}
df["month"] = df["plantingdate"].dt.month
df["is_rainy"] = df["month"].isin(rainy_months)

if season_choice == "Rainy":
    df = df[df["is_rainy"]]
elif season_choice == "Dry":
    df = df[~df["is_rainy"]]

# -----------------------
# Metrics
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Trees", f"{int(df['seedlingsplanted'].sum()):,}")
col2.metric("Records", len(df))
rainy_pct = df["is_rainy"].mean() * 100 if len(df) else 0
col3.metric("Rainy Season %", f"{rainy_pct:.1f}%")

# -----------------------
# Map with Folium
# -----------------------
if not df.empty:
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=6, tiles="CartoDB positron")

    for _, row in df.iterrows():
        popup_html = f"""
        <b>Date:</b> {row['plantingdate'].date()}<br>
        <b>Seedlings:</b> {row['seedlingsplanted']}<br>
        <b>Temperature:</b> {row['temperature']}°C<br>
        <b>Rainfall:</b> {row['rainfall']} mm
        """
        folium.CircleMarker(
            location=(row["lat"], row["lon"]),
            radius=5,
            color="green",
            fill=True,
            fill_color="green",
            fill_opacity=0.6,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width=800, height=600)

else:
    st.warning("No data available for selected filters.")

# -----------------------
# Data Table & Download
# -----------------------
st.subheader("Filtered Data")
st.dataframe(df)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_tree_planting.csv", "text/csv")
