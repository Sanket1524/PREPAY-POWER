
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure Streamlit for better performance and updates
st.set_page_config(
    page_title="Prepay Power: District Heating Forecast", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Elegant & Attractive UI ---
st.markdown("""
<style>
* {
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: 700 !important;
    color: #1f2937 !important;
}
p, div, span {
    color: #374151 !important;
}
.sidebar .sidebar-content {
    background: #f1f5f9 !important;
}
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #ffb6c1 0%, #ffc0cb 100%); border-radius: 12px; margin-bottom: 2rem;">
    <h1 style="color: #ffffff; font-size: 48px !important;">💡 Prepay Power</h1>
    <p style="color: #ffffff; font-size: 32px !important;">District Heating Forecast Dashboard</p>
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

# Sidebar Inputs
with st.sidebar:
    st.markdown("### 📍 Site Selection")
    site = st.selectbox("Select Site", list(sites.keys()))
    defaults = sites.get(site, {})

    st.markdown("#### Building Parameters")
    area = st.number_input("Area (m²)", value=defaults.get("area", 10000))
    u_value = st.number_input("U-Value (W/m²K)", value=defaults.get("u_value", 0.15))
    indoor_temp = st.number_input("Indoor Temp (°C)", value=defaults.get("indoor_temp", 20))
    outdoor_temp = st.number_input("Outdoor Temp (°C)", value=defaults.get("outdoor_temp", 5))

    st.markdown("#### System Parameters")
    system_loss = st.slider("System Loss (%)", 0, 100, int(defaults.get("system_loss", 0.5) * 100)) / 100
    boiler_eff = st.slider("Boiler Efficiency (%)", 1, 100, int(defaults.get("boiler_eff", 85))) / 100

    st.markdown("#### CHP Configuration")
    chp_installed = st.checkbox("CHP Installed", value=defaults.get("chp_installed", False))
    if chp_installed:
        chp_th = st.number_input("CHP Thermal Output (kW)", value=defaults.get("chp_th", 0.0))
        chp_hours = st.slider("CHP Hours/Day", 0, 24, value=defaults.get("chp_hours", 0))
    else:
        chp_th, chp_hours = 0, 0

    st.markdown("#### Heat Pump Configuration")
    hp_installed = st.checkbox("Heat Pump Installed", value=defaults.get("hp_installed", False))
    if hp_installed:
        hp_th = st.number_input("HP Thermal Output (kW)", value=defaults.get("hp_th", 0.0))
        hp_hours = st.slider("HP Hours/Day", 0, 24, value=defaults.get("hp_hours", 0))
        hp_cop = st.number_input("HP COP", value=defaults.get("hp_cop", 1.0))
    else:
        hp_th, hp_hours, hp_cop = 0, 0, 1

# Core Calculations
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_hours if chp_installed else 0
hp_thermal = hp_th * hp_hours if hp_installed else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas_input = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# Output Summary
st.subheader("📊 Output Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Heat Demand", f"{heat_demand:.2f} kWh/day")
col2.metric("CHP Thermal", f"{chp_thermal:.2f} kWh")
col3.metric("HP Thermal", f"{hp_thermal:.2f} kWh")
col1.metric("Boiler Thermal", f"{boiler_thermal:.2f} kWh")
col2.metric("Boiler Gas Input", f"{boiler_gas_input:.2f} kWh")
col3.metric("CO₂ Emissions", f"{boiler_gas_input * defaults.get('co2_factor', 0.23):.2f} kg")

# Forecast Chart
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
    forecast.append({"Month": m, "Heating": heat, "CHP": chp_m, "HP": hp_m, "Boiler": boiler})

df = pd.DataFrame(forecast)
fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
              title="Monthly Heating Forecast (kWh)",
              markers=True,
              color_discrete_sequence=["#ff1493", "#636EFA", "#00CC96", "#AB63FA"])
st.plotly_chart(fig, use_container_width=True)
