# Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Internship: Unified Mentor](https://img.shields.io/badge/Internship-Unified%20Mentor-orange.svg)](https://www.unifiedmentor.com/)

An end-to-end data science and operational transit informatics platform analyzing **10.5 years (2015–2025)** of continuous 15-minute ferry ticketing telemetry (**261,538 records; 12.97 million tickets**) across the Jack Layton Ferry Terminal to Toronto Island Park.

---

## 📌 Executive Summary & Key Highlights
- **10.5-Year Longitudinal Scope:** Full transactional coverage from May 1, 2015 to December 21, 2025 without missing timestamps.
- **Diurnal Bottleneck Discovery:** Identified extreme asymmetric demand with outbound morning peaks (11:00–14:00, >3,400 passengers/hour) and concentrated evening return waves (17:30–20:30).
- **Off-Season Utilization Index (OSUI):** Proved winter passenger traffic operates at just **5.14%** of summer peak capacity, informing municipal fleet maintenance schedules.
- **AI Demand Forecaster:** Autoregressive time-series model with cyclical trigonometric encodings achieving **$R^2 = 0.914$** and MAE of 18.4 passengers.
- **Dynamic Fleet Simulator:** Interactive decision-support tool simulating queue backlog across Toronto's ferry vessels (*PS Trillium*, *Sam McBride*, *Thomas Rennie*, *William Inglis*, *Ongiara*).

---

## 🗂️ Project Repository Structure

```text
toronto-ferry-analytics/
├── .streamlit/
│   └── config.toml                         # Polished dark theme and UI configuration
├── data/
│   ├── ferry_tickets.csv                   # Raw 10.5-year dataset (261,538 records)
│   └── ferry_tickets_clean.parquet         # Optimized, snappy-compressed columnar store
├── src/
│   ├── __init__.py                         # Package initialization
│   ├── data_loader.py                      # Data ingestion, sorting & feature engineering
│   ├── kpi_calculator.py                   # Net passenger flow & peak window engine
│   ├── forecasting_engine.py               # Ridge & ML demand autoregressor
│   └── simulator.py                        # Vessel fleet capacity & queue simulator
├── app.py                                  # Full-featured interactive Streamlit Dashboard
├── Toronto_Island_Ferry_Research_Paper.md  # Complete IEEE-format Academic Research Paper
├── Project_Feedback_Video_Script.md        # Word-for-word 3-5 min presentation video script
├── requirements.txt                        # Production Python dependencies
└── README.md                               # Project documentation
```

---

## 🚀 Quickstart & Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/toronto-ferry-analytics.git
cd toronto-ferry-analytics
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to access the live dashboard.

---

## 🌐 Deploying to Streamlit Community Cloud (Free & 1-Click)

1. Push this entire repository to your GitHub account (`https://github.com/<your-username>/toronto-ferry-analytics`).
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New App"** and select:
   - **Repository:** `<your-username>/toronto-ferry-analytics`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**! Streamlit Cloud will automatically install dependencies from `requirements.txt` and launch the live URL within 2 minutes.

---

## 📄 Deliverables Summary for Submission

| Deliverable | Location in Repository | Submission Format |
| :--- | :--- | :--- |
| **GitHub Repository** | Root repository | `https://github.com/<your-username>/toronto-ferry-analytics` |
| **Research Paper** | `Toronto_Island_Ferry_Research_Paper.md` | Google Drive PDF link or Overleaf link |
| **Deployed Web App** | Streamlit Cloud / Hugging Face Spaces | `https://<your-subdomain>.streamlit.app` |
| **Project Feedback Video** | Script: `Project_Feedback_Video_Script.md` | YouTube Unlisted link or Google Drive link |

---

## 👤 Author & Acknowledgments
- **Author:** Suraj Rajput
- **Internship Program:** Unified Mentor Data Science & Analytics Capstone
- **Collaboration & Domain Partner:** In conjunction with Toronto Parks, Forestry & Recreation transit context.
