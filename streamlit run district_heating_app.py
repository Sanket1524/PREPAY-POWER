import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Setup ---
st.set_page_config(page_title="Prepay Power: District Heating Forecast", layout="wide")

# --- Clean Modern Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 11px;
        background: #fafafa;
    }
    
    /* Header Styling */
    .header-container {
        background: #e6007e;
        padding: 1.5rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 2px 8px rgba(230, 0, 126, 0.15);
    }
    
    .header-title {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        text-align: center;
        margin: 0;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    
    /* Frame Styling */
    .frame-container {
        background: white;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        min-height: 350px;
    }
    
    .frame-title {
        color: #374151 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    /* Metric Styling */
    .stMetric {
        background: #f9fafb;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .stMetric > div {
        background: transparent !important;
    }
    
    .stMetric label {
        color: #6b7280 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent !important;
    }
    
    /* Chart Styling */
    .stPlotlyChart {
        background: white;
        border-radius: 8px;
        padding: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Form Controls */
    .stSelectbox, .stNumberInput, .stSlider, .stRadio {
        background: white;
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .stSelectbox > div, .stNumberInput > div {
        background: white;
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    /* Section Headers */
    .section-header {
        background: #e6007e;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Custom Button Styling */
    .stButton > button {
        background: #e6007e;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #be185d;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.5rem !important;
        }
        .frame-container {
            margin: 0.25rem 0;
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">💡 Prepay Power</h1>
    <p class="header-subtitle">District Heating Forecast & Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# --- Site Profiles ---
sites = {
    "Barnwell": {
        "area": 22102,
        "u_value": 0.15,
        "indoor_temp": 20,
        "outdoor_temp": 5,
        "system_loss": 0.50,
        "boiler_eff": 0.85,
        "co2_factor": 0.23,
        "elec_price": 0.25,
        "chp_installed": "Yes",
        "chp_th": 44.7,
        "chp_el": 19.965,
        "chp_gas": 67.9,
        "chp_hours": 15,
        "chp_adj": 0.95,
        "hp_installed": "Yes",
        "hp_th": 60,
        "hp_hours": 9,
        "hp_cop": 4
    },
    "Custom": {}
}

# --- Dramatic Configuration Panel ---
st.markdown("""
<style>
    .config-panel {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid #475569;
        margin: 1rem 0;
    }
    
    .config-header {
        background: linear-gradient(135deg, #e6007e 0%, #be185d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(230, 0, 126, 0.3);
    }
    
    .dial-container {
        background: linear-gradient(145deg, #2d3748, #1a202c);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #4a5568;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .dial-label {
        color: #e2e8f0;
        font-size: 0.8rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dial-value {
        color: #e6007e;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
        margin-top: 0.5rem;
        text-shadow: 0 0 10px rgba(230, 0, 126, 0.5);
    }
    
    .toggle-switch {
        background: linear-gradient(145deg, #374151, #1f2937);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border: 1px solid #4b5563;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .site-info {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Site Selection Toggle
col1, col2 = st.columns([1, 3])
with col1:
    site_toggle = st.toggle("🏢 Barnwell Site", value=True, help="Toggle between Barnwell (pre-configured) and Custom site")
    
# Set site based on toggle
site = "Barnwell" if site_toggle else "Custom"
defaults = sites.get(site, {})

# Main Configuration Panel
st.markdown("""
<div class="config-panel">
    <div class="config-header">
        <h3 style="margin: 0; font-weight: 700; font-size: 1.3rem;">⚙️ MASTER CONTROL PANEL</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">{'Barnwell Site - Pre-configured' if site_toggle else 'Custom Site - Full Control'}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Show site info if Barnwell is selected
if site_toggle:
    st.markdown("""
    <div class="site-info">
        <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">🏢 Barnwell Site - Pre-configured Parameters</h4>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">
            Area: 22,102 m² | CHP: 44.7 kW Thermal, 19.97 kW Electric | Heat Pump: 60 kW, COP 4.0 | 
            Boiler Efficiency: 85% | System Loss: 50%
        </p>
    </div>
    """, unsafe_allow_html=True)

# Configuration Controls in Single Frame
with st.container():
    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    
    # Top Row - Building & System Parameters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">🏠 Building Area</div>', unsafe_allow_html=True)
        area = st.slider("", 0, 50000, defaults.get("area", 0), 100, disabled=site_toggle, key="area_dial")
        st.markdown(f'<div class="dial-value">{area:,.0f} m²</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">🌡️ Indoor Temp</div>', unsafe_allow_html=True)
        indoor_temp = st.slider("", 15, 25, defaults.get("indoor_temp", 20), 1, disabled=site_toggle, key="indoor_dial")
        st.markdown(f'<div class="dial-value">{indoor_temp}°C</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">⚡ U-Value</div>', unsafe_allow_html=True)
        u_value = st.slider("", 0.05, 0.5, float(defaults.get("u_value", 0.15)), 0.01, disabled=site_toggle, key="uvalue_dial")
        st.markdown(f'<div class="dial-value">{u_value:.2f} W/m²K</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">🔥 Boiler Efficiency</div>', unsafe_allow_html=True)
        boiler_eff = st.slider("", 1, 100, int(defaults.get("boiler_eff", 85)), 5, disabled=site_toggle, key="boiler_dial")
        st.markdown(f'<div class="dial-value">{boiler_eff}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">💰 Electricity Price</div>', unsafe_allow_html=True)
        elec_price = st.slider("", 0.1, 0.5, float(defaults.get("elec_price", 0.25)), 0.01, disabled=site_toggle, key="elec_dial")
        st.markdown(f'<div class="dial-value">€{elec_price:.2f}/kWh</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">🌍 CO₂ Factor</div>', unsafe_allow_html=True)
        co2_factor = st.slider("", 0.1, 0.5, float(defaults.get("co2_factor", 0.23)), 0.01, disabled=site_toggle, key="co2_dial")
        st.markdown(f'<div class="dial-value">{co2_factor:.2f} kg/kWh</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dial-container">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">📊 Chart Type</div>', unsafe_allow_html=True)
        chart_type = st.selectbox("", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"], key="chart_dial")
        st.markdown(f'<div class="dial-value">{chart_type}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="toggle-switch">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">📈 Show Forecast</div>', unsafe_allow_html=True)
        show_forecast = st.checkbox("", value=True, key="forecast_toggle")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # System Configuration Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="toggle-switch">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">🔥 CHP System</div>', unsafe_allow_html=True)
        chp_on = st.toggle("Installed", value=defaults.get("chp_installed") == "Yes", disabled=site_toggle, key="chp_toggle")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if chp_on:
            st.markdown('<div class="dial-container">', unsafe_allow_html=True)
            st.markdown('<div class="dial-label">CHP Thermal Output</div>', unsafe_allow_html=True)
            chp_th = st.slider("", 0, 100, int(defaults.get("chp_th", 0)), 1, disabled=site_toggle, key="chp_th_dial")
            st.markdown(f'<div class="dial-value">{chp_th} kW</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="dial-container">', unsafe_allow_html=True)
            st.markdown('<div class="dial-label">CHP Hours/Day</div>', unsafe_allow_html=True)
            chp_hours = st.slider("", 0, 24, defaults.get("chp_hours", 0), 1, disabled=site_toggle, key="chp_hours_dial")
            st.markdown(f'<div class="dial-value">{chp_hours} hrs</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            chp_th = chp_hours = 0
    
    with col2:
        st.markdown('<div class="toggle-switch">', unsafe_allow_html=True)
        st.markdown('<div class="dial-label">❄️ Heat Pump System</div>', unsafe_allow_html=True)
        hp_on = st.toggle("Installed", value=defaults.get("hp_installed") == "Yes", disabled=site_toggle, key="hp_toggle")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if hp_on:
            st.markdown('<div class="dial-container">', unsafe_allow_html=True)
            st.markdown('<div class="dial-label">HP Thermal Output</div>', unsafe_allow_html=True)
            hp_th = st.slider("", 0, 100, int(defaults.get("hp_th", 0)), 1, disabled=site_toggle, key="hp_th_dial")
            st.markdown(f'<div class="dial-value">{hp_th} kW</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="dial-container">', unsafe_allow_html=True)
            st.markdown('<div class="dial-label">HP COP</div>', unsafe_allow_html=True)
            hp_cop = st.slider("", 1, 6, float(defaults.get("hp_cop", 1)), 0.1, disabled=site_toggle, key="hp_cop_dial")
            st.markdown(f'<div class="dial-value">{hp_cop:.1f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            hp_th = hp_cop = 0
    
    # Additional parameters
    outdoor_temp = defaults.get("outdoor_temp", 5)
    system_loss = defaults.get("system_loss", 0.5)
    chp_el = defaults.get("chp_el", 0) if chp_on else 0
    chp_gas = defaults.get("chp_gas", 0) if chp_on else 0
    chp_adj = defaults.get("chp_adj", 0.95) if chp_on else 0
    hp_hours = defaults.get("hp_hours", 0) if hp_on else 0
    show_metrics = True
    show_breakdown = True
    show_efficiency = True
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Calculations ---
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_adj * chp_hours if chp_on == "Yes" else 0
hp_thermal = hp_th * hp_hours if hp_on == "Yes" else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas_input = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# --- 4 Vertical Frames Layout ---
frame1, frame2, frame3, frame4 = st.columns(4)

# Frame 1: Key Metrics
with frame1:
    st.markdown('<div class="frame-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="frame-title">📊 Key Metrics</h3>', unsafe_allow_html=True)
    if show_metrics:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Heat Demand", f"{heat_demand:.2f} kWh/day")
            st.metric("CHP Thermal", f"{chp_thermal:.2f} kWh")
            st.metric("HP Thermal", f"{hp_thermal:.2f} kWh")
        with col2:
            st.metric("Boiler Thermal", f"{boiler_thermal:.2f} kWh")
            st.metric("Boiler Gas Input", f"{boiler_gas_input:.2f} kWh")
            st.metric("CO₂ Emissions", f"{boiler_gas_input * co2_factor:.2f} kg")
    st.markdown('</div>', unsafe_allow_html=True)

# Frame 2: Energy Breakdown
with frame2:
    st.markdown('<div class="frame-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="frame-title">⚡ Energy Breakdown</h3>', unsafe_allow_html=True)
    if show_breakdown:
        energy_data = {
            "Source": ["CHP", "Heat Pump", "Boiler"],
            "Energy (kWh)": [chp_thermal, hp_thermal, boiler_thermal]
        }
        energy_df = pd.DataFrame(energy_data)
        
        if chart_type == "Bar Chart":
            fig = px.bar(energy_df, x="Source", y="Energy (kWh)", 
                        title="Daily Energy Breakdown", color="Source",
                        color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4'])
        elif chart_type == "Pie Chart":
            fig = px.pie(energy_df, values="Energy (kWh)", names="Source", 
                        title="Energy Source Distribution",
                        color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4'])
        else:
            fig = px.bar(energy_df, x="Source", y="Energy (kWh)", 
                        title="Daily Energy Breakdown", color="Source",
                        color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4'])
        
        fig.update_layout(
            font=dict(size=11, family="Inter"),
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=14,
            title_font_color='#374151'
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Frame 3: Efficiency Analysis
with frame3:
    st.markdown('<div class="frame-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="frame-title">🔋 Efficiency Analysis</h3>', unsafe_allow_html=True)
    if show_efficiency:
        # Calculate efficiencies
        total_input = boiler_gas_input + (chp_gas * chp_hours if chp_on == "Yes" else 0) + (hp_th * hp_hours / hp_cop if hp_on == "Yes" else 0)
        total_output = heat_demand
        overall_efficiency = (total_output / total_input * 100) if total_input > 0 else 0
        
        efficiency_data = {
            "Metric": ["Overall Efficiency", "Boiler Efficiency", "CHP Efficiency", "HP COP"],
            "Value (%)": [overall_efficiency, boiler_eff * 100, (chp_th / chp_gas * 100) if chp_gas > 0 else 0, hp_cop * 100]
        }
        eff_df = pd.DataFrame(efficiency_data)
        
        fig = px.bar(eff_df, x="Metric", y="Value (%)", 
                    title="System Efficiency Metrics", color="Metric",
                    color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4', '#10b981'])
        fig.update_layout(
            font=dict(size=11, family="Inter"),
            height=300,
            yaxis_title="Efficiency (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=14,
            title_font_color='#374151'
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Frame 4: Cost Analysis
with frame4:
    st.markdown('<div class="frame-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="frame-title">💰 Cost Analysis</h3>', unsafe_allow_html=True)
    # Calculate costs
    chp_elec_revenue = chp_el * chp_hours * elec_price if chp_on == "Yes" else 0
    chp_gas_cost = chp_gas * chp_hours * 0.08 if chp_on == "Yes" else 0  # Assuming gas price €0.08/kWh
    hp_elec_cost = (hp_th * hp_hours / hp_cop) * elec_price if hp_on == "Yes" else 0
    boiler_gas_cost = boiler_gas_input * 0.08  # Assuming gas price €0.08/kWh
    
    cost_data = {
        "Component": ["CHP Revenue", "CHP Gas Cost", "HP Elec Cost", "Boiler Gas Cost"],
        "Cost (€/day)": [chp_elec_revenue, -chp_gas_cost, -hp_elec_cost, -boiler_gas_cost]
    }
    cost_df = pd.DataFrame(cost_data)
    
    fig = px.bar(cost_df, x="Component", y="Cost (€/day)", 
                title="Daily Cost Breakdown", color="Cost (€/day)",
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'])
    fig.update_layout(
        font=dict(size=11, family="Inter"),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=14,
        title_font_color='#374151'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Monthly Forecast (Full Width) ---
if show_forecast:
    st.markdown("""
    <div style="background: #e6007e; padding: 1.25rem; border-radius: 8px; margin: 2rem 0;">
        <h2 style="color: white; margin: 0; font-weight: 600;">📈 Monthly Forecast</h2>
    </div>
    """, unsafe_allow_html=True)
    
    monthly_temps = {
        "Jan": 5.0, "Feb": 5.5, "Mar": 7.0, "Apr": 9.0, "May": 11.0, "Jun": 13.5,
        "Jul": 15.0, "Aug": 15.0, "Sep": 13.0, "Oct": 10.0, "Nov": 7.0, "Dec": 5.5
    }
    days_in_month = {
        "Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31, "Jun": 30,
        "Jul": 31, "Aug": 31, "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31
    }
    
    forecast = []
    for m in monthly_temps:
        temp = monthly_temps[m]
        days = days_in_month[m]
        heat = (u_value * area * (indoor_temp - temp) * 24 / 1000) * (1 + system_loss) * days
        chp_m = chp_th * chp_adj * chp_hours * days if chp_on == "Yes" else 0
        hp_m = hp_th * hp_hours * days if hp_on == "Yes" else 0
        boiler = max(0, heat - chp_m - hp_m)
        forecast.append({"Month": m, "Heating": round(heat), "CHP": round(chp_m), "HP": round(hp_m), "Boiler": round(boiler)})

    df = pd.DataFrame(forecast)
    
    # Dynamic chart based on user selection
    if chart_type == "Line Chart":
        fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                      title="Monthly Heating Forecast (kWh)", markers=True,
                      color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4', '#10b981'])
    elif chart_type == "Bar Chart":
        fig = px.bar(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                     title="Monthly Heating Forecast (kWh)", barmode='stack',
                     color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4', '#10b981'])
    elif chart_type == "Area Chart":
        fig = px.area(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                      title="Monthly Heating Forecast (kWh)",
                      color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4', '#10b981'])
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                         title="Monthly Heating Forecast (kWh)",
                         color_discrete_sequence=['#e6007e', '#8b5cf6', '#06b6d4', '#10b981'])
    
    fig.update_layout(
        yaxis_title="Energy (kWh)", 
        legend_title="Source", 
        template="plotly_white",
        font=dict(size=11, family="Inter"),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16,
        title_font_color='#374151'
    )
    
    # Add container styling for the chart
    st.markdown('<div style="background: white; border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive data table
    st.markdown("""
    <div style="background: white; border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-top: 1rem;">
        <h3 style="color: #374151; font-weight: 600; margin-bottom: 1rem;">📋 Forecast Data</h3>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
