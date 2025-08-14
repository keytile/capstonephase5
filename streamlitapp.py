import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Kenya Tree Planting Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #2ca02c;
        color: white;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: 600;
    }
    .footer {
        font-size: 14px;
        color: #6c757d;
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Kenya.svg", width=120)
st.sidebar.title("🌱 Kenya Reforestation")
st.sidebar.markdown("### *Hotspots, Gaps & Equity*")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate",
    ["Overview", "Hotspots Map", "Seasonal Trends", "Equity Rankings", "Recommendations"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("📊 *Data: Kenya Forest Service | 2024*")

# -----------------------------
# Mock Data Loader (Replace with real CSVs in production)
# -----------------------------
@st.cache_data
def load_data():
    # Simulate df_gps.csv with realistic Kenya bounds
    np.random.seed(42)
    n = 76562  # Matches cleaned data count

    # Realistic Kenya lat/lon bounds
    lats = np.random.uniform(-4.1, 5.3, n)
    lons = np.random.uniform(33.0, 42.0, n)

    # Dates over multiple years
    dates = pd.to_datetime(np.random.choice(pd.date_range("2022-01-01", "2024-12-31"), n))
    months = [d.month for d in dates]

    # Seedlings planted (log-normal to match skew)
    seedlings = np.random.lognormal(9, 2, n).astype(int)
    seedlings = np.clip(seedlings, 1, 500000)  # Match outlier filtering

    # Simulate clusters (1,642 total)
    clusters = np.random.randint(0, 1642, n)

    # Assign region: Northern (arid) vs Central/South
    # Using lat < 1.0 AND lon > 38.0 to approximate Turkana, Wajir, Mandera
    region = [
        "Northern" if lat < 1.0 and lon > 38.0 else "Central/South"
        for lat, lon in zip(lats, lons)
    ]

    # Create DataFrame
    df_gps = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'plantingdate': dates,
        'seedlingsplanted': seedlings,
        'month': months,
        'cluster': clusters,
        'region': region
    })

    # Simulate county_tree_planting_summary.csv (Top 10 from PDF)
    equity_data = pd.DataFrame({
        'Rank': range(1, 11),
        'County': ['Samburu', 'Mandera', 'Turkana', 'Kajiado', 'Marsabit',
                   'Wajir', 'Homa Bay', 'Garissa', 'Machakos', 'Nairobi'],
        'Total Trees': [139784, 439514, 544083, 868541, 394670,
                        762708, 2798398, 1962876, 4966774, 17145322],
        'Population (K)': [358, 1026, 985, 1012, 459, 730, 1131, 623, 1421, 4397],
        'Trees per 10K': [3905, 4284, 5524, 8582, 8598, 10448, 24743, 31507, 34953, 38993]
    })

    return df_gps, equity_data

# Load data
df_gps, equity_df = load_data()

# -----------------------------
# Pages
# -----------------------------
if menu == "Overview":
    st.title("🇰🇪 Kenya Tree Planting Dashboard")
    st.markdown("### *A Data-Driven Approach to Equitable Reforestation*")
    st.markdown("""
    This dashboard analyzes **76,562** tree planting events across Kenya to uncover **where**, **when**, and **how fairly** reforestation is happening.

    > 🌱 *Reforestation isn't just about planting trees — it's about planting them where they matter most.*
    """)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Planting Events", "76,562")
    col2.metric("Planting Clusters", "1,642")
    col3.metric("Seasonal Alignment", "78% 🌦️")
    col4.metric("Equity Metric", "Trees per 10K People")

    st.markdown("---")
    st.subheader("Key Insights at a Glance")
    st.markdown("""
    - 🔴 **Urban Bias**: Most planting is near cities (Nairobi, Nakuru, Mombasa).
    - 🟡 **Northern Gaps**: Turkana, Wajir, Mandera are under-planted despite need.
    - 🟢 **Good Timing**: 78% of planting aligns with rainy seasons (MAM & OND).
    - ⚖️ **Equity Surprise**: Arid counties lead in per-capita effort.
    """)

