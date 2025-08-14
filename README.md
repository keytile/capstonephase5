# 🌱 Kenya Tree Planting Analysis  
### *Hotspots, Gaps & Seasonal Alignment*  
*A Data-Driven Approach to Equitable Reforestation*  

---

## 📌 Overview 
This Jupyter notebook presents a comprehensive spatial and temporal analysis of tree planting activities across Kenya, leveraging GPS-tagged field data and county-level summaries to uncover **where**, **when**, and **how equitably** reforestation is happening.

Built for the **Kenya Forest Service** and county development partners, this project transforms raw planting data into actionable insights—guiding smarter, fairer, and ecologically aligned reforestation strategies.

> 🔍 **Key Question**: Are we planting trees where they matter most?

---

## 🧩 Key Objectives  
✅ Map planting **hotspots and gaps**  
✅ Assess **seasonal alignment** with rainy periods (MAM & OND)  
✅ Benchmark counties by **equity** — trees per 10,000 people  
✅ Deliver **data-driven recommendations** for policy and field action  

---

## 📦 Data Sources  
| Dataset | Description |
|--------|-------------|
| `df_gps.csv` | 76,562 cleaned GPS-tagged planting events (lat, lon, date, seedlings, temp, rainfall) |
| `county_tree_planting_summary.csv` | Aggregated planting stats + 2019 census population for all 47 counties |

🔧 **Features Engineered**:  
- `month` from planting date  
- `cluster` ID via DBSCAN spatial clustering  
- `trees_per_10k` for equity benchmarking  

---

## 🔍 Key Insights  

### 🌺 **Hotspots**  
- **1,642 planting clusters** identified nationwide  
- Top hotspots: **Nairobi, Nakuru, Kisumu, Mombasa, Eldoret, Thika**  
- Strong correlation with **urban centers and transport networks**

### 🗺️ **Spatial Gaps**  
- Critical under-planting in **arid northern counties**:  
  🔸 Turkana  🔸 Wajir  🔸 Mandera  
- Low accessibility ≠ low engagement — these regions show **high per-capita effort**

### 🌦️ **Seasonal Alignment**  
- ✅ **78%** of planting occurs during favorable rainy seasons (MAM: Mar–May, OND: Oct–Dec)  
- ⚠️ **22%** still plant in dry periods — risk of low seedling survival

### ⚖️ **Equity Paradox**  
| Rank | County | Trees per 10K People |
|------|--------|-----------------------|
| 1 | Garissa | 31,507 |
| 2 | Machakos | 34,953 |
| 10 | **Nairobi** | **38,993** *(despite highest total trees)* |

👉 Urban areas lead in volume, but **northern counties lead in per-capita equity**

---

## 🛠️ Recommendations  
| Action | Impact |
|-------|--------|
| 🚐 Deploy **mobile nurseries** to northern counties | Close spatial gaps |
| 📅 Enforce **seasonal planting calendars** | Boost seedling survival |
| 📊 Adopt **trees per 10,000 people** metric | Fair, inclusive benchmarking |
| 🖥️ Build a **real-time monitoring dashboard** | Empower decision-makers |

---

## 🚀 Next Steps  
- Integrate **species and survival rate** data  
- Expand community-led monitoring in remote areas  
- Scale insights into national reforestation policy  

---

## 🌍 Conclusion  
> *"Reforestation isn't just about planting trees — it's about planting them where they matter most."*  

This analysis shifts the narrative from **volume to value**, from **counting trees to counting impact**. With targeted action, Kenya can grow a greener, more resilient, and equitable future — one seedling at a time.

---

📁 *Notebook created for the Kenya Tree Planting Initiative • 2025*  
🔐 *Data: GPS & County-Level Aggregates | Tools: Python, GeoPandas, DBSCAN, Matplotlib, Seaborn*