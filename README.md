# Dhaka Air Quality Analytics 🇧🇩 💨

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database: SQLite / PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-336791.svg)](https://www.postgresql.org/)
[![Power BI Dashboard](https://img.shields.io/badge/Visualization-Power%20BI-F2C811.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data Integrity: SHA-256 Verified](https://img.shields.io/badge/Data%20Integrity-SHA--256%20Verified-brightgreen.svg)](data/raw/SOURCES.md)

An end-to-end, portfolio-grade environmental data analytics project examining fine particulate matter ($\text{PM}_{2.5}$) and Air Quality Index (AQI) dynamics in Dhaka, Bangladesh (2016–2021). Built strictly with verified primary observations, zero synthetic rows, and full scientific rigor.

---

## 📌 Project Summary & Problem Statement

Dhaka, home to over 20 million residents, regularly experiences acute particulate air pollution. While public headlines frequently report episodic spikes, long-term empirical distributions, seasonal dynamics, and the impact of evolving international standards are rarely evaluated under strict data engineering standards.

This repository provides an independent, reproducible investigation of ground-level air quality observations in Dhaka:
- **Temporal Depth:** 44,986 continuous hourly records across 1,922 calendar days (2016–2021).
- **Quality Gate:** 1,781 calendar days meeting or exceeding the **$\ge 75\%$ temporal completeness threshold** (at least 18 valid hours/day).
- **Standards Benchmarked:** Revised **U.S. EPA May 6, 2024 AQI Breakpoints** vs Classic Pre-2024 Breakpoints, **WHO 2021 Global Air Quality Guidelines** ($15\,\mu\text{g/m}^3$), and Bangladesh **S.R.O. 255-Law/2022** national standards ($65\,\mu\text{g/m}^3$).
- **Multi-Station Scope:** Comparison of U.S. Embassy FEM monitor with the Bangladesh Department of Environment (DoE) CAMS multi-station network across Dhaka (Manik Mia Ave, Farmgate, Darus Salam) and 13 divisional cities.

---

## 📊 Key Findings & Visual Highlights

All analytical findings are classified under strict epistemic standards:
- **`[Observed]`**: Directly measured in the dataset.
- **`[Inferred]`**: Statistically derived relationships supported by numerical tests.
- **`[Hypothesis]`**: Plausible external explanation not directly measured by the sensor instruments.

### 1. Pervasive Benchmark Breaches & Concentration Distribution `[Observed]`
- **5-Year Mean $\text{PM}_{2.5}$:** **$87.52\,\mu\text{g/m}^3$** (Median **$61.38\,\mu\text{g/m}^3$**, Std Dev **$65.48\,\mu\text{g/m}^3$**).
- **WHO 2021 Exceedance Rate:** **$97.64\%$ of days** (1,739 of 1,781 compliant days) breached the 24-hr guideline ($15.0\,\mu\text{g/m}^3$).
- **Bangladesh Standard Exceedance Rate:** **$47.78\%$ of days** (851 of 1,781 compliant days) breached the statutory limit ($65.0\,\mu\text{g/m}^3$).

![PM2.5 Distribution and AQI Categories](images/01_pm25_distribution_and_aqi_categories.png)

---

### 2. Extreme Seasonal Disparity `[Inferred]`
- **Winter Factor:** Winter mean concentration (**$172.84\,\mu\text{g/m}^3$**) is **$5.24$ times higher** than Monsoon mean (**$32.99\,\mu\text{g/m}^3$**), confirmed statistically significant ($p < 0.001$, Mann-Whitney $U = 240,412.0$).
- **Winter Severity:** During winter months (Dec–Feb), **$97.71\%$ of days** exceed the national 24-hr threshold ($65\,\mu\text{g/m}^3$).

![Seasonal Boxplots](images/05_season_boxplots.png)

---

### 3. Impact of U.S. EPA May 6, 2024 Breakpoint Revision `[Observed]`
- Lowering the "Very Unhealthy" threshold from $150.5$ to $125.5\,\mu\text{g/m}^3$ and "Hazardous" from $250.5$ to $225.5\,\mu\text{g/m}^3$ caused a massive category reclassification:
  - **"Hazardous" Days:** Nearly doubled from **41 to 73 days (+78.0%)**.
  - **"Very Unhealthy" Days:** Increased from **293 to 417 days (+42.3%)**.
  - **Clean "Good" Days:** Contracted from 16 to just **6 days (-62.5%)**.

![Multi-Standard AQI Comparison](images/02_multi_standard_aqi_comparison.png)

---

### 4. Diurnal (Hourly) Inversion & Negligible Weekend Relief `[Observed]`
- **Diurnal Curve:** Peaks at **23:00 BST ($103.90\,\mu\text{g/m}^3$)** and reaches its trough at **16:00 BST ($58.73\,\mu\text{g/m}^3$)** ($1.77\times$ ratio).
- **Weekend Effect:** Weekday mean ($88.22\,\mu\text{g/m}^3$) vs official Bangladesh weekend mean ($85.74\,\mu\text{g/m}^3$) differs by only **$-2.82\%$**, proving that background regional emissions and nocturnal atmospheric inversions dominate over light passenger vehicle traffic.

![Diurnal Hour of Day Profile](images/06_diurnal_hour_of_day_profile.png)

---

## 📈 Power BI Interactive Dashboard Architecture

The dashboard model is implemented in [`powerbi/POWER_BI_SPEC.md`](powerbi/POWER_BI_SPEC.md) using a dimensional Star Schema with dynamic DAX measures in [`powerbi/measures.dax`](powerbi/measures.dax).

![Power BI Executive Overview](images/11_powerbi_dashboard_overview.png)
![Power BI Trends and Seasonality](images/12_powerbi_dashboard_trends.png)

---

## 📁 Repository Structure

```
dhaka-air-quality-analytics/
├── .gitignore                      # Git exclusion rules
├── LICENSE                         # MIT License
├── README.md                       # Comprehensive project documentation
├── requirements.txt                # Pinned Python dependencies
├── data/
│   ├── raw/
│   │   ├── SOURCES.md              # Provenance & SHA-256 checksums
│   │   ├── Dhaka_PM2.5_2016_YTD.csv# AirNow DOS raw 2016
│   │   ├── Dhaka_PM2.5_2017_YTD.csv# AirNow DOS raw 2017
│   │   ├── Dhaka_PM2.5_2018_YTD.csv# AirNow DOS raw 2018
│   │   ├── Dhaka_PM2.5_2019_YTD.csv# AirNow DOS raw 2019
│   │   ├── Dhaka_PM2.5_2020_YTD.csv# AirNow DOS raw 2020
│   │   ├── Dhaka_PM2.5_2021_YTD.csv# AirNow DOS raw 2021
│   │   └── case_data.csv           # Bangladesh DoE CASE daily data
│   ├── processed/
│   │   ├── dhaka_pm25_hourly_cleaned.csv  # 44,986 cleaned hourly rows
│   │   ├── dhaka_pm25_daily_cleaned.csv   # 1,922 daily rows (1,781 compliant)
│   │   ├── case_cams_daily_cleaned.csv    # 23,751 multi-station records
│   │   ├── computed_metrics.json          # Exact empirical metrics
│   │   ├── cleaning_log.csv               # Machine-readable cleaning log
│   │   └── CLEANING_LOG.md                # Markdown audit log table
│   └── dhaka_air_quality.db        # Embedded analytical SQLite database
├── images/                         # 12 publication-grade figures & mockups
├── notebooks/
│   └── dhaka_air_quality_analysis.ipynb # Fully executed, error-free notebook
├── powerbi/
│   ├── POWER_BI_SPEC.md            # Star Schema data model & page layout
│   └── measures.dax                # Production DAX measures library
├── reports/
│   └── dhaka_air_quality_report.md # Full 9-section scientific report
├── sql/
│   ├── schema.sql                  # PostgreSQL / ANSI relational schema
│   ├── analysis.sql                # Analytical queries with window functions
│   └── load_database.py            # Automated database builder
└── src/
    ├── cleaning.py                 # Automated data audit and cleaning pipeline
    └── eda_and_charts.py           # Statistical engine and chart generator
```

---

## 🛠️ Tech Stack & Dependencies

- **Programming & Data Science:** Python 3.10+, Pandas 2.2, NumPy 1.26, SciPy 1.13
- **Visualization:** Matplotlib 3.8, Seaborn 0.13
- **Database & SQL:** PostgreSQL 14+ / SQLite 3, SQLAlchemy 2.0
- **Business Intelligence:** Microsoft Power BI (Star Schema, DAX)
- **Environment & Execution:** Jupyter Notebook, VS Code, Git

---

## 🚀 How to Reproduce (Step-by-Step)

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-username/dhaka-air-quality-analytics.git
cd dhaka-air-quality-analytics

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Ingest and Clean Primary Data
```bash
python src/cleaning.py
```
*Generates cleaned datasets in `data/processed/` and writes `data/processed/CLEANING_LOG.md`.*

### 3. Run EDA & Generate Publication Charts
```bash
python src/eda_and_charts.py
```
*Calculates exact statistics in `data/processed/computed_metrics.json` and renders 10 high-resolution charts in `images/`.*

### 4. Build and Query the Relational Database
```bash
python sql/load_database.py
```
*Initializes `data/dhaka_air_quality.db` and verifies all queries in `sql/analysis.sql`.*

### 5. Run the Interactive Jupyter Notebook
```bash
jupyter lab notebooks/dhaka_air_quality_analysis.ipynb
```
*Executes all cells top-to-bottom with zero errors.*

---

## ⚠️ Analytical Limitations & Sensor Scope

1. **Spatial Representation:** Primary observations originate from the U.S. Embassy monitor in Baridhara (an upscale diplomatic zone). Actual exposure in industrial or dense traffic corridors (Tejgaon, Postogola, Darus Salam) is likely higher.
2. **Criteria Pollutant Scope:** Continuous FEM monitoring was available for $\text{PM}_{2.5}$. Gaseous pollutants ($\text{NO}_2, \text{SO}_2, \text{CO}, \text{O}_3$) were accessible as daily aggregated indices from CAMS bulletins.
3. **No Direct Emission Monitoring:** All pollution sources (brick kilns, vehicle exhaust, construction dust, transboundary transport) remain **`[Hypothesis]`** until verified by isotopic source apportionment or chemical speciation.
4. **Historical Boundary:** Public transmission from the U.S. Department of State monitor ceased in mid-2021 due to program funding constraints.

---

## 📬 Author & Contact

- **Author:** Senior Data Analyst & Data Visualization Engineer
- **Project Domain:** Environmental Data Science, Public Health & Business Intelligence
- **Inquiries:** Open an issue or pull request in this repository.

---

## 📋 Delivery Acceptance Checklist

- [x] **Ground Rule 0 Verified:** Zero synthetic or fabricated rows. Primary source SHA-256 register completed in [`data/raw/SOURCES.md`](data/raw/SOURCES.md).
- [x] **Spec Corrections Applied:** U.S. EPA May 6, 2024 breakpoints declared and compared; Bangladesh S.R.O. 255/2022 limits verified from Gazette text; DoE AQI methodology applied; Physical consistency rule $\text{PM}_{2.5} \le \text{PM}_{10}$ implemented.
- [x] **Data Audit & Cleaning Pipeline:** Automated in [`src/cleaning.py`](src/cleaning.py); cleaning log table generated in [`data/processed/CLEANING_LOG.md`](data/processed/CLEANING_LOG.md).
- [x] **Exploratory Data Analysis:** All 9 research questions answered using exact computed metrics in [`data/processed/computed_metrics.json`](data/processed/computed_metrics.json).
- [x] **Publication Charts:** 12 high-resolution figures generated in [`images/`](images/).
- [x] **Jupyter Notebook:** Verified top-to-bottom execution with 0 errors in [`notebooks/dhaka_air_quality_analysis.ipynb`](notebooks/dhaka_air_quality_analysis.ipynb).
- [x] **Relational SQL Suite:** Staging and Star Schema in [`sql/schema.sql`](sql/schema.sql), analytical window functions in [`sql/analysis.sql`](sql/analysis.sql), embedded database built via [`sql/load_database.py`](sql/load_database.py).
- [x] **Power BI Specification:** Star Schema model documented in [`powerbi/POWER_BI_SPEC.md`](powerbi/POWER_BI_SPEC.md), production DAX library in [`powerbi/measures.dax`](powerbi/measures.dax), canvas mockups in [`images/11_powerbi_dashboard_overview.png`](images/11_powerbi_dashboard_overview.png) and [`images/12_powerbi_dashboard_trends.png`](images/12_powerbi_dashboard_trends.png).
- [x] **Final Scientific Report:** Comprehensive 9-section report in [`reports/dhaka_air_quality_report.md`](reports/dhaka_air_quality_report.md) with strict epistemic labeling (`[Observed]`, `[Inferred]`, `[Hypothesis]`).
- [x] **Repository Documentation:** Production [`README.md`](README.md), [`LICENSE`](LICENSE), and pinned [`requirements.txt`](requirements.txt).