elif menu == "Hotspots Map":
    st.title("📍 Planting Hotspots & Gaps")

    # Show map
    st.map(df_gps[['lat', 'lon']].sample(1000))  # Streamlit native map

    st.markdown("### 🔍 Major Hotspots")
    hotspots = ["Nairobi", "Nakuru", "Kisumu", "Mombasa", "Eldoret", "Thika"]
    st.write("✅ " + " | ".join(hotspots))

    st.markdown("### ⚠️ Critical Gaps")
    gaps = ["**Turkana**", "**Wajir**", "**Mandera**"]
    st.write("🔴 " + " | ".join(gaps) + " — Low access, high ecological need")

    st.markdown("### Cluster Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df_gps['cluster'], bins=50, kde=False, ax=ax, color='green')
    ax.set_title("Spatial Clustering (DBSCAN) - 1,642 Clusters")
    ax.set_xlabel("Cluster ID")
    st.pyplot(fig)

elif menu == "Seasonal Trends":
    st.title("🌧️ Seasonal Alignment Analysis")
    st.markdown("Planting aligned with rainy seasons (MAM: Mar-May, OND: Oct-Dec) has higher survival.")

    # Monthly trend
    monthly = df_gps.groupby('month').size()
    fig = px.bar(monthly, x=monthly.index, y=monthly.values,
                 labels={'x': 'Month', 'y': 'Number of Planting Events'},
                 title="Monthly Planting Activity")
    fig.add_vrect(x0=2.5, x1=5.5, fillcolor="lightblue", opacity=0.3, line_width=0, annotation_text="MAM Rainy")
    fig.add_vrect(x0=9.5, x1=12.5, fillcolor="lightblue", opacity=0.3, line_width=0, annotation_text="OND Rainy")
    st.plotly_chart(fig)

    st.markdown("### 📊 Performance Summary")
    col1, col2 = st.columns(2)
    col1.metric("Planting in Rainy Seasons", "78% ✅")
    col2.metric("Needs Improvement", "22% ⚠️")

    st.markdown("📌 *Recommendation: Enforce planting calendars aligned with MAM & OND.*")

elif menu == "Equity Rankings":
    st.title("⚖️ County Equity Rankings")
    st.markdown("Measuring **trees per 10,000 people** reveals true impact beyond volume.")

    st.dataframe(
        equity_df.style.format({
            'Total Trees': '{:,}',
            'Population (K)': '{:.0f}',
            'Trees per 10K': '{:.0f}'
        }).background_gradient(subset=['Trees per 10K'], cmap='Greens'),
        hide_index=True
    )

    fig = px.bar(equity_df, x='County', y='Trees per 10K', color='Trees per 10K',
                 color_continuous_scale='greens',
                 title="Equity: Trees Planted per 10,000 People")
    st.plotly_chart(fig)

    st.markdown("💡 **Insight**: Nairobi ranks 10th in equity despite planting the most trees — population dilutes per-capita impact.")

elif menu == "Recommendations":
    st.title("🚀 Recommendations & Next Steps")
    st.markdown("### Based on data-driven insights")

    recs = [
        ("🚐 Deploy Mobile Nurseries", "Target Turkana, Wajir, Mandera to close spatial gaps"),
        ("📅 Enforce Seasonal Calendars", "Align all planting with MAM & OND rainy seasons"),
        ("📊 Adopt Per-Capita Metrics", "Use 'trees per 10K people' for fair benchmarking"),
        ("🖥️ Build a Dashboard", "Real-time tracking of hotspots, gaps, and timing"),
        ("🌱 Track Survival & Species", "Improve data collection for long-term impact"),
        ("🤝 Empower Communities", "Scale up engagement in high-effort arid counties")
    ]

    for emoji, text in recs:
        st.markdown(f"- {emoji} **{text}**")

    st.markdown("---")
    st.markdown("### 🎯 Transformative Impact")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Targeted Action", "✓")
    col2.metric("📈 Higher Survival", "✓")
    col3.metric("⚖️ Fair Distribution", "✓")
    col4.metric("👥 Stakeholder Empowerment", "✓")

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer">
    Kenya Tree Planting Initiative • 2024 • Data Source: Kenya Forest Service & County Governments
</div>
""", unsafe_allow_html=True)
