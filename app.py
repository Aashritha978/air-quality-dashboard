import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Air Quality Analysis - Indian Cities",
    page_icon="🌫️",
    layout="wide"
)

# Title and description
st.title("🌫️ Air Quality Analysis for Indian Cities")
st.markdown("*Analyze AQI trends, pollutant levels, and air quality patterns across major Indian cities*")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("city_day.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# City selector
cities = sorted(df['City'].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", cities)

# Date range picker (FIXED - no tuple indexing issue)
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

# Get date range as two separate values
date_tuple = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date range properly (FIX)
if len(date_tuple) == 2:
    start_date, end_date = date_tuple
else:
    start_date = date_tuple[0] if len(date_tuple) > 0 else min_date
    end_date = date_tuple[-1] if len(date_tuple) > 1 else max_date

# Pollutant selector
pollutants = ['PM2.5', 'PM10', 'NO2', 'NO', 'NH3', 'CO', 'SO2', 'O3']
selected_pollutant = st.sidebar.selectbox("Select Pollutant", pollutants)

# Filter data
mask = (df['City'] == selected_city) & (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
df_filtered = df[mask].copy()

# Check if data exists
if df_filtered.empty:
    st.warning(f"No data available for {selected_city} in the selected date range.")
    st.stop()

# --- Key Metrics Row ---
st.subheader(f"📊 Air Quality Summary for {selected_city}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_aqi = df_filtered['AQI'].mean()
    st.metric("Average AQI", f"{avg_aqi:.1f}" if pd.notna(avg_aqi) else "N/A")

with col2:
    max_aqi = df_filtered['AQI'].max()
    st.metric("Max AQI", f"{max_aqi:.0f}" if pd.notna(max_aqi) else "N/A")

with col3:
    if 'AQI_Bucket' in df_filtered.columns:
        common_bucket = df_filtered['AQI_Bucket'].mode().iloc[0] if not df_filtered['AQI_Bucket'].mode().empty else "N/A"
        st.metric("Most Common Air Quality", common_bucket)
    else:
        st.metric("Most Common Air Quality", "N/A")

with col4:
    total_days = len(df_filtered)
    st.metric("Total Days Analyzed", total_days)

st.markdown("---")

# --- Row 1: AQI Trend and Pollutant Trend ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 AQI Trend in {selected_city}")
    if 'AQI' in df_filtered.columns and not df_filtered['AQI'].isna().all():
        fig_aqi = px.line(
            df_filtered,
            x='Date',
            y='AQI',
            title=f"AQI Over Time in {selected_city}",
            labels={'AQI': 'Air Quality Index', 'Date': 'Date'},
            color_discrete_sequence=['#FF6B6B']
        )
        # Add AQI threshold lines
        fig_aqi.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Good (50)")
        fig_aqi.add_hline(y=100, line_dash="dash", line_color="yellow", annotation_text="Moderate (100)")
        fig_aqi.add_hline(y=200, line_dash="dash", line_color="orange", annotation_text="Poor (200)")
        fig_aqi.add_hline(y=300, line_dash="dash", line_color="red", annotation_text="Very Poor (300)")
        fig_aqi.add_hline(y=400, line_dash="dash", line_color="purple", annotation_text="Severe (400)")
        st.plotly_chart(fig_aqi, use_container_width=True)
    else:
        st.info("AQI data not available for this selection")

with col2:
    st.subheader(f"📊 {selected_pollutant} Trend in {selected_city}")
    if selected_pollutant in df_filtered.columns and not df_filtered[selected_pollutant].isna().all():
        fig_poll = px.line(
            df_filtered,
            x='Date',
            y=selected_pollutant,
            title=f"{selected_pollutant} Concentration Over Time",
            labels={selected_pollutant: f'{selected_pollutant} (µg/m³)', 'Date': 'Date'},
            color_discrete_sequence=['#4ECDC4']
        )
        st.plotly_chart(fig_poll, use_container_width=True)
    else:
        st.info(f"{selected_pollutant} data not available for this selection")

st.markdown("---")

# --- Row 2: AQI Distribution ---
st.subheader(f"📊 Air Quality Distribution in {selected_city}")

col1, col2 = st.columns(2)

with col1:
    if 'AQI_Bucket' in df_filtered.columns:
        bucket_counts = df_filtered['AQI_Bucket'].value_counts().reset_index()
        bucket_counts.columns = ['AQI_Bucket', 'Count']
        fig_bucket = px.bar(
            bucket_counts,
            x='AQI_Bucket',
            y='Count',
            title="AQI Category Distribution",
            color='AQI_Bucket',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_bucket, use_container_width=True)
    else:
        st.info("AQI_Bucket data not available")

with col2:
    if 'AQI' in df_filtered.columns:
        fig_hist = px.histogram(
            df_filtered,
            x='AQI',
            nbins=30,
            title="AQI Value Distribution",
            labels={'AQI': 'Air Quality Index'},
            color_discrete_sequence=['#95E77E']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# --- Row 3: Pollutant Comparison ---
st.subheader(f"🔬 Average Pollutant Levels in {selected_city}")

pollutants_avg = {}
for p in pollutants:
    if p in df_filtered.columns:
        avg_val = df_filtered[p].mean()
        if pd.notna(avg_val) and avg_val > 0:
            pollutants_avg[p] = avg_val

if pollutants_avg:
    avg_df = pd.DataFrame(list(pollutants_avg.items()), columns=['Pollutant', 'Average Value (µg/m³)'])
    fig_avg = px.bar(
        avg_df,
        x='Pollutant',
        y='Average Value (µg/m³)',
        title="Average Pollutant Concentrations",
        color='Pollutant',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_avg, use_container_width=True)
else:
    st.info("No pollutant data available for comparison")

st.markdown("---")

# --- Row 4: Monthly Analysis ---
st.subheader(f"📅 Monthly Average AQI in {selected_city}")

if 'AQI' in df_filtered.columns:
    df_filtered['Year-Month'] = df_filtered['Date'].dt.strftime('%Y-%m')
    monthly_avg = df_filtered.groupby('Year-Month')['AQI'].mean().reset_index()
    
    fig_monthly = px.line(
        monthly_avg,
        x='Year-Month',
        y='AQI',
        title="Monthly Average AQI Trend",
        labels={'AQI': 'Average AQI', 'Year-Month': 'Month'},
        markers=True,
        color_discrete_sequence=['#FFA07A']
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# --- Row 5: Yearly Comparison ---
st.subheader(f"📆 Year-over-Year AQI Comparison for {selected_city}")

if 'AQI' in df_filtered.columns:
    df_filtered['Year'] = df_filtered['Date'].dt.year
    yearly_avg = df_filtered.groupby('Year')['AQI'].mean().reset_index()
    
    fig_yearly = px.bar(
        yearly_avg,
        x='Year',
        y='AQI',
        title="Yearly Average AQI",
        labels={'AQI': 'Average AQI', 'Year': 'Year'},
        color='AQI',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

st.markdown("---")

# --- Row 6: Best and Worst Days ---
st.subheader(f"🏆 Best & Worst Air Quality Days in {selected_city}")

col1, col2 = st.columns(2)

with col1:
    if 'AQI' in df_filtered.columns and not df_filtered['AQI'].isna().all():
        best_day = df_filtered.loc[df_filtered['AQI'].idxmin()]
        st.metric(
            "Best Air Quality Day",
            f"{best_day['Date'].strftime('%Y-%m-%d')}",
            f"AQI: {best_day['AQI']:.0f}"
        )

with col2:
    if 'AQI' in df_filtered.columns and not df_filtered['AQI'].isna().all():
        worst_day = df_filtered.loc[df_filtered['AQI'].idxmax()]
        st.metric(
            "Worst Air Quality Day",
            f"{worst_day['Date'].strftime('%Y-%m-%d')}",
            f"AQI: {worst_day['AQI']:.0f}"
        )

st.markdown("---")

# --- Row 7: Raw Data (Expandable) ---
with st.expander("📋 View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download button
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download filtered data as CSV",
        data=csv,
        file_name=f"{selected_city}_air_quality_data.csv",
        mime="text/csv"
    )

# --- Footer ---
st.markdown("---")
st.markdown("""
### 💡 AQI Reference Guide

| AQI Range | Air Quality Category | Health Impact |
|-----------|---------------------|---------------|
| 0 - 50 | Good | Minimal impact |
| 51 - 100 | Satisfactory | Minor breathing discomfort for sensitive people |
| 101 - 200 | Moderate | Breathing discomfort for people with lung disease |
| 201 - 300 | Poor | Breathing discomfort for most people |
| 301 - 400 | Very Poor | Respiratory illness on prolonged exposure |
| 401 - 500 | Severe | Affects healthy people and seriously impacts those with diseases |

*Data source: CPCB (Central Pollution Control Board)*
""")