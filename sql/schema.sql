-- =====================================================================
-- Dhaka Air Quality Analytics - Database Schema
-- Database: PostgreSQL (ANSI SQL compatible with MySQL 8.0+)
-- Target Schema: Dimension & Fact tables for Power BI and Analytics
-- =====================================================================

-- Drop tables if they already exist (in reverse order of foreign keys)
DROP TABLE IF EXISTS fact_air_quality_readings CASCADE;
DROP TABLE IF EXISTS dim_stations CASCADE;
DROP TABLE IF EXISTS dim_dates CASCADE;
DROP TABLE IF EXISTS staging_air_quality_raw CASCADE;

-- ---------------------------------------------------------------------
-- 1. Staging Table: Raw ingestion table
-- ---------------------------------------------------------------------
CREATE TABLE staging_air_quality_raw (
    reading_raw_id          SERIAL PRIMARY KEY,
    raw_timestamp           VARCHAR(100),
    raw_station             VARCHAR(100),
    raw_latitude            VARCHAR(50),
    raw_longitude           VARCHAR(50),
    raw_pm25                VARCHAR(50),
    raw_pm10                VARCHAR(50),
    raw_no2                 VARCHAR(50),
    raw_so2                 VARCHAR(50),
    raw_co                  VARCHAR(50),
    raw_o3                  VARCHAR(50),
    raw_aqi                 VARCHAR(50),
    raw_dominant_pollutant  VARCHAR(50),
    raw_temperature         VARCHAR(50),
    raw_humidity            VARCHAR(50),
    raw_source              VARCHAR(100),
    ingestion_timestamp     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- 2. Dimension Table: Monitoring Stations (dim_stations)
-- ---------------------------------------------------------------------
CREATE TABLE dim_stations (
    station_id              VARCHAR(50) PRIMARY KEY,        -- e.g., 'us_embassy_dhaka', 'cams_darus_salam', 'cams_firmgate'
    station_name            VARCHAR(100) NOT NULL,          -- Descriptive name
    city                    VARCHAR(50) DEFAULT 'Dhaka',
    division                VARCHAR(50) DEFAULT 'Dhaka',
    country                 VARCHAR(50) DEFAULT 'Bangladesh',
    latitude                NUMERIC(9, 6) NOT NULL,
    longitude               NUMERIC(9, 6) NOT NULL,
    elevation_m             NUMERIC(6, 2),
    station_type            VARCHAR(50),                    -- 'Diplomatic/Urban', 'CAMS_Urban_Commercial', 'CAMS_Residential'
    operator                VARCHAR(100),                   -- 'US Department of State / AirNow', 'DoE Bangladesh'
    source_network          VARCHAR(100) NOT NULL           -- 'AirNow', 'DoE CAMS', 'OpenAQ'
);

-- ---------------------------------------------------------------------
-- 3. Dimension Table: Date & Calendar (dim_dates)
-- ---------------------------------------------------------------------
CREATE TABLE dim_dates (
    date_key                INTEGER PRIMARY KEY,            -- Format: YYYYMMDD
    full_date               DATE NOT NULL UNIQUE,
    year                    SMALLINT NOT NULL,
    quarter                 SMALLINT NOT NULL,
    month                   SMALLINT NOT NULL,
    month_name              VARCHAR(20) NOT NULL,
    month_short             CHAR(3) NOT NULL,
    week_of_year            SMALLINT NOT NULL,
    day_of_month            SMALLINT NOT NULL,
    day_of_week             SMALLINT NOT NULL,              -- 1 (Sunday) to 7 (Saturday) or ISO 1-7
    day_name                VARCHAR(20) NOT NULL,
    is_weekend              BOOLEAN NOT NULL,               -- In Bangladesh, Friday & Saturday are official weekends
    season_name             VARCHAR(20) NOT NULL,           -- 'Winter', 'Pre-Monsoon', 'Monsoon', 'Post-Monsoon'
    season_order            SMALLINT NOT NULL               -- 1: Winter, 2: Pre-Monsoon, 3: Monsoon, 4: Post-Monsoon
);

-- ---------------------------------------------------------------------
-- 4. Fact Table: Cleaned Air Quality Readings (fact_air_quality_readings)
-- ---------------------------------------------------------------------
CREATE TABLE fact_air_quality_readings (
    reading_id              BIGSERIAL PRIMARY KEY,
    timestamp_local         TIMESTAMP WITHOUT TIME ZONE NOT NULL, -- Standardized to Asia/Dhaka (UTC+6)
    timestamp_utc           TIMESTAMP WITH TIME ZONE NOT NULL,
    date_key                INTEGER NOT NULL REFERENCES dim_dates(date_key),
    station_id              VARCHAR(50) NOT NULL REFERENCES dim_stations(station_id),
    hour_of_day             SMALLINT NOT NULL CHECK (hour_of_day BETWEEN 0 AND 23),
    
    -- Pollutant Concentrations (µg/m³ for PM and standard mass concentrations)
    pm25                    NUMERIC(8, 2),                  -- PM2.5 in µg/m³
    pm10                    NUMERIC(8, 2),                  -- PM10 in µg/m³
    no2                     NUMERIC(8, 2),                  -- NO2 in µg/m³ or ppb
    so2                     NUMERIC(8, 2),                  -- SO2 in µg/m³ or ppb
    co                      NUMERIC(8, 2),                  -- CO in mg/m³ or ppm
    o3                      NUMERIC(8, 2),                  -- O3 in µg/m³ or ppb
    
    -- Calculated Air Quality Index & Classifications
    aqi                     INTEGER,                        -- Calculated Air Quality Index (0 - 500+)
    aqi_category            VARCHAR(50),                    -- 'Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'
    dominant_pollutant      VARCHAR(20),                    -- 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3'
    
    -- Exceedance Threshold Flags
    exceeds_who_pm25_daily  BOOLEAN,                        -- Daily avg > 15 µg/m³ (WHO 2021 AQG)
    exceeds_bd_pm25_daily   BOOLEAN,                        -- Daily avg > 65 µg/m³ (BD ECR 1997/2005) or 35 µg/m³ (ECR 2022 draft/revision)
    
    -- Meteorological Covariates
    temperature_c           NUMERIC(5, 2),                  -- Ambient Temperature (°C)
    humidity_pct            NUMERIC(5, 2),                  -- Relative Humidity (%)
    
    -- Data Lineage & Quality Tracking
    source                  VARCHAR(100) NOT NULL,          -- Provenance identifier
    qc_flag                 VARCHAR(20) DEFAULT 'VALID',    -- 'VALID', 'SUSPECT', 'OUTLIER', 'CALIBRATION'
    
    -- Constraints
    CONSTRAINT uq_station_timestamp UNIQUE (station_id, timestamp_local)
);

-- ---------------------------------------------------------------------
-- 5. Performance Indexes
-- ---------------------------------------------------------------------
CREATE INDEX idx_readings_date_key ON fact_air_quality_readings(date_key);
CREATE INDEX idx_readings_station ON fact_air_quality_readings(station_id);
CREATE INDEX idx_readings_timestamp ON fact_air_quality_readings(timestamp_local);
CREATE INDEX idx_readings_pm25 ON fact_air_quality_readings(pm25);
CREATE INDEX idx_readings_aqi ON fact_air_quality_readings(aqi);
