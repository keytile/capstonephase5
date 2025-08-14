import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Kenya Tree Planting (GeoPandas)", layout="wide")
st.title("🌳 Kenya Tree Planting Dashboard — GeoPandas Edition")
st.markdown("Simple app using GeoPandas `.explore()` for interactive mapping.")

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
    df = df[kenya_mask].copy()
    return df

df = load_data()

# -----------------------
# Convert to GeoDataFrame
# -----------------------
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])],
    crs="EPSG:4326"
)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")
season_choice = st.sidebar.radio("Season", ["All", "Rainy", "Dry"], index=0)
rainy_months = {3, 4, 5, 10, 11, 12}
gdf["month"] = gdf["plantingdate"].dt.month
gdf["is_rainy"] = gdf["month"].isin(rainy_months)

if season_choice == "Rainy":
    gdf = gdf[gdf["is_rainy"]]
elif season_choice == "Dry":
    gdf = gdf[~gdf["is_rainy"]]

# -----------------------
# Metrics
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Trees", f"{int(gdf['seedlingsplanted'].sum()):,}")
col2.metric("Records", len(gdf))
rainy_pct = gdf["is_rainy"].mean() * 100 if len(gdf) else 0
col3.metric("Rainy Season %", f"{rainy_pct:.1f}%")

# -----------------------
# Map with GeoPandas
# -----------------------
m = gdf.explore(
    column="seedlingsplanted",
    cmap="YlGn",
    popup=["plantingdate", "seedlingsplanted", "temperature", "rainfall"],
    tiles="CartoDB positron",
    marker_kwds={"radius": 5}
)

# Embed map into Streamlit
from streamlit.components.v1 import html
html(m._repr_html_(), height=600)

# -----------------------
# Data Table
# -----------------------
st.subheader("Filtered Data")
st.dataframe(gdf.drop(columns="geometry"))
csv = gdf.drop(columns="geometry").to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_tree_planting.csv", "text/csv")
