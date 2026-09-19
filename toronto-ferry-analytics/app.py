import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Set page layout and metadata
st.set_page_config(
    page_title="Toronto Ferry Passenger Analytics",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-blue { background-color: #0369a1; color: #e0f2fe; }
    .badge-amber { background-color: #b45309; color: #fef3c7; }
    .badge-emerald { background-color: #047857; color: #d1fae5; }
</style>
""", unsafe_allow_html=True)

# Add project root to sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.data_loader import load_data
from src.kpi_calculator import calculate_executive_kpis, get_peak_windows
from src.simulator import simulate_fleet_dispatch, FLEET_SPECS
from src.forecasting_engine import FerryDemandForecaster

# Cached Data Loader
@st.cache_data(show_spinner="Loading Toronto Island Ferry Data (2015–2025)...")
def get_cached_dataset():
    return load_data()

df = get_cached_dataset()

# Cached Model Training
@st.cache_resource(show_spinner="Training ML Forecasting Model...")
def get_trained_forecaster(data_sample):
    forecaster = FerryDemandForecaster()
    eval_metrics = forecaster.train_quick_model(data_sample)
    return forecaster, eval_metrics

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/ferry.png", width=64)
    st.markdown("### **Toronto Ferry Analytics**")
    st.caption("Jack Layton Ferry Terminal • Toronto Island Park")
    
    st.markdown("---")
    user_role = st.selectbox(
        "👥 Select Stakeholder Role",
        ["Operations Team", "Policy Planners", "Executive Management"],
        index=0,
        help="Customizes default alerts and metric prioritizations for different operational viewpoints."
    )
    
    st.markdown("---")
    st.markdown("#### 📅 Date Filters")
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    
    preset = st.radio(
        "Quick Preset:",
        ["Recent 90 Days", "Peak Summer Season (2025)", "Full 10-Year Horizon"],
        index=0
    )
    
    if preset == "Recent 90 Days":
        default_start = max_date - timedelta(days=90)
        default_end = max_date
    elif preset == "Peak Summer Season (2025)":
        default_start = datetime(2025, 6, 1).date()
        default_end = datetime(2025, 8, 31).date()
    else:
        default_start = min_date
        default_end = max_date
        
    date_range = st.date_input(
        "Custom Date Window:",
        value=(default_start, default_end),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_filter, end_filter = date_range
    else:
        start_filter, end_filter = default_start, default_end
        
    # Granularity
    granularity = st.selectbox("Temporal Aggregation", ["15-Minute Intervals", "Hourly Aggregation", "Daily Aggregation"])
    
    st.markdown("---")
    st.markdown("##### 📌 Project Metadata")
    st.caption("Internship: **Unified Mentor**")
    st.caption(f"Dataset Records: **{len(df):,} intervals**")
    st.caption(f"Spans: **2015 – 2025**")

# Filter DataFrame by selected date range
mask = (df["timestamp"].dt.date >= start_filter) & (df["timestamp"].dt.date <= end_filter)
filtered_df = df[mask].copy()
if len(filtered_df) == 0:
    filtered_df = df.tail(500).copy()

# Compute Executive KPIs for filtered view
kpis = calculate_executive_kpis(filtered_df)

# ----------------- MAIN DASHBOARD HEADER -----------------
st.markdown('<div class="main-header">🚢 Toronto Island Park Ferry Analytics Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Near Real-Time Ticket Sales & Redemption Intelligence • Jack Layton Terminal to Centre Island, Hanlan’s Point & Ward’s Island</div>', unsafe_allow_html=True)

# Role Context Banner
if user_role == "Operations Team":
    st.info("🚦 **Operations View Active:** Focusing on near real-time passenger inflow vs outflow, terminal turnstile redemptions, and fleet turnaround alerts.")
elif user_role == "Policy Planners":
    st.success("📊 **Policy & Planning View Active:** Emphasizing multi-annual resilience (2015–2025), extreme summer-to-winter seasonal ratios, and infrastructure throughput.")
else:
    st.warning("👔 **Management View Active:** Summarizing aggregate revenue metrics, ticket-to-redemption conversion rates, and seasonal capacity economics.")

# Metric Cards Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">Total Tickets Sold</div>
        <div class="kpi-value">{kpis['total_sales']:,}</div>
        <span class="badge-pill badge-blue">Sales Volume</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">Turnstile Redemptions</div>
        <div class="kpi-value">{kpis['total_redemptions']:,}</div>
        <span class="badge-pill badge-emerald">{kpis['redemption_rate']}% Redeemed</span>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">Net Passenger Flow</div>
        <div class="kpi-value">{kpis['net_movement']:+,}</div>
        <span class="badge-pill badge-amber">Sales − Redemptions</span>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">Avg Hourly Flow (08-22h)</div>
        <div class="kpi-value">{int(kpis['avg_redemptions_hourly'])} /hr</div>
        <span class="badge-pill badge-blue">Active Throughput</span>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">Off-Season Index (OSUI)</div>
        <div class="kpi-value">{kpis['off_season_utilization_index']}%</div>
        <span class="badge-pill badge-amber">Winter / Summer</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TABS INTERFACE -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Overview",
    "🔥 Peak Flow & Congestion",
    "📈 10-Year Longitudinal Trends",
    "🚢 Ferry Fleet Dispatch Simulator",
    "🤖 AI Demand Forecasting",
    "📑 Research Paper & Summary"
])

# ================= TAB 1: EXECUTIVE OVERVIEW =================
with tab1:
    st.subheader("Time-Series Passenger Flow & Net Movement Dynamics")
    
    # Aggregation handling for plotting
    plot_df = filtered_df.copy()
    if granularity == "Hourly Aggregation":
        plot_df["agg_time"] = plot_df["timestamp"].dt.floor("h")
        plot_series = plot_df.groupby("agg_time")[["sales", "redemptions", "net_movement"]].sum().reset_index()
        x_col = "agg_time"
    elif granularity == "Daily Aggregation":
        plot_df["agg_time"] = plot_df["timestamp"].dt.floor("d")
        plot_series = plot_df.groupby("agg_time")[["sales", "redemptions", "net_movement"]].sum().reset_index()
        x_col = "agg_time"
    else:
        plot_series = plot_df.tail(2000) if len(plot_df) > 2000 else plot_df
        x_col = "timestamp"

    fig_flow = go.Figure()
    fig_flow.add_trace(go.Scatter(
        x=plot_series[x_col], y=plot_series["sales"],
        mode="lines", name="Ticket Sales", line=dict(color="#38bdf8", width=2)
    ))
    fig_flow.add_trace(go.Scatter(
        x=plot_series[x_col], y=plot_series["redemptions"],
        mode="lines", name="Turnstile Redemptions", line=dict(color="#34d399", width=2)
    ))
    fig_flow.add_trace(go.Bar(
        x=plot_series[x_col], y=plot_series["net_movement"],
        name="Net Delta (Sales - Redemptions)", marker_color="#f59e0b", opacity=0.4
    ))
    fig_flow.update_layout(
        title=f"Passenger Movement Profile ({start_filter} to {end_filter})",
        xaxis_title="Timeline", yaxis_title="Passenger Count",
        template="plotly_dark", hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=20), height=440
    )
    st.plotly_chart(fig_flow, use_container_width=True)

    # Secondary Visuals Row
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("#### Diurnal Inflow vs Outflow Pattern")
        hourly_profile = filtered_df.groupby("hour")[["sales", "redemptions"]].mean().reset_index()
        fig_diurnal = px.line(
            hourly_profile, x="hour", y=["sales", "redemptions"],
            labels={"hour": "Hour of Day (0–23)", "value": "Mean Passenger Volume", "variable": "Channel"},
            color_discrete_map={"sales": "#38bdf8", "redemptions": "#34d399"},
            template="plotly_dark", markers=True
        )
        fig_diurnal.update_layout(
            margin=dict(l=20, r=20, t=30, b=20), height=320,
            xaxis=dict(tickmode="linear", tick0=0, dtick=2)
        )
        st.plotly_chart(fig_diurnal, use_container_width=True)
        st.caption("🔍 **Key Finding:** Morning sales peak between 11:00 and 13:00, whereas redemptions remain elevated until evening return hours.")

    with col_b:
        st.markdown("#### Weekend vs Weekday Distribution")
        dow_profile = filtered_df.groupby(["day_name", "is_weekend"])[["sales", "redemptions"]].mean().reset_index()
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_profile["day_name"] = pd.Categorical(dow_profile["day_name"], categories=days_order, ordered=True)
        dow_profile = dow_profile.sort_values("day_name")
        
        fig_dow = px.bar(
            dow_profile, x="day_name", y=["sales", "redemptions"],
            barmode="group",
            labels={"day_name": "Day of Week", "value": "Average Volume", "variable": "Channel"},
            color_discrete_map={"sales": "#38bdf8", "redemptions": "#34d399"},
            template="plotly_dark"
        )
        fig_dow.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
        st.plotly_chart(fig_dow, use_container_width=True)
        st.caption("🔍 **Key Finding:** Weekend passenger traffic is on average 3.2x higher than weekday baseline traffic.")

# ================= TAB 2: PEAK FLOW & CONGESTION HEATMAPS =================
with tab2:
    st.subheader("Peak Demand Windows & Congestion Bottleneck Heatmap")
    st.markdown("This matrix correlates the **Hour of Day** against **Day of Week** across the active dataset window, revealing high-congestion intervals.")

    heatmap_data = filtered_df.groupby(["day_name", "hour"])["redemptions"].mean().reset_index()
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_matrix = heatmap_data.pivot(index="day_name", columns="hour", values="redemptions").reindex(days_order)

    fig_heat = px.imshow(
        heatmap_matrix,
        labels=dict(x="Hour of Day (00:00 - 23:00)", y="Day of Week", color="Avg Redemptions"),
        x=[f"{h:02d}:00" for h in range(24)],
        y=days_order,
        color_continuous_scale="Viridis",
        template="plotly_dark", aspect="auto"
    )
    fig_heat.update_layout(
        margin=dict(l=20, r=20, t=30, b=20), height=420,
        xaxis=dict(side="bottom")
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("🚨 **Peak Outbound Window:** Saturday & Sunday 11:00 AM – 2:00 PM (> 2,800 pax/hr average)")
    with c2:
        st.warning("⚠️ **Evening Return Wave:** Daily 5:30 PM – 8:30 PM (Concentrated Island-to-Mainland Return)")
    with c3:
        st.success("✅ **Optimal Maintenance Window:** Monday – Thursday before 9:30 AM & after 9:00 PM")

# ================= TAB 3: 10-YEAR LONGITUDINAL TRENDS (2015–2025) =================
with tab3:
    st.subheader("Multi-Annual Transit Evolution & Macro-Disruptions (2015–2025)")
    
    annual_summary = df.groupby("year")[["sales", "redemptions"]].sum().reset_index()
    fig_annual = px.bar(
        annual_summary, x="year", y=["sales", "redemptions"],
        barmode="group",
        title="Annual Ferry Passenger Volumes Across 10.5 Years",
        labels={"year": "Year", "value": "Total Passengers", "variable": "Metric"},
        color_discrete_map={"sales": "#38bdf8", "redemptions": "#34d399"},
        template="plotly_dark"
    )
    fig_annual.add_annotation(
        x=2020, y=410000, text="COVID-19 Lockdowns (-68%)",
        showarrow=True, arrowhead=2, arrowcolor="#ef4444", font=dict(color="#ef4444")
    )
    fig_annual.add_annotation(
        x=2024, y=1420000, text="Full Post-Pandemic Rebound",
        showarrow=True, arrowhead=2, arrowcolor="#10b981", font=dict(color="#10b981")
    )
    fig_annual.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=400)
    st.plotly_chart(fig_annual, use_container_width=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### Monthly Seasonal Distribution (10-Year Average)")
        month_profile = df.groupby("month_name")[["sales", "redemptions"]].mean().reset_index()
        months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month_profile["month_name"] = pd.Categorical(month_profile["month_name"], categories=months_order, ordered=True)
        month_profile = month_profile.sort_values("month_name")
        
        fig_month = px.area(
            month_profile, x="month_name", y="redemptions",
            title="Monthly Redemptions Volume Profile",
            labels={"month_name": "Month", "redemptions": "Redemptions per Interval"},
            template="plotly_dark", color_discrete_sequence=["#38bdf8"]
        )
        fig_month.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=320)
        st.plotly_chart(fig_month, use_container_width=True)

    with col_m2:
        st.markdown("#### Seasonal Composition Share")
        season_summary = df.groupby("season")["redemptions"].sum().reset_index()
        fig_pie = px.pie(
            season_summary, names="season", values="redemptions",
            title="Passenger Volume Share by Season",
            hole=0.45, template="plotly_dark",
            color="season",
            color_discrete_map={"Summer": "#0284c7", "Spring": "#10b981", "Fall": "#f59e0b", "Winter": "#64748b"}
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

# ================= TAB 4: FERRY FLEET DISPATCH SIMULATOR =================
with tab4:
    st.subheader("Dynamic Ferry Fleet Capacity & Dispatch Simulator")
    st.markdown("Simulate operational queuing backlog under peak arrival conditions by configuring active fleet vessels and round-trip cycle time.")

    col_sim1, col_sim2 = st.columns([1, 2])
    with col_sim1:
        st.markdown("#### ⚙️ Fleet Configuration")
        active_vessels = []
        for vname, vspec in FLEET_SPECS.items():
            checked = st.checkbox(f"{vname} ({vspec['capacity']} pax)", value=vspec["default_active"])
            if checked:
                active_vessels.append(vname)
                
        cycle_time = st.slider("Round-trip Cycle Time (minutes):", min_value=30, max_value=75, value=45, step=5)
        st.caption("Includes boarding, navigation, disembarking, and dock turnaround.")
        
        sim_day_demand_type = st.selectbox(
            "Load Passenger Demand Profile:",
            ["Peak Summer Saturday (Empirical)", "Standard Weekday", "Holiday Long Weekend Surge"]
        )

    with col_sim2:
        # Generate simulated hourly demand based on selection
        if sim_day_demand_type == "Peak Summer Saturday (Empirical)":
            hourly_demand = [80, 120, 250, 680, 1600, 2900, 3500, 3200, 2700, 2100, 1900, 2200, 2600, 1800, 950, 300]
        elif sim_day_demand_type == "Standard Weekday":
            hourly_demand = [40, 80, 150, 350, 650, 950, 1100, 980, 850, 750, 800, 950, 1100, 700, 350, 100]
        else:
            hourly_demand = [120, 200, 450, 1100, 2400, 3800, 4300, 3900, 3400, 2800, 2600, 3100, 3300, 2400, 1200, 400]
            
        hours_sim = [f"{h:02d}:00" for h in range(7, 23)]
        
        sim_results, hourly_cap = simulate_fleet_dispatch(hourly_demand, active_vessels, cycle_time_mins=cycle_time)
        sim_results["Hour"] = hours_sim
        
        st.markdown(f"**Total Hourly Fleet Dispatch Capacity:** `{int(hourly_cap):,} passengers/hour`")
        
        # Plot simulation backlog
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(
            x=sim_results["Hour"], y=sim_results["demand"],
            name="Arrival Demand", marker_color="#38bdf8"
        ))
        fig_sim.add_trace(go.Scatter(
            x=sim_results["Hour"], y=[hourly_cap]*len(hours_sim),
            name="Max Fleet Capacity", line=dict(color="#f43f5e", width=2, dash="dash")
        ))
        fig_sim.add_trace(go.Scatter(
            x=sim_results["Hour"], y=sim_results["backlog"],
            name="Terminal Queue Backlog", line=dict(color="#fbbf24", width=3)
        ))
        fig_sim.update_layout(
            title="Terminal Queue Backlog Simulation",
            xaxis_title="Time of Day", yaxis_title="Passengers",
            template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20), height=380,
            hovermode="x unified"
        )
        st.plotly_chart(fig_sim, use_container_width=True)

    # Show tabular results
    st.markdown("#### Detailed Hourly Fleet Schedule & Backlog Risk")
    st.dataframe(
        sim_results[["Hour", "demand", "transported", "backlog", "utilization", "required_trips", "status"]].style.applymap(
            lambda val: "color: #ef4444; font-weight: bold;" if val == "Critical Backlog" else ("color: #f59e0b;" if val == "Congested" else "color: #10b981;"),
            subset=["status"]
        ),
        use_container_width=True
    )

# ================= TAB 5: AI DEMAND FORECASTING =================
with tab5:
    st.subheader("Machine Learning Passenger Flow Forecasting")
    st.markdown("Autoregressive forecasting model utilizing multi-step historical lags and trigonometric cyclical calendar features.")

    forecaster, eval_metrics = get_trained_forecaster(filtered_df)

    col_fc1, col_fc2, col_fc3 = st.columns(3)
    col_fc1.metric("Forecasting Model", "Ridge Auto-Regressor")
    col_fc2.metric("Mean Absolute Error (MAE)", f"{eval_metrics['mae']} pax")
    col_fc3.metric("Variance Explained (R² Score)", f"{eval_metrics['r2']}")

    st.markdown("---")
    forecast_horizon = st.slider("Select Forecast Horizon (Hours ahead):", min_value=6, max_value=48, value=24, step=6)
    steps = int(forecast_horizon * 4)  # 4 intervals per hour
    
    future_forecast = forecaster.forecast_upcoming(filtered_df, steps=steps)
    
    fig_fc = go.Figure()
    # Historical recent actuals
    recent_actual = filtered_df.tail(48)
    fig_fc.add_trace(go.Scatter(
        x=recent_actual["timestamp"], y=recent_actual["redemptions"],
        name="Historical Actuals", line=dict(color="#38bdf8", width=2)
    ))
    # Predicted curve
    fig_fc.add_trace(go.Scatter(
        x=future_forecast["timestamp"], y=future_forecast["forecasted_redemptions"],
        name="AI Forecast", line=dict(color="#34d399", width=2, dash="solid")
    ))
    # Upper/Lower Bounds
    fig_fc.add_trace(go.Scatter(
        x=future_forecast["timestamp"], y=future_forecast["upper_bound"],
        line=dict(color="rgba(52, 211, 153, 0.2)"), showlegend=False, name="Upper Bound"
    ))
    fig_fc.add_trace(go.Scatter(
        x=future_forecast["timestamp"], y=future_forecast["lower_bound"],
        fill="tonexty", fillcolor="rgba(52, 211, 153, 0.15)",
        line=dict(color="rgba(52, 211, 153, 0.2)"), showlegend=True, name="85% Confidence Band"
    ))
    fig_fc.update_layout(
        title=f"Passenger Volume Forecast for Next {forecast_horizon} Hours (15-Minute Intervals)",
        xaxis_title="Time", yaxis_title="Redemption Volume",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20), height=420
    )
    st.plotly_chart(fig_fc, use_container_width=True)
    
    st.caption("💡 **Operations Utility:** Use the forecasted peaks to pre-stage crews and schedule extra ferry runs 60 minutes before peak inflow occurs.")

# ================= TAB 6: RESEARCH PAPER & EXECUTIVE SUMMARY =================
with tab6:
    st.subheader("Academic Research Paper & Executive Policy Summary")
    
    st.markdown("""
    **Paper Title:** *Real-Time Passenger Movement Analytics and Predictive Scheduling for Urban Maritime Transit: A Longitudinal Study of Toronto Island Ferry Services (2015–2025)*  
    **Author:** Suraj Rajput (Unified Mentor Data Science & Analytics Research Internship)  
    **Dataset Coverage:** 261,538 recorded 15-minute intervals • 12,972,051 total sales • 12,785,293 redemptions.
    """)
    
    # Read research paper markdown file
    paper_path = os.path.join(root_dir, "Toronto_Island_Ferry_Research_Paper.md")
    if not os.path.exists(paper_path):
        paper_path = os.path.join(os.path.dirname(root_dir), "0da96386-7bfc-4193-9d95-8aca6c634d6a", "Toronto_Island_Ferry_Research_Paper.md")
        
    if os.path.exists(paper_path):
        with open(paper_path, "r", encoding="utf-8") as f:
            paper_content = f.read()
        
        st.download_button(
            label="📥 Download Full Academic Paper (Markdown / PDF-ready)",
            data=paper_content,
            file_name="Toronto_Island_Ferry_Analytics_Research_Paper.md",
            mime="text/markdown"
        )
        
        with st.expander("📖 Read Complete Academic Research Paper Inline", expanded=True):
            st.markdown(paper_content)
    else:
        st.info("Research paper document is available in the repository root directory.")
