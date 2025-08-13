import streamlit as st
import pandas as pd
import plotly.express as px

# Configure Streamlit for better performance and updates
st.set_page_config(
    page_title="Prepay Power: District Heating Forecast", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Disable caching for dynamic updates
@st.cache_data(ttl=0)
def get_data():
    return None

# --- Page Setup ---

# --- Custom CSS for Elegant & Attractive UI ---
st.markdown("""
<style>
/* Global Font & Design System */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    line-height: 1.6 !important;
}

/* Elegant Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700 !important;
    color: #1f2937 !important;
    margin-bottom: 1rem !important;
    letter-spacing: -0.025em !important;
}

/* Clean Content Styling */
p, div, span {
    color: #374151 !important;
    font-weight: 400 !important;
}

/* Enhanced Sidebar */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border-right: 2px solid #e2e8f0 !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05) !important;
}

.sidebar .sidebar-content .stMarkdown {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #1e293b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Elegant Input Controls */
.stNumberInput > div > div > input {
    font-size: 14px !important;
    padding: 12px 16px !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    transition: all 0.2s ease !important;
}

.stNumberInput > div > div > input:focus {
    border-color: #ff1493 !important;
    box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.1) !important;
}

.stSelectbox > div > div > div {
    font-size: 14px !important;
    border-radius: 12px !important;
}

.stSlider > div > div > div > div {
    font-size: 14px !important;
}

/* Premium Metrics Cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.3s ease !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
}

[data-testid="metric-container"] label {
    font-size: 13px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="metric-container"] div[data-testid="metric-value"] {
    font-size: 20px !important;
    font-weight: 800 !important;
    color: #1e293b !important;
    margin-top: 8px !important;
}

/* Enhanced Dataframe */
.dataframe {
    font-size: 13px !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Elegant Chart Styling */
.js-plotly-plot {
    font-size: 13px !important;
    border-radius: 12px !important;
}

/* Hide Default Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ff1493 0%, #e91e63 100%);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #e91e63 0%, #be185d 100%);
}

/* Section Headers */
.section-header {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 16px;
    padding: 20px;
    border: 2px solid #e2e8f0;
    margin-bottom: 24px;
}

/* Info Boxes */
.stAlert {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="text-align: center; padding: 2.5rem 0; background: linear-gradient(135deg, #ff1493 0%, #e91e63 100%); border-radius: 12px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 180pt !important; margin: 0; font-weight: 900; letter-spacing: -2px; text-shadow: 0 4px 8px rgba(0,0,0,0.4);">💡 Prepay Power</h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 140pt !important; margin: 1.5rem 0 0 0; font-weight: 700; text-shadow: 0 3px 6px rgba(0,0,0,0.3);">District Heating Forecast Dashboard</p>
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
        "chp_installed": True,
        "chp_th": 44.7,
        "chp_el": 19.965,
        "chp_gas": 67.9,
        "chp_hours": 15,
        "chp_adj": 0.95,
        "hp_installed": True,
        "hp_th": 60,
        "hp_hours": 9,
        "hp_cop": 4
    },
    "Custom": {}
}

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### 📍 Site Selection")
    site = st.selectbox("Select Site", list(sites.keys()))
    
    st.markdown("### 🔧 Configuration")
    use_barnwell = st.toggle("Use Barnwell Site", value=(site == "Barnwell"))
    
    # Get default values based on site selection
    default_site = "Barnwell" if use_barnwell else site
    defaults = sites.get(default_site, {})
    
    st.markdown("#### Building Parameters")
    area = st.number_input("Area (m²)", value=defaults.get("area", 10000), min_value=100, step=100)
    u_value = st.number_input("U-Value (W/m²K)", value=defaults.get("u_value", 0.15), min_value=0.05, max_value=1.0, step=0.01)
    indoor_temp = st.number_input("Indoor Temp (°C)", value=defaults.get("indoor_temp", 20), min_value=15, max_value=25, step=1)
    outdoor_temp = st.number_input("Outdoor Temp (°C)", value=defaults.get("outdoor_temp", 5), min_value=-10, max_value=20, step=1)
    
    st.markdown("#### System Parameters")
    system_loss = st.slider("System Loss (%)", 0, 100, int(defaults.get("system_loss", 0.5) * 100)) / 100
    boiler_eff = st.slider("Boiler Efficiency (%)", 1, 100, int(defaults.get("boiler_eff", 85))) / 100
    
    st.markdown("#### Economic Parameters")
    co2_factor = st.number_input("CO₂ Emission Factor (kg/kWh)", value=defaults.get("co2_factor", 0.23), min_value=0.1, max_value=1.0, step=0.01)
    elec_price = st.number_input("Electricity Price (€/kWh)", value=defaults.get("elec_price", 0.25), min_value=0.1, max_value=1.0, step=0.01)
    
    st.markdown("#### CHP Configuration")
    chp_installed = st.checkbox("CHP Installed", value=defaults.get("chp_installed", False))
    if chp_installed:
        chp_th = st.number_input("CHP Thermal Output (kW)", value=float(defaults.get("chp_th", 0)), min_value=0.0, step=0.1)
        chp_hours = st.slider("CHP Hours/Day", 0, 24, value=defaults.get("chp_hours", 0))
    else:
        chp_th = 0
        chp_hours = 0
    
    st.markdown("#### Heat Pump Configuration")
    hp_installed = st.checkbox("Heat Pump Installed", value=defaults.get("hp_installed", False))
    if hp_installed:
        hp_th = st.number_input("HP Thermal Output (kW)", value=float(defaults.get("hp_th", 0)), min_value=0.0, step=0.1)
        hp_hours = st.slider("HP Hours/Day", 0, 24, value=defaults.get("hp_hours", 0))
        hp_cop = st.number_input("HP COP", value=float(defaults.get("hp_cop", 1)), min_value=1.0, max_value=10.0, step=0.1)
    else:
        hp_th = 0
        hp_hours = 0
        hp_cop = 1
    
    if use_barnwell:
        st.info("📋 Barnwell parameters loaded - you can still modify them above")

# --- Calculations ---
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_hours if chp_installed else 0
hp_thermal = hp_th * hp_hours if hp_installed else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas_input = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# --- Main Dashboard ---
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 24px; border: 2px solid #e2e8f0; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h2 style="margin: 0; color: #1e293b; font-size: 24px; font-weight: 800; letter-spacing: -0.025em;">📊 Energy Analysis Dashboard</h2>
</div>
""", unsafe_allow_html=True)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Heat Demand", f"{heat_demand:.1f} kWh/day", f"{heat_demand/24:.1f} kW")
with col2:
    st.metric("CHP Thermal", f"{chp_thermal:.1f} kWh", f"{chp_thermal/24:.1f} kW" if chp_thermal > 0 else "0 kW")
with col3:
    st.metric("HP Thermal", f"{hp_thermal:.1f} kWh", f"{hp_thermal/24:.1f} kW" if hp_thermal > 0 else "0 kW")
with col4:
    st.metric("Boiler Thermal", f"{boiler_thermal:.1f} kWh", f"{boiler_gas_input:.1f} kWh gas")

# Energy Breakdown
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔋 Energy Sources")
    energy_data = {
        "Source": ["CHP", "Heat Pump", "Boiler"],
        "Energy (kWh)": [chp_thermal, hp_thermal, boiler_thermal]
    }
    energy_df = pd.DataFrame(energy_data)
    energy_df = energy_df[energy_df["Energy (kWh)"] > 0]  # Only show non-zero values
    
    if not energy_df.empty:
        fig_pie = px.pie(energy_df, values="Energy (kWh)", names="Source", 
                        title="Daily Energy Distribution",
                        color_discrete_sequence=['#ff1493', '#8b5cf6', '#06b6d4'])
        fig_pie.update_layout(font=dict(size=11))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No energy sources configured")

with col2:
    st.markdown("### 📈 Energy Comparison")
    if not energy_df.empty:
        fig_bar = px.bar(energy_df, x="Source", y="Energy (kWh)", 
                        title="Daily Energy Output by Source",
                        color_discrete_sequence=['#ff1493', '#8b5cf6', '#06b6d4'])
        fig_bar.update_layout(font=dict(size=11))
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No energy sources to compare")

# Monthly Forecast
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 24px; border: 2px solid #e2e8f0; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h2 style="margin: 0; color: #1e293b; font-size: 24px; font-weight: 800; letter-spacing: -0.025em;">📅 Monthly Forecast</h2>
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
    chp_m = chp_th * chp_hours * days if chp_installed else 0
    hp_m = hp_th * hp_hours * days if hp_installed else 0
    boiler = max(0, heat - chp_m - hp_m)
    forecast.append({
        "Month": m, 
        "Heating": round(heat), 
        "CHP": round(chp_m), 
        "HP": round(hp_m), 
        "Boiler": round(boiler)
    })

df = pd.DataFrame(forecast)

# Forecast Chart
fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
              title="Monthly Heating Forecast (kWh)", 
              markers=True,
              color_discrete_sequence=['#1f2937', '#ff1493', '#8b5cf6', '#06b6d4'])
fig.update_layout(
    yaxis_title="Energy (kWh)", 
    legend_title="Source", 
    template="plotly_white",
    font=dict(size=11)
)
st.plotly_chart(fig, use_container_width=True)

# Forecast Data Table
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 24px; border: 2px solid #e2e8f0; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 800; letter-spacing: -0.025em;">📋 Forecast Data</h3>
</div>
""", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 11px;">
    Prepay Power District Heating Forecast Dashboard | Built with Streamlit
</div>
""", unsafe_allow_html=True)
