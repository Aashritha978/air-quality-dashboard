# 🌫️ Air Quality Analysis Dashboard – Indian Cities

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://air-quality-of-indian-cities.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📊 Live Demo

🔗 **View the live dashboard:** [https://air-quality-of-indian-cities.streamlit.app](https://air-quality-of-indian-cities.streamlit.app)

*(Update this link after deploying to Streamlit Cloud)*

---

## 📌 Overview

An **interactive data dashboard** that analyzes air quality trends across major Indian cities using real-world pollution data from the **Central Pollution Control Board (CPCB)**. This tool helps visualize AQI patterns, track pollutant levels, and identify seasonal trends to better understand India's air pollution crisis.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏙️ **City Selection** | Choose from 25+ Indian cities (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, etc.) |
| 📅 **Date Range Filter** | Analyze data from 2015–2020 with customizable time periods |
| 📈 **AQI Trend Chart** | Interactive line chart with color-coded AQI thresholds (Good → Severe) |
| 🧪 **Pollutant Tracking** | Monitor PM2.5, PM10, NO2, CO, SO2, O3, and more |
| 📊 **Air Quality Distribution** | Bar chart showing frequency of each AQI category |
| 📆 **Monthly & Yearly Trends** | Identify seasonal patterns and year-over-year changes |
| 🏆 **Best & Worst Days** | Find the cleanest and most polluted days for any city |
| 📥 **Data Export** | Download filtered data as CSV for further analysis |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core programming language |
| **Streamlit** | Interactive web dashboard framework |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations |
| **CSV** | Dataset format |

---

## 📁 Dataset

**Source:** Central Pollution Control Board (CPCB), Government of India

**File:** `city_day.csv`

**Time Period:** 2015 – 2020

**Key Columns:**
- `City` – Indian city name
- `Date` – Date of measurement
- `PM2.5`, `PM10`, `NO2`, `NO`, `NH3`, `CO`, `SO2`, `O3` – Pollutant concentrations (µg/m³)
- `AQI` – Air Quality Index value
- `AQI_Bucket` – Category (Good, Satisfactory, Moderate, Poor, Very Poor, Severe)

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8 or higher
- Git (optional)

### Step 1: Clone the repository
```bash
git clone https://github.com/Aashritha978/Air-quality-of-indian-cities.git
cd Air-quality-of-indian-cities
Step 2: Install dependencies
bash
pip install -r requirements.txt
Step 3: Run the dashboard
bash
streamlit run app.py
Step 4: Open your browser
The dashboard will automatically open at http://localhost:8501

📸 Dashboard Preview
AQI Trend with Threshold Lines
Shows AQI over time with color-coded health advisory lines

Pollutant Comparison
Compare average concentrations of different pollutants

Monthly Analysis
Identify seasonal patterns (winter vs summer AQI)

📈 Sample Insights
City	Average AQI	Most Common Category	Peak AQI
Amaravati	95.3	Satisfactory	312 (Very Poor)
Delhi	—	—	—
Mumbai	—	—	—
(Run the dashboard to explore insights for all cities!)

📂 Project Structure
text
Air-quality-of-indian-cities/
│
├── app.py                 # Main Streamlit dashboard code
├── city_day.csv           # Air quality dataset (CPCB)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Files to exclude from GitHub
🌟 Future Improvements
City Comparison – Compare AQI between two cities side-by-side

[️ Geographical Map – India map with AQI overlay for each city

Forecasting – Predict future AQI using time series models (Prophet/ARIMA)

Health Recommendations – Real-time health tips based on current AQI

Real-time API Integration – Fetch live air quality data

Mobile-responsive Design – Optimize for smartphone viewing

👩‍💻 Author
Battaji Aashritha

🔗 GitHub

🔗 LinkedIn (Add your LinkedIn profile link)

🙏 Acknowledgments
Central Pollution Control Board (CPCB) – For making air quality data publicly available

Streamlit – For the amazing framework

Plotly – For interactive visualizations

📝 License
This project is for educational and portfolio purposes. Data belongs to CPCB.

⭐ Show Your Support
If you found this project helpful, please give it a ⭐ on GitHub!

📧 Contact
For questions or feedback, feel free to reach out via GitHub Issues or connect on LinkedIn.

Built with ❤️ using Python and Streamlit

