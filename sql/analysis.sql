-- =====================================================================
-- Dhaka Air Quality Analytics - Analytical SQL Script
-- File: sql/analysis.sql
-- Target Engines: PostgreSQL 14+, ANSI SQL compatible (MySQL 8.0+, SQLite)
-- =====================================================================

-- =====================================================================
-- SECTION 1: DATA QUALITY & INTEGRITY CHECKS
-- =====================================================================

-- Query 1.1: Null counts and completeness per analytical column
-- Purpose: Verify completeness of pollutant readings and ensure no null primary keys exist
SELECT 
    COUNT(*) AS total_rows,
    COUNT(reading_id) AS non_null_ids,
    COUNT(*) - COUNT(pm25) AS pm25_null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(pm25)) / COUNT(*), 2) AS pm25_null_pct,
    COUNT(*) - COUNT(aqi_epa_2024) AS aqi_null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(aqi_epa_2024)) / COUNT(*), 2) AS aqi_null_pct,
    COUNT(*) - COUNT(timestamp_local) AS timestamp_null_count
FROM fact_air_quality_hourly;

-- Query 1.2: Check for duplicate timestamps per monitoring station
-- Purpose: Confirm strict 1-to-1 uniqueness constraint on (station_id, timestamp_local)
SELECT 
    station_id,
    timestamp_local,
    COUNT(*) AS occurrence_count
FROM fact_air_quality_hourly
GROUP BY station_id, timestamp_local
HAVING COUNT(*) > 1;

-- =====================================================================
-- SECTION 2: OVERALL & STATION-LEVEL AQI METRICS
-- =====================================================================

-- Query 2.1: Overall PM2.5 summary metrics across the entire observation period
-- Purpose: Compute population-level mean, median approximation, std, min, and max PM2.5
SELECT 
    COUNT(*) AS total_valid_days,
    ROUND(AVG(pm25_mean), 2) AS overall_mean_pm25,
    ROUND(MIN(pm25_mean), 2) AS overall_min_pm25,
    ROUND(MAX(pm25_mean), 2) AS overall_max_pm25,
    ROUND(STDDEV(pm25_mean), 2) AS overall_std_pm25
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY';

-- Query 2.2: Multi-station CAMS ranking by Average AQI
-- Purpose: Rank all Continuous Air Monitoring Stations across Dhaka and Bangladesh by mean AQI
SELECT 
    station_id,
    station_name,
    COUNT(*) AS valid_readings_count,
    ROUND(AVG(aqi), 1) AS mean_aqi,
    ROUND(MIN(aqi), 1) AS min_aqi,
    ROUND(MAX(aqi), 1) AS max_aqi
FROM fact_case_cams_daily
WHERE aqi IS NOT NULL
GROUP BY station_id, station_name
HAVING COUNT(*) >= 100
ORDER BY mean_aqi DESC;

-- =====================================================================
-- SECTION 3: TEMPORAL DISAGGREGATION (MONTHLY & SEASONAL)
-- =====================================================================

-- Query 3.1: Monthly mean PM2.5 and AQI profile
-- Purpose: Uncover annual sinusoidal cycle across calendar months (January to December)
SELECT 
    month,
    CASE month
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month_name,
    COUNT(*) AS total_compliant_days,
    ROUND(AVG(pm25_mean), 2) AS mean_pm25,
    ROUND(MIN(pm25_mean), 2) AS min_pm25,
    ROUND(MAX(pm25_mean), 2) AS max_pm25,
    ROUND(AVG(aqi_epa_2024), 1) AS mean_aqi_epa_2024
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY'
GROUP BY month
ORDER BY month ASC;

-- Query 3.2: Seasonal AQI metrics and standard exceedance breakdown
-- Purpose: Quantify seasonal disparity between Winter, Pre-Monsoon, Monsoon, and Post-Monsoon
SELECT 
    season,
    COUNT(*) AS season_days,
    ROUND(AVG(pm25_mean), 2) AS mean_pm25,
    ROUND(MIN(pm25_mean), 2) AS min_pm25,
    ROUND(MAX(pm25_mean), 2) AS max_pm25,
    ROUND(AVG(aqi_epa_2024), 1) AS mean_aqi_epa_2024,
    SUM(CASE WHEN exceeds_who_2021 = TRUE THEN 1 ELSE 0 END) AS days_exceeding_who,
    ROUND(100.0 * SUM(CASE WHEN exceeds_who_2021 = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS who_exceed_pct,
    SUM(CASE WHEN exceeds_bd_2022 = TRUE THEN 1 ELSE 0 END) AS days_exceeding_bd_standard,
    ROUND(100.0 * SUM(CASE WHEN exceeds_bd_2022 = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS bd_exceed_pct
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY'
GROUP BY season
ORDER BY mean_pm25 DESC;

-- =====================================================================
-- SECTION 4: EXTREME POLLUTION EPISODES & TOP N DAYS
-- =====================================================================

-- Query 4.1: Top 15 most polluted days in Dhaka history
-- Purpose: Isolate peak acute exposure events for public health impact evaluation
SELECT 
    date,
    year,
    month,
    season,
    pm25_mean,
    aqi_epa_2024,
    category_epa_2024,
    valid_hours
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY'
ORDER BY pm25_mean DESC
LIMIT 15;

-- =====================================================================
-- SECTION 5: ADVANCED WINDOW FUNCTIONS
-- =====================================================================

-- Query 5.1: 7-Day Centered Rolling Average Concentration
-- Purpose: Smooth high-frequency day-to-day noise to reveal medium-term synoptic trends
SELECT 
    date,
    season,
    pm25_mean,
    ROUND(AVG(pm25_mean) OVER (
        ORDER BY date 
        ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ), 2) AS rolling_7day_mean_pm25,
    ROUND(AVG(pm25_mean) OVER (
        ORDER BY date 
        ROWS BETWEEN 14 PRECEDING AND 15 FOLLOWING
    ), 2) AS rolling_30day_mean_pm25
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY'
ORDER BY date ASC;

-- Query 5.2: Year-over-Year (YoY) Change using LAG() Window Function
-- Purpose: Calculate annual percentage change in mean PM2.5 across complete years
WITH annual_metrics AS (
    SELECT 
        year,
        COUNT(*) AS valid_days_in_year,
        ROUND(AVG(pm25_mean), 2) AS annual_mean_pm25,
        ROUND(AVG(aqi_epa_2024), 1) AS annual_mean_aqi,
        SUM(CASE WHEN exceeds_bd_2022 = TRUE THEN 1 ELSE 0 END) AS bd_exceed_days
    FROM fact_air_quality_daily
    WHERE qc_flag = 'VALID_DAY' AND year BETWEEN 2016 AND 2020
    GROUP BY year
)
SELECT 
    year,
    valid_days_in_year,
    annual_mean_pm25,
    LAG(annual_mean_pm25, 1) OVER (ORDER BY year) AS prev_year_mean_pm25,
    ROUND(annual_mean_pm25 - LAG(annual_mean_pm25, 1) OVER (ORDER BY year), 2) AS abs_yoy_change_ugm3,
    ROUND(100.0 * (annual_mean_pm25 - LAG(annual_mean_pm25, 1) OVER (ORDER BY year)) / 
          LAG(annual_mean_pm25, 1) OVER (ORDER BY year), 2) AS yoy_change_pct,
    bd_exceed_days,
    ROUND(100.0 * bd_exceed_days / valid_days_in_year, 2) AS bd_exceed_pct
FROM annual_metrics
ORDER BY year ASC;

-- =====================================================================
-- SECTION 6: STATUTORY EXCEEDANCE & HEALTH BENCHMARKS
-- =====================================================================

-- Query 6.1: Overall Exceedance Counts against WHO 2021 & Bangladesh S.R.O 255/2022
-- Purpose: Quantify regulatory compliance gap across the entire 5-year observation record
SELECT 
    COUNT(*) AS total_compliant_days,
    SUM(CASE WHEN pm25_mean > 15.0 THEN 1 ELSE 0 END) AS who_2021_exceed_days,
    ROUND(100.0 * SUM(CASE WHEN pm25_mean > 15.0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS who_2021_exceed_pct,
    SUM(CASE WHEN pm25_mean > 65.0 THEN 1 ELSE 0 END) AS bd_2022_exceed_days,
    ROUND(100.0 * SUM(CASE WHEN pm25_mean > 65.0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS bd_2022_exceed_pct
FROM fact_air_quality_daily
WHERE qc_flag = 'VALID_DAY';
