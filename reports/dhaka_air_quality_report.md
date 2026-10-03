# Dhaka Air Quality Analytics: An Empirical Investigation of Particulate Pollution, Regulatory Compliance, and Temporal Dynamics (2016–2021)

**Author:** Senior Data Analyst & Data Visualization Engineer  
**Target Domain:** Dhaka, Bangladesh (`Asia/Dhaka`, UTC+6)  
**Primary Datasets:** U.S. Department of State / AirNow BAM-1020 FEM Monitor & Bangladesh Department of Environment (DoE) CAMS Network  
**Repository:** `dhaka-air-quality-analytics`  
**Date:** October 2026  

---

## Executive Summary

Dhaka, the capital of Bangladesh, ranks consistently among the world's most particulate-polluted megacities. This report provides an independent, empirical analysis of ground-level air quality observations in Dhaka between **January 1, 2016, and June 1, 2021**. Using 44,986 validated hourly readings and 1,781 compliant 24-hour daily measurements from regulatory-grade instrumentation, this study evaluates the true distribution of fine particulate matter ($\text{PM}_{2.5}$), quantifies compliance against statutory benchmarks, assesses the public health impact of the **U.S. EPA May 6, 2024 AQI breakpoint revisions**, and maps spatial disparities across monitoring stations.

### Key Empirical Findings at a Glance
- **Severe Particulate Burden `[Observed]`:** The overall 5-year mean $\text{PM}_{2.5}$ concentration was **$87.52\,\mu\text{g/m}^3$** (median **$61.38\,\mu\text{g/m}^3$**, standard deviation **$65.48\,\mu\text{g/m}^3$**), spanning an extreme range from **$4.83\,\mu\text{g/m}^3$** to **$340.79\,\mu\text{g/m}^3$**.
- **Pervasive Health Benchmark Exceedance `[Observed]`:**
  - **$97.64\%$ of days** (1,739 of 1,781 valid days) exceeded the World Health Organization (WHO) 2021 24-hour guideline ($15.0\,\mu\text{g/m}^3$).
  - **$47.78\%$ of days** (851 of 1,781 valid days) exceeded the national Bangladesh statutory 24-hour limit ($65.0\,\mu\text{g/m}^3$ under S.R.O. 255-Law/2022).
- **Extreme Winter-to-Monsoon Disparity `[Inferred]`:** Winter mean $\text{PM}_{2.5}$ (**$172.84\,\mu\text{g/m}^3$**) was **$5.24$ times higher** than Monsoon mean (**$32.99\,\mu\text{g/m}^3$**), a disparity confirmed statistically significant ($p < 0.001$, Mann-Whitney $U = 240,412.0$). Winter days exceeded the national standard **$97.71\%$** of the time.
- **Impact of Revised 2024 EPA AQI Breakpoints `[Observed]`:** Applying the U.S. EPA revised May 6, 2024 $\text{PM}_{2.5}$ breakpoints nearly doubled the count of **"Hazardous"** days from **41 to 73 days (+78.0%)** and expanded **"Very Unhealthy"** days from **293 to 417 days (+42.3%)**, while clean **"Good"** days contracted from 16 to just 6 days (-62.5%).
- **Nocturnal Diurnal Inversion `[Observed]`:** Hourly pollution peaks at **23:00 BST ($103.90\,\mu\text{g/m}^3$)** and reaches its diurnal trough at **16:00 BST ($58.73\,\mu\text{g/m}^3$)**, a 1.77-fold intra-day ratio.
- **Negligible Weekend Relief `[Observed]`:** Official Bangladesh weekend days (Friday & Saturday, mean **$85.74\,\mu\text{g/m}^3$**) experienced only a **$2.82\%$ reduction** compared to weekdays (**$88.22\,\mu\text{g/m}^3$**), demonstrating that background industrial activity, regional transboundary transport, and seasonal combustion overpower localized commuter traffic reductions.

---

## 1. Analytical Problem & Scope

Particulate air pollution poses severe cardiovascular, respiratory, and economic burdens on Dhaka's ~20 million residents. However, public discussions frequently rely on unverified real-time snapshots, mixed AQI standards, or unstated data cleaning assumptions. This project establishes an authoritative analytical framework to answer 9 primary research questions:

