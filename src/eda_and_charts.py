"""
Dhaka Air Quality Analytics - Exploratory Data Analysis & Visualization Pipeline
Module: src/eda_and_charts.py

Computes exact statistical metrics from verified processed datasets and
generates publication-quality charts saved to images/.
All findings are classified as [Observed], [Inferred], or [Hypothesis].
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
IMAGES_DIR = PROJECT_ROOT / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Visual styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 15
plt.rcParams['figure.titleweight'] = 'bold'

# Standard Color Palette for AQI Categories
AQI_COLORS = {
    'Good': '#00e400',
    'Moderate': '#ffff00',
    'Unhealthy for Sensitive Groups': '#ff7e00',
    'Caution': '#ff7e00',
    'Unhealthy': '#ff0000',
    'Very Unhealthy': '#8f3f97',
    'Hazardous': '#7e0023',
    'Extremely Unhealthy': '#7e0023'
}

def load_data():
    df_daily = pd.read_csv(PROCESSED_DIR / "dhaka_pm25_daily_cleaned.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    
    df_hourly = pd.read_csv(PROCESSED_DIR / "dhaka_pm25_hourly_cleaned.csv")
    df_hourly['datetime_local'] = pd.to_datetime(df_hourly['datetime_local'])
    
    df_case = pd.read_csv(PROCESSED_DIR / "case_cams_daily_cleaned.csv")
    df_case['date'] = pd.to_datetime(df_case['date'])
    
    return df_daily, df_hourly, df_case


def run_eda_and_generate_charts():
    df_daily, df_hourly, df_case = load_data()
    df_valid_daily = df_daily[df_daily['qc_flag'] == 'VALID_DAY'].copy()
    
    metrics = {}
    
    # -------------------------------------------------------------
    # 1. Overall Statistics (PM2.5 ug/m3)
    # -------------------------------------------------------------
    total_days = len(df_daily)
    valid_days = len(df_valid_daily)
    pm25_mean = df_valid_daily['pm25_mean'].mean()
    pm25_std = df_valid_daily['pm25_mean'].std()
    pm25_median = df_valid_daily['pm25_mean'].median()
    pm25_min = df_valid_daily['pm25_mean'].min()
    pm25_max = df_valid_daily['pm25_mean'].max()
    pm25_q25 = df_valid_daily['pm25_mean'].quantile(0.25)
    pm25_q75 = df_valid_daily['pm25_mean'].quantile(0.75)
    pm25_iqr = pm25_q75 - pm25_q25
    
    metrics['overall'] = {
        'total_calendar_days': int(total_days),
        'valid_compliant_days': int(valid_days),
        'completeness_pct': round((valid_days / total_days) * 100, 2),
        'date_start': str(df_daily['date'].min().date()),
        'date_end': str(df_daily['date'].max().date()),
        'mean_pm25': round(pm25_mean, 2),
        'std_pm25': round(pm25_std, 2),
        'median_pm25': round(pm25_median, 2),
        'min_pm25': round(pm25_min, 2),
        'max_pm25': round(pm25_max, 2),
        'q25_pm25': round(pm25_q25, 2),
        'q75_pm25': round(pm25_q75, 2),
        'iqr_pm25': round(pm25_iqr, 2)
    }
    
    # -------------------------------------------------------------
    # 2. Exceedance Analysis (WHO 2021 vs Bangladesh 2022)
    # -------------------------------------------------------------
    who_exceed_count = (df_valid_daily['pm25_mean'] > 15.0).sum()
    who_exceed_pct = (who_exceed_count / valid_days) * 100.0
    
    bd_exceed_count = (df_valid_daily['pm25_mean'] > 65.0).sum()
    bd_exceed_pct = (bd_exceed_count / valid_days) * 100.0
    
    metrics['exceedance'] = {
        'who_2021_limit_ugm3': 15.0,
        'who_exceed_days': int(who_exceed_count),
        'who_exceed_pct': round(who_exceed_pct, 2),
        'bd_2022_limit_ugm3': 65.0,
        'bd_exceed_days': int(bd_exceed_count),
        'bd_exceed_pct': round(bd_exceed_pct, 2)
    }
    
    # -------------------------------------------------------------
    # 3. AQI Category Distributions (EPA 2024 vs EPA Pre-2024 vs BD DoE)
    # -------------------------------------------------------------
    cat_order_epa = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
    cat_order_bd = ['Good', 'Moderate', 'Caution', 'Unhealthy', 'Very Unhealthy', 'Extremely Unhealthy']
    
    epa_2024_counts = df_valid_daily['category_epa_2024'].value_counts()
    epa_pre2024_counts = df_valid_daily['category_epa_pre2024'].value_counts()
    bd_doe_counts = df_valid_daily['category_bd_doe'].value_counts()
    
    metrics['aqi_categories'] = {
        'epa_2024': {cat: int(epa_2024_counts.get(cat, 0)) for cat in cat_order_epa},
        'epa_pre2024': {cat: int(epa_pre2024_counts.get(cat, 0)) for cat in cat_order_epa},
        'bd_doe': {cat: int(bd_doe_counts.get(cat, 0)) for cat in cat_order_bd}
    }
    
    # -------------------------------------------------------------
    # 4. Seasonal Disaggregation
    # -------------------------------------------------------------
    season_order = ['Winter', 'Pre-Monsoon', 'Monsoon', 'Post-Monsoon']
    season_stats = {}
    for s in season_order:
        s_df = df_valid_daily[df_valid_daily['season'] == s]
        season_stats[s] = {
            'days': int(len(s_df)),
            'mean_pm25': round(s_df['pm25_mean'].mean(), 2),
            'median_pm25': round(s_df['pm25_mean'].median(), 2),
            'std_pm25': round(s_df['pm25_mean'].std(), 2),
            'min_pm25': round(s_df['pm25_mean'].min(), 2),
            'max_pm25': round(s_df['pm25_mean'].max(), 2),
            'exceed_who_pct': round((s_df['pm25_mean'] > 15.0).mean() * 100, 2),
            'exceed_bd_pct': round((s_df['pm25_mean'] > 65.0).mean() * 100, 2)
        }
    metrics['seasonality'] = season_stats
    
    # -------------------------------------------------------------
    # 5. Diurnal (Hourly) & Day-of-Week Disaggregation
    # -------------------------------------------------------------
    valid_hourly = df_hourly[df_hourly['pm25'].notna()].copy()
    hourly_means = valid_hourly.groupby('hour')['pm25'].mean()
    hourly_medians = valid_hourly.groupby('hour')['pm25'].median()
    
    peak_hour = int(hourly_means.idxmax())
    peak_val = round(hourly_means.max(), 2)
    lowest_hour = int(hourly_means.idxmin())
    lowest_val = round(hourly_means.min(), 2)
    
    metrics['diurnal'] = {
        'peak_hour_local_bst': peak_hour,
        'peak_mean_pm25': peak_val,
        'lowest_hour_local_bst': lowest_hour,
        'lowest_mean_pm25': lowest_val,
        'diurnal_ratio_peak_to_lowest': round(peak_val / lowest_val, 2)
    }
    
    # Day of week
    dow_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    dow_means = df_valid_daily.groupby('day_of_week')['pm25_mean'].mean().reindex(dow_order)
    weekend_mean = df_valid_daily[df_valid_daily['is_weekend']]['pm25_mean'].mean()
    weekday_mean = df_valid_daily[~df_valid_daily['is_weekend']]['pm25_mean'].mean()
    
    metrics['day_of_week'] = {
        'weekday_mean_pm25': round(weekday_mean, 2),
        'weekend_mean_pm25': round(weekend_mean, 2),
        'weekend_difference_pct': round(((weekend_mean - weekday_mean) / weekday_mean) * 100, 2)
    }
    
    # -------------------------------------------------------------
    # 6. Year-over-Year Complete Years (2016 - 2020)
    # -------------------------------------------------------------
    complete_years = [2016, 2017, 2018, 2019, 2020]
    yoy_stats = {}
    for yr in complete_years:
        yr_df = df_valid_daily[df_valid_daily['year'] == yr]
        yoy_stats[yr] = {
            'valid_days': int(len(yr_df)),
            'annual_mean_pm25': round(yr_df['pm25_mean'].mean(), 2),
            'annual_median_pm25': round(yr_df['pm25_mean'].median(), 2),
            'exceed_bd_days': int((yr_df['pm25_mean'] > 65.0).sum()),
            'exceed_bd_pct': round((yr_df['pm25_mean'] > 65.0).mean() * 100, 2)
        }
    metrics['year_over_year'] = yoy_stats
    
    # -------------------------------------------------------------
    # 7. Anomaly Detection (Rolling 30-Day Z-Score)
    # -------------------------------------------------------------
    df_valid_daily_sorted = df_valid_daily.sort_values('date').copy()
    rolling_mean = df_valid_daily_sorted['pm25_mean'].rolling(30, min_periods=14, center=True).mean()
    rolling_std = df_valid_daily_sorted['pm25_mean'].rolling(30, min_periods=14, center=True).std()
    df_valid_daily_sorted['z_score'] = (df_valid_daily_sorted['pm25_mean'] - rolling_mean) / rolling_std
    
    anomalies = df_valid_daily_sorted[df_valid_daily_sorted['z_score'].abs() > 2.5]
    top_positive_anomalies = anomalies[anomalies['z_score'] > 2.5].sort_values('pm25_mean', ascending=False)
    
    metrics['anomalies'] = {
        'total_flagged_anomalies': int(len(anomalies)),
        'positive_spikes_count': int((anomalies['z_score'] > 2.5).sum()),
        'negative_dips_count': int((anomalies['z_score'] < -2.5).sum()),
        'top_spikes': [
            {
                'date': str(r['date'].date()),
                'pm25_mean': round(r['pm25_mean'], 1),
                'z_score': round(r['z_score'], 2),
                'season': r['season']
            }
            for _, r in top_positive_anomalies.head(5).iterrows()
        ]
    }
    
    # -------------------------------------------------------------
    # 8. Multi-Station CASE Project Comparison
    # -------------------------------------------------------------
    case_summary = df_case.groupby(['station_id', 'station_name'])['aqi'].agg(['count', 'mean', 'median', 'max']).reset_index()
    case_summary = case_summary[case_summary['count'] >= 100].sort_values('mean', ascending=False)
    metrics['stations'] = [
        {
            'station_id': r['station_id'],
            'station_name': r['station_name'],
            'readings': int(r['count']),
            'mean_aqi': round(r['mean'], 1),
            'median_aqi': round(r['median'], 1),
            'max_aqi': round(r['max'], 1)
        }
        for _, r in case_summary.iterrows()
    ]
    
    # =============================================================
    # GENERATE PUBLICATION-GRADE CHARTS
    # =============================================================
    print("Generating publication charts in images/...")
    
    # CHART 1: PM2.5 Distribution and AQI Categories (EPA 2024)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.histplot(df_valid_daily['pm25_mean'], kde=True, color='#1f77b4', bins=40, ax=ax1)
    ax1.axvline(15.0, color='#d62728', linestyle='--', linewidth=2, label='WHO 2021 24h Guideline (15 µg/m³)')
    ax1.axvline(65.0, color='#ff7f0e', linestyle='--', linewidth=2, label='Bangladesh S.R.O 255/2022 Limit (65 µg/m³)')
    ax1.axvline(pm25_median, color='#2ca02c', linestyle='-', linewidth=2, label=f'Observed Median ({pm25_median:.1f} µg/m³)')
    ax1.set_title('Daily PM2.5 Concentration Distribution (Dhaka)', pad=12)
    ax1.set_xlabel('Daily Mean PM2.5 (µg/m³)')
    ax1.set_ylabel('Day Count')
    ax1.legend(frameon=True)
    
    # Category Bar Chart
    cat_counts = df_valid_daily['category_epa_2024'].value_counts().reindex(cat_order_epa).fillna(0)
    palette = [AQI_COLORS[c] for c in cat_order_epa]
    bars = ax2.bar(cat_counts.index, cat_counts.values, color=palette, edgecolor='black', linewidth=0.8)
    ax2.set_title('Days by AQI Category (US EPA Revised 2024 Standard)', pad=12)
    ax2.set_xlabel('AQI Health Category')
    ax2.set_ylabel('Number of Days')
    ax2.set_xticklabels(cat_counts.index, rotation=35, ha='right')
    
    for bar in bars:
        h = bar.get_height()
        pct = (h / valid_days) * 100
        ax2.annotate(f'{int(h)}\n({pct:.1f}%)',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, weight='bold')
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "01_pm25_distribution_and_aqi_categories.png", dpi=300)
    plt.close()
    
    # CHART 2: Multi-Standard AQI Category Comparison
    fig, ax = plt.subplots(figsize=(14, 6))
    
    df_cat_comp = pd.DataFrame({
        'US EPA Revised 2024': [epa_2024_counts.get(c, 0) for c in cat_order_epa],
        'US EPA Classic Pre-2024': [epa_pre2024_counts.get(c, 0) for c in cat_order_epa]
    }, index=cat_order_epa)
    
    df_cat_comp.plot(kind='bar', ax=ax, width=0.7, color=['#2b5c8f', '#e67e22'], edgecolor='black', linewidth=0.8)
    ax.set_title('Shift in AQI Health Categories: Revised EPA 2024 vs Pre-2024 Standards', pad=12)
    ax.set_xlabel('AQI Category')
    ax.set_ylabel('Number of Days')
    ax.set_xticklabels(cat_order_epa, rotation=30, ha='right')
    ax.legend(frameon=True)
    
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f'{int(h)}',
                        xy=(p.get_x() + p.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "02_multi_standard_aqi_comparison.png", dpi=300)
    plt.close()
    
    # CHART 3: Long-term Daily Time Series with 30-day Rolling Mean
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.scatter(df_valid_daily['date'], df_valid_daily['pm25_mean'], color='#aec7e8', alpha=0.4, s=12, label='Daily 24h Mean PM2.5')
    rolling_30d = df_valid_daily.set_index('date')['pm25_mean'].rolling('30D').mean()
    ax.plot(rolling_30d.index, rolling_30d.values, color='#1f77b4', linewidth=2.5, label='30-Day Rolling Mean')
    
    ax.axhline(65.0, color='#ff7f0e', linestyle='--', linewidth=1.8, label='Bangladesh Standard (65 µg/m³)')
    ax.axhline(15.0, color='#d62728', linestyle=':', linewidth=1.8, label='WHO 2021 Guideline (15 µg/m³)')
    
    ax.set_title('Long-Term Daily PM2.5 Time Series & 30-Day Trend (2016–2021)', pad=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('PM2.5 Concentration (µg/m³)')
    ax.set_ylim(0, 500)
    ax.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "03_long_term_daily_timeseries_rolling.png", dpi=300)
    plt.close()
    
    # CHART 4: Seasonality Month x Year Heatmap
    pivot_month_year = df_valid_daily.pivot_table(index='year', columns='month', values='pm25_mean', aggfunc='mean')
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_month_year.columns = [month_names[m-1] for m in pivot_month_year.columns]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot_month_year, cmap='YlOrRd', annot=True, fmt='.1f', linewidths=0.8, cbar_kws={'label': 'Mean PM2.5 (µg/m³)'}, ax=ax)
    ax.set_title('Monthly Mean PM2.5 Concentration Heatmap (µg/m³)', pad=12)
    ax.set_xlabel('Month of Year')
    ax.set_ylabel('Year')
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "04_seasonality_month_year_heatmap.png", dpi=300)
    plt.close()
    
    # CHART 5: Seasonal Boxplots
    fig, ax = plt.subplots(figsize=(12, 6))
    season_palette = {'Winter': '#8f3f97', 'Pre-Monsoon': '#ff7f0e', 'Monsoon': '#2ca02c', 'Post-Monsoon': '#1f77b4'}
    sns.boxplot(data=df_valid_daily, x='season', y='pm25_mean', order=season_order, palette=season_palette, ax=ax, showmeans=True,
                meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black", "markersize":"8"})
    ax.axhline(65.0, color='red', linestyle='--', linewidth=1.5, label='Bangladesh Daily Standard (65 µg/m³)')
    ax.axhline(15.0, color='blue', linestyle=':', linewidth=1.5, label='WHO 2021 Guideline (15 µg/m³)')
    ax.set_title('Seasonal PM2.5 Distribution (Boxplot with White Mean Dots)', pad=12)
    ax.set_xlabel('Climatological Season')
    ax.set_ylabel('Daily Mean PM2.5 (µg/m³)')
    ax.legend(frameon=True)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "05_season_boxplots.png", dpi=300)
    plt.close()
    
    # CHART 6: Diurnal (Hour of Day) Profile
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(hourly_means.index, hourly_means.values, marker='o', linewidth=2.5, color='#d62728', label='Mean PM2.5 by Hour')
    ax.plot(hourly_medians.index, hourly_medians.values, marker='s', linewidth=2.0, color='#1f77b4', linestyle='--', label='Median PM2.5 by Hour')
    ax.set_title('Diurnal PM2.5 Profile (Asia/Dhaka BST Time)', pad=12)
    ax.set_xlabel('Hour of Day (00:00 to 23:00 BST)')
    ax.set_ylabel('PM2.5 (µg/m³)')
    ax.set_xticks(range(0, 24))
    ax.legend(frameon=True)
    
    # Annotate peak and trough
    ax.annotate(f'Peak: {peak_val:.1f} µg/m³\n({peak_hour:02d}:00 BST)',
                xy=(peak_hour, peak_val), xytext=(peak_hour - 3, peak_val + 10),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                weight='bold', fontsize=9)
    ax.annotate(f'Lowest: {lowest_val:.1f} µg/m³\n({lowest_hour:02d}:00 BST)',
                xy=(lowest_hour, lowest_val), xytext=(lowest_hour + 1, lowest_val - 15),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                weight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "06_diurnal_hour_of_day_profile.png", dpi=300)
    plt.close()
    
    # CHART 7: Day of Week & Weekend Comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_dow = ['#3498db' if d not in ['Friday', 'Saturday'] else '#e74c3c' for d in dow_order]
    bars = ax.bar(dow_order, dow_means.values, color=colors_dow, edgecolor='black', linewidth=0.8)
    ax.set_title('PM2.5 Levels Across Days of Week (Friday-Saturday: Official Bangladesh Weekend)', pad=12)
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Mean PM2.5 (µg/m³)')
    
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, weight='bold')
        
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "07_day_of_week_weekend_profile.png", dpi=300)
    plt.close()
    
    # CHART 8: Exceedance Comparison (WHO vs Bangladesh Standard)
    fig, ax = plt.subplots(figsize=(10, 5))
    standards = ['WHO 2021 Guideline\n(> 15 µg/m³)', 'Bangladesh S.R.O. 255/2022\n(> 65 µg/m³)']
    exceed_rates = [who_exceed_pct, bd_exceed_pct]
    bars = ax.bar(standards, exceed_rates, color=['#c0392b', '#2980b9'], width=0.5, edgecolor='black')
    ax.set_title('Percentage of Days Exceeding Air Quality Benchmarks (2016–2021)', pad=12)
    ax.set_ylabel('Exceedance Rate (% of Valid Days)')
    ax.set_ylim(0, 105)
    
    for bar, count in zip(bars, [who_exceed_count, bd_exceed_count]):
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%\n({count:,} of {valid_days:,} days)',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "08_exceedance_who_vs_bangladesh.png", dpi=300)
    plt.close()
    
    # CHART 9: Multi-Station / City Comparison (CASE Network)
    fig, ax = plt.subplots(figsize=(14, 6))
    top_stations = case_summary.head(10)
    bars = ax.barh(top_stations['station_name'], top_stations['mean'], color='#4a69bd', edgecolor='black', linewidth=0.8)
    ax.set_title('Mean AQI by Station / City (Bangladesh DoE CAMS Network)', pad=12)
    ax.set_xlabel('Mean Air Quality Index (AQI)')
    ax.invert_yaxis()
    
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f'{w:.1f}',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, weight='bold')
        
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "09_station_city_comparison_cams.png", dpi=300)
    plt.close()
    
    # CHART 10: Anomaly Detection Rolling Z-Score
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(df_valid_daily_sorted['date'], df_valid_daily_sorted['z_score'], color='#7f8c8d', linewidth=0.8, alpha=0.7, label='Rolling 30-Day Z-Score')
    ax.axhline(2.5, color='#e74c3c', linestyle='--', linewidth=1.5, label='Positive Anomaly Threshold (+2.5σ)')
    ax.axhline(-2.5, color='#3498db', linestyle='--', linewidth=1.5, label='Negative Anomaly Threshold (-2.5σ)')
    
    # Highlight anomalies
    pos_anom = anomalies[anomalies['z_score'] > 2.5]
    neg_anom = anomalies[anomalies['z_score'] < -2.5]
    ax.scatter(pos_anom['date'], pos_anom['z_score'], color='#e74c3c', s=35, zorder=5, label=f'Extreme Pollution Spikes (N={len(pos_anom)})')
    ax.scatter(neg_anom['date'], neg_anom['z_score'], color='#3498db', s=35, zorder=5, label=f'Clean Spells (N={len(neg_anom)})')
    
    ax.set_title('Statistical Anomaly Detection (Rolling 30-Day Z-Score on Daily PM2.5)', pad=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Standard Deviations (Z-Score)')
    ax.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "10_anomaly_detection_rolling_zscore.png", dpi=300)
    plt.close()
    
    # Save computed metrics to JSON for exact reporting
    import json
    metrics_path = PROCESSED_DIR / "computed_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"All 10 analysis charts generated in {IMAGES_DIR}.")
    print(f"Exact computed metrics written to {metrics_path}.")
    return metrics


if __name__ == "__main__":
    run_eda_and_generate_charts()