1. What is the empirical distribution of $\text{PM}_{2.5}$ and AQI in Dhaka, and how many days occupy each health category?
2. How does the adoption of the U.S. EPA May 6, 2024 revised AQI standard alter category classification compared to previous standards?
3. What is the magnitude of seasonal variation across Winter, Pre-Monsoon, Monsoon, and Post-Monsoon?
4. How do pollution concentrations fluctuate across hours of the day and days of the week?
5. How do monitoring stations within Dhaka (Darus Salam, Farmgate, Manik Mia Ave) and regional Bangladeshi cities compare?
6. How frequently are the WHO 2021 Air Quality Guidelines and Bangladesh national standards breached?
7. What periods exhibit statistically extreme pollution anomalies?
8. What is the multi-year trajectory across complete calendar years (2016–2020)?
9. What structural and sensor limitations constrain causal attribution?

---

## 2. Dataset Architecture & Primary Provenance

Data was retrieved strictly from primary regulatory and government monitoring networks, with all raw files cryptographically hashed with SHA-256 into [`data/raw/SOURCES.md`](file:///c:/project%2003/dhaka%20air/data/raw/SOURCES.md):

1. **U.S. Department of State / AirNow DOS Network (2016–2021):**
   - **Station Location:** U.S. Embassy Dhaka, Madani Avenue, Baridhara (`23.7979° N, 90.4223° E`).
   - **Instrument:** Met One BAM-1020 (Beta Attenuation Mass Monitor), designated Federal Equivalent Method (FEM) for continuous hourly $\text{PM}_{2.5}$.
   - **Records Ingested:** 44,990 raw hourly observations across 6 annual files.
2. **Bangladesh Department of Environment (DoE) — Clean Air and Sustainable Environment (CASE) CAMS Network:**
   - **Dhaka Stations:** CAMS-1 (Sangsad Bhaban / Manik Mia Ave, Urban Background), CAMS-2 (Farmgate / Commercial Traffic Corridor), CAMS-3 (Darus Salam / Mirpur Industrial Corridor).
   - **Regional Stations:** 13 divisional cities (Gazipur, Narayanganj, Chittagong, Sylhet, Khulna, Rajshahi, Barisal, Savar, Mymensingh, Rangpur, Cumilla, Narsingdi).
   - **Records Ingested:** 24,093 daily bulletin records.

---

## 3. Data Audit, Quality Control & Cleaning Pipeline

The automated cleaning pipeline in [`src/cleaning.py`](file:///c:/project%2003/dhaka%20air/src/cleaning.py) executed rigorous data governance protocols:

### Formal Cleaning Log

| Stage | Issue Detected | Rows Affected | Decision Taken | Technical & Physical Rationale |
| :--- | :--- | :---: | :--- | :--- |
| **Timestamp Normalization** | 8 duplicate timestamps at 03:00 on U.S. DST transition Sundays | 8 | Averaged duplicate pairs into 4 unique hourly records | U.S. central servers mistakenly applied spring-forward clock shifts to an Asia/Dhaka monitor that does not observe DST. |
| **Sentinel Handling** | `-999.0` error codes in `Raw Conc.` | 1,986 | Replaced with `NaN` | AirNow standard flag for unrecorded observations; non-numerical. |
| **Operator QA/QC** | Operator `'Invalid'` QC flags | 159 | Replaced with `NaN` | Recorded tape breaks, flow rate deviations, or maintenance shutdowns. |
| **Zero-Drift Correction** | Negative concentrations ($-15$ to $-1\,\mu\text{g/m}^3$) | 27 | Censored 15 valid small drift values ($-4$ to $-1$) to $0.0\,\mu\text{g/m}^3$; set 12 invalid negatives to `NaN` | BAM-1020 instruments experience baseline zero-drift under high relative humidity clean monsoon spells; reflects clean ambient air within instrument noise tolerance. |
| **Outlier Retention** | Hourly spikes $> 600\,\mu\text{g/m}^3$ (max $985.0\,\mu\text{g/m}^3$) | 33 | Retained 100% of extreme readings | Continuous multi-hour ramps verified real nocturnal winter radiation inversion smog events; deleting would cause downward bias. |
| **Completeness Gate** | Incomplete calendar days ($< 18$ valid hours) | 141 | Retained 1,781 valid days; set 141 incomplete days to `NaN` | Standard EPA/WHO protocol: 24-hr daily averages require $\ge 75\%$ temporal completeness to eliminate diurnal bias. |
| **CAMS Normalization** | 33 location name variants with footnote letters (`Dhakaa`, etc.) | 24,093 | Standardized into 16 canonical stations | Separated Dhaka CAMS 1–3 and canonicalized regional cities. |
| **CAMS Missing Values** | Non-numeric `'DNA'` strings | 4,368 | Parsed as `NaN` and converted AQI to numeric | Signifies sensor outage or missing bulletin transmission. |
| **CAMS Deduplication** | Duplicate station-date bulletin scrapes | 104 | Pruned to first verified record | Enforces relational primary key uniqueness. |

---

## 4. Exploratory Data Analysis & Empirical Findings

### 4.1 Concentration Distribution & Category Breakdown
Across 1,781 compliant days between 2016 and 2021:
- **Mean:** $87.52\,\mu\text{g/m}^3$
- **Median:** $61.38\,\mu\text{g/m}^3$
- **Standard Deviation:** $65.48\,\mu\text{g/m}^3$
- **25th Percentile:** $35.96\,\mu\text{g/m}^3$
- **75th Percentile:** $130.88\,\mu\text{g/m}^3$
- **Interquartile Range (IQR):** $94.92\,\mu\text{g/m}^3$

The distribution exhibits severe positive skewness, driven by persistent winter episodes where daily means routinely exceed $200\,\mu\text{g/m}^3$.

```
AQI Category Distribution under Revised US EPA May 6, 2024 Standards:
  Good (0-50):                     6 days (  0.34%)  ■
  Moderate (51-100):             431 days ( 24.20%)  ████████████
  Unhealthy for Sensitive (101): 379 days ( 21.28%)  ███████████
  Unhealthy (151-200):           475 days ( 26.67%)  █████████████
  Very Unhealthy (201-300):      417 days ( 23.41%)  ████████████
  Hazardous (301+):               73 days (  4.10%)  ██
```

![Daily PM2.5 Distribution and AQI Categories](file:///c:/project%2003/dhaka%20air/images/01_pm25_distribution_and_aqi_categories.png)

---

### 4.2 Impact of US EPA May 6, 2024 AQI Breakpoint Revision
The revision of EPA breakpoints substantially reclassified Dhaka's air quality record:

| Category | US EPA Revised 2024 | US EPA Pre-2024 Classic | Absolute Shift (Days) | Relative Change |
| :--- | :---: | :---: | :---: | :---: |
| **Good** | 6 | 16 | -10 | -62.5% |
| **Moderate** | 431 | 421 | +10 | +2.4% |
| **Unhealthy for Sensitive Groups** | 379 | 379 | 0 | 0.0% |
| **Unhealthy** | 475 | 631 | -156 | -24.7% |
| **Very Unhealthy** | 417 | 293 | +124 | +42.3% |
| **Hazardous** | 73 | 41 | +32 | **+78.0%** |

*Analytical Significance `[Inferred]`:* Lowering the "Very Unhealthy" threshold from $150.5$ to $125.5\,\mu\text{g/m}^3$ and "Hazardous" from $250.5$ to $225.5\,\mu\text{g/m}^3$ reclassified 156 days into higher severity health brackets, accurately warning vulnerable citizens during severe winter episodes.

![Multi-Standard AQI Comparison](file:///c:/project%2003/dhaka%20air/images/02_multi_standard_aqi_comparison.png)

---

### 4.3 Seasonal Cycles & Climatological Drivers
Dhaka's air quality is governed by the South Asian monsoon cycle:

| Season | Valid Days | Mean PM2.5 ($\mu\text{g/m}^3$) | Median PM2.5 | Std Dev | Days > 65 $\mu\text{g/m}^3$ (BD Std) | Days > 15 $\mu\text{g/m}^3$ (WHO) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Winter (Dec–Feb)** | 436 | **$172.84$** | **$167.77$** | $51.09$ | **97.71%** (426 days) | **99.77%** (435 days) |
| **Post-Monsoon (Oct–Nov)**| 266 | **$83.02$** | **$73.40$** | $44.25$ | **60.53%** (161 days) | **97.37%** (259 days) |
| **Pre-Monsoon (Mar–May)** | 525 | **$76.47$** | **$63.00$** | $43.46$ | **47.05%** (247 days) | **99.81%** (524 days) |
| **Monsoon (Jun–Sep)** | 554 | **$32.99$** | **$31.50$** | $13.30$ | **3.07%** (17 days) | **94.04%** (521 days) |

![Seasonal Boxplots](file:///c:/project%2003/dhaka%20air/images/05_season_boxplots.png)
![Monthly Heatmap](file:///c:/project%2003/dhaka%20air/images/04_seasonality_month_year_heatmap.png)

*Key Insights:*
- **The Winter Factor `[Observed]`:** Winter particulate pollution is **5.24 times higher** than Monsoon levels.
- **The Wet Scavenging Hypothesis `[Hypothesis]`:** Monsoon precipitation effectively scrubs coarse and fine particulates via precipitation wash-out, combined with a higher planetary boundary layer that dilutes surface emissions. Conversely, dry winter conditions with low surface wind speeds, nocturnal temperature inversions, and seasonal brick kiln operations trap particulate matter near breathing height.

---

### 4.4 Diurnal (Hourly) & Day-of-Week Dynamics

- **Diurnal Curve `[Observed]`:**
  - Peak Concentration: **23:00 BST ($103.90\,\mu\text{g/m}^3$)**, remaining elevated through 02:00 BST ($102.7\,\mu\text{g/m}^3$).
  - Secondary Morning Rush Peak: **09:00 BST ($88.64\,\mu\text{g/m}^3$)**.
  - Trough Concentration: **16:00 BST ($58.73\,\mu\text{g/m}^3$)**.
  - Peak-to-Trough Ratio: **$1.77\times$**.

![Diurnal Hour of Day Profile](file:///c:/project%2003/dhaka%20air/images/06_diurnal_hour_of_day_profile.png)

*Hypothesized Mechanisms `[Hypothesis]`:* The nocturnal peak is driven by two coinciding phenomena: (1) atmospheric boundary-layer compression following sunset creating strong ground radiation inversions, and (2) municipal traffic restrictions allowing heavy diesel commercial trucks to enter Dhaka metropolitan boundaries only after 22:00 BST.

- **Day of Week Profile `[Observed]`:**
  - Weekday Mean (Sun–Thu): **$88.22\,\mu\text{g/m}^3$**
  - Weekend Mean (Fri–Sat): **$85.74\,\mu\text{g/m}^3$**
  - Difference: **$-2.82\%$** (Statistically insignificant).
  - *Inference `[Inferred]`:* Particulate pollution in Dhaka is overwhelmingly dominated by regional background emissions, transboundary transport, continuous industrial operations, and meteorological stagnation rather than localized light passenger vehicle commuting.

---

### 4.5 Spatial Station Variations (Dhaka & Regional Bangladesh)
Analyzing 23,751 records from the Bangladesh Department of Environment CAMS network reveals notable intra-urban and inter-regional variation:

- **Intra-Dhaka Gradient `[Observed]`:**
  1. **Dhaka CAMS-3 (Darus Salam, Mirpur):** Mean AQI = **$179.6$**, Max = **$524$** (Unhealthy / Heavy transit corridor)
  2. **Dhaka CAMS-2 (Farmgate / BARC):** Mean AQI = **$169.2$**, Max = **$557$** (Commercial intersection)
  3. **Dhaka CAMS-1 (Manik Mia Ave):** Mean AQI = **$158.2$**, Max = **$477$** (Urban background / Parliament)
- **Regional Bangladesh Gradient `[Observed]`:**
  - Northern and Industrial Corridor Stations: **Rangpur (Mean AQI 191.8)**, **Mymensingh (184.3)**, **Narayanganj (179.5)**, and **Gazipur (165.2)** exhibit pollution levels comparable to or exceeding central Dhaka.
  - Southern / Coastal / North-Eastern Stations: **Sylhet (Mean AQI 105.3)**, **Khulna (120.9)**, and **Chittagong (121.9)** exhibit noticeably cleaner ambient air quality.

![Station and City Comparison](file:///c:/project%2003/dhaka%20air/images/09_station_city_comparison_cams.png)

---

### 4.6 Statistical Anomaly Detection
Applying a 30-day centered rolling z-score ($|z| > 2.5$) identified **27 acute anomaly days** (25 extreme positive spikes and 2 negative dips):

- **Top Severe Spikes `[Observed]`:**
  1. `2021-01-19`: $340.8\,\mu\text{g/m}^3$ ($z = +2.89$, Winter peak episode)
  2. `2021-03-16`: $320.3\,\mu\text{g/m}^3$ ($z = +2.63$, Late Pre-Monsoon surge)
  3. `2021-03-21`: $318.4\,\mu\text{g/m}^3$ ($z = +2.56$, Dust storm / pre-monsoon convective event)
  4. `2020-02-20`: $273.8\,\mu\text{g/m}^3$ ($z = +2.67$, Winter inversion episode)
  5. `2016-12-24`: $273.1\,\mu\text{g/m}^3$ ($z = +2.55$, Winter inversion episode)

![Anomaly Detection Rolling Z-Score](file:///c:/project%2003/dhaka%20air/images/10_anomaly_detection_rolling_zscore.png)

---

### 4.7 Year-over-Year Trajectory (2016–2020)
Examining complete calendar years:

| Year | Compliant Days | Annual Mean PM2.5 ($\mu\text{g/m}^3$) | Annual Median PM2.5 | Days > 65 $\mu\text{g/m}^3$ | Exceedance Rate (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2016** | 305 | **$67.90$** | $49.17$ | 108 | 35.41% |
| **2017** | 352 | **$79.71$** | $55.60$ | 144 | 40.91% |
| **2018** | 268 | **$100.31$** | $84.39$ | 150 | **55.97%** |
| **2019** | 359 | **$86.38$** | $65.92$ | 183 | 50.97% |
| **2020** | 352 | **$84.63$** | $57.44$ | 159 | 45.17% |

*Inference `[Inferred]`:* Annual $\text{PM}_{2.5}$ peaked in 2018 ($100.31\,\mu\text{g/m}^3$). While 2020 showed a modest decline to $84.63\,\mu\text{g/m}^3$ (likely influenced by COVID-19 pandemic mobility restrictions during March–May 2020), every complete calendar year exceeded the Bangladesh annual standard ($15.0\,\mu\text{g/m}^3$) by $4.5\times$ to $6.7\times$, and exceeded the WHO annual guideline ($5.0\,\mu\text{g/m}^3$) by $13.6\times$ to $20.1\times$.

---

## 5. Relational SQL Pipeline & Analytics Engine

The accompanying SQL suite [`sql/analysis.sql`](file:///c:/project%2003/dhaka%20air/sql/analysis.sql) and embedded database [`data/dhaka_air_quality.db`](file:///c:/project%2003/dhaka%20air/data/dhaka_air_quality.db) implement enterprise-grade analytical transformations:

1. **Window-Based 7-Day & 30-Day Smoothing:** Eliminates synoptic fluctuations to identify persistent stagnation cycles.
2. **Year-over-Year Growth with `LAG()`:** Computes exact percentage shifts between adjacent years without recursive joins.
3. **Data Governance & Uniqueness Verification:** Asserts zero duplicate keys on `(station_id, timestamp_local)` and validates column-level null rates.

---

## 6. Power BI Dashboard Architecture

The dashboard design in [`powerbi/POWER_BI_SPEC.md`](file:///c:/project%2003/dhaka%20air/powerbi/POWER_BI_SPEC.md) adheres to enterprise business intelligence standards:

- **Dimensional Star Schema:** Fact tables (`fact_air_quality_daily`, `fact_case_cams_daily`) linked in 1-to-many single-directional relationships to dimension tables (`dim_dates`, `dim_stations`).
- **Dynamic DAX Measures Library:** Implemented in [`powerbi/measures.dax`](file:///c:/project%2003/dhaka%20air/powerbi/measures.dax), preventing hard-coded numbers and supporting dynamic multi-slicer filtering.
- **Visual Canvas Previews:**
  - Executive Overview: [`images/11_powerbi_dashboard_overview.png`](file:///c:/project%2003/dhaka%20air/images/11_powerbi_dashboard_overview.png)
  - Trends & Seasonality: [`images/12_powerbi_dashboard_trends.png`](file:///c:/project%2003/dhaka%20air/images/12_powerbi_dashboard_trends.png)

![Power BI Overview Preview](file:///c:/project%2003/dhaka%20air/images/11_powerbi_dashboard_overview.png)

---

## 7. Analytical Limitations & Epistemic Boundaries

To maintain scientific integrity, several critical limitations must be explicitly recognized:

1. **Spatial Representativeness of Primary Monitor:** The primary continuous hourly time series originates from the U.S. Embassy in Baridhara. This site represents an upscale, planned residential and diplomatic microenvironment with higher tree canopy cover and lower local industrial density than western or southern Dhaka (e.g., Hazaribagh, Postogola, Tejgaon). City-wide exposure is likely higher than recorded here.
2. **Single Criteria Pollutant Focus:** The continuous U.S. Embassy monitor measures $\text{PM}_{2.5}$ exclusively. Multi-pollutant gaseous parameters ($\text{NO}_2, \text{SO}_2, \text{CO}, \text{O}_3$) and coarse fraction ($\text{PM}_{10}$) were available only as daily aggregated indices from the CAMS network. As a result, $\text{PM}_{2.5}$ is observed as the dominant particulate driver, but gaseous oxidant interactions cannot be modeled at hourly resolution.
3. **Absence of Direct Emission Source Monitoring:** Ambient sensors measure concentration, not emissions. Plausible causes—including fixed-chimney brick kilns in peri-urban clusters, construction dust, road re-suspension, two-stroke engines, and transboundary biomass plumes from the Indo-Gangetic Plain—remain **`[Hypothesis]`** until verified by isotopic source apportionment or chemical speciation.
4. **Discontinuation of U.S. Embassy Public Transmission:** Public streaming from the U.S. State Department AirNow monitor ended in 2021 due to program funding constraints, limiting continuous hourly FEM observations to mid-2021.

---

## 8. Epistemic Findings Register

| Epistemic Class | Finding Statement | Statistical & Empirical Evidence |
| :--- | :--- | :--- |
| **`[Observed]`** | 5-year mean $\text{PM}_{2.5}$ was $87.52\,\mu\text{g/m}^3$ (median $61.38\,\mu\text{g/m}^3$). | Computed directly from 1,781 compliant 24-hr daily averages. |
| **`[Observed]`** | WHO 2021 24-hr guideline exceeded on 97.64% of days. | 1,739 of 1,781 valid calendar days $> 15.0\,\mu\text{g/m}^3$. |
| **`[Observed]`** | Bangladesh S.R.O. 255/2022 24-hr standard exceeded on 47.78% of days. | 851 of 1,781 valid calendar days $> 65.0\,\mu\text{g/m}^3$. |
| **`[Observed]`** | US EPA 2024 breakpoint revision increased Hazardous days from 41 to 73 (+78.0%). | Reclassification based on 40 CFR Part 58 Appendix G revised breakpoints. |
| **`[Observed]`** | Diurnal peak occurs at 23:00 BST ($103.90\,\mu\text{g/m}^3$); trough at 16:00 BST ($58.73\,\mu\text{g/m}^3$). | Hourly BAM-1020 time-series average across 44,986 hours. |
| **`[Observed]`** | Darus Salam CAMS-3 exhibited the highest mean AQI (179.6) among Dhaka stations. | CAMS bulletin records (N=696 days). |
| **`[Inferred]`** | Winter pollution is 5.24-fold higher than Monsoon pollution. | Mann-Whitney $U = 240,412.0, p < 0.001$. |
| **`[Inferred]`** | Commuter traffic reductions on weekends produce negligible particulate relief (-2.82%). | Weekday mean $88.22\,\mu\text{g/m}^3$ vs Weekend mean $85.74\,\mu\text{g/m}^3$. |
| **`[Hypothesis]`** | Winter particulate surges are driven by seasonal brick kiln operations and nocturnal temperature inversions. | Plausible physical mechanism; ambient sensors measure concentration, not emission flux. |
| **`[Hypothesis]`** | Late-night concentration spike (22:00–02:00 BST) is caused by commercial heavy truck entry into Dhaka. | Aligns with municipal traffic curfew regulations, but unconfirmed by vehicle counters. |

---

## 9. Conclusions & Strategic Recommendations

1. **Air Pollution in Dhaka is an Environmental Emergency:** With nearly 98% of days breaching WHO health guidelines and almost half exceeding national statutory limits, acute particulate exposure is an endemic, year-round reality.
2. **Seasonal Interventions Must Take Priority:** Regulatory action must focus heavily on the October–February window. Because winter pollution is over 5-fold higher than monsoon levels, targeted seasonal controls on peri-urban brick kilns, unpaved road dust suppression, and biomass burning will yield the highest marginal health benefits.
3. **Adopt Modern AQI Breakpoints Nationally:** Bangladesh DoE should harmonize its public AQI reporting with the revised U.S. EPA 2024 breakpoints. Under current outdated thresholds, citizens receive "Unhealthy" or "Moderate" alerts on days when exposure is clinically hazardous.
4. **Expand Multi-Pollutant Speciation Monitoring:** Regulatory authorities must deploy continuous chemical speciation monitors (organic carbon, elemental carbon, sulfates, nitrates) to move from empirical hypotheses to causal emission attribution.
