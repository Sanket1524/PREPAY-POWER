
import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page config
st.set_page_config(page_title="Prepay Power: District Heating Forecast", layout="wide", initial_sidebar_state="expanded")

# Custom Dark Theme Styling
st.markdown("""
<style>
body {
    background-color: #111827;
    color: #f9fafb;
}
h1, h2, h3, h4 {
    color: #f472b6;
}
[data-testid="metric-container"] {
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 12px;
}
.sidebar .sidebar-content {
    background: #1f2937;
    color: #f9fafb;
}
</style>
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
        "chp_hours": 15,
        "hp_installed": True,
        "hp_th": 60,
        "hp_hours": 9,
        "hp_cop": 4
    },
    "Custom": {}
}

# Sidebar inputs
with st.sidebar:
    st.title("🔧 Configuration")
    site = st.selectbox("Select Site", list(sites.keys()))
    defaults = sites.get(site, {})

    area = st.number_input("Area (m²)", value=defaults.get("area", 10000))
    u_value = st.number_input("U-Value", value=defaults.get("u_value", 0.15))
    indoor_temp = st.number_input("Indoor Temp (°C)", value=defaults.get("indoor_temp", 20))
    outdoor_temp = st.number_input("Outdoor Temp (°C)", value=defaults.get("outdoor_temp", 5))
    system_loss = st.slider("System Loss (%)", 0, 100, int(defaults.get("system_loss", 0.5) * 100)) / 100
    boiler_eff = st.slider("Boiler Efficiency (%)", 1, 100, int(defaults.get("boiler_eff", 85))) / 100
    co2_factor = st.number_input("CO₂ Emission Factor", value=defaults.get("co2_factor", 0.23))
    elec_price = st.number_input("Electricity Price", value=defaults.get("elec_price", 0.25))

    chp_installed = st.checkbox("CHP Installed", value=defaults.get("chp_installed", False))
    chp_th = st.number_input("CHP Thermal Output (kW)", value=defaults.get("chp_th", 0.0)) if chp_installed else 0.0
    chp_hours = st.slider("CHP Hours/Day", 0, 24, value=defaults.get("chp_hours", 0)) if chp_installed else 0

    hp_installed = st.checkbox("Heat Pump Installed", value=defaults.get("hp_installed", False))
    hp_th = st.number_input("HP Thermal Output (kW)", value=defaults.get("hp_th", 0.0)) if hp_installed else 0.0
    hp_hours = st.slider("HP Hours/Day", 0, 24, value=defaults.get("hp_hours", 0)) if hp_installed else 0
    hp_cop = st.number_input("HP COP", value=defaults.get("hp_cop", 1.0)) if hp_installed else 1.0

# --- Calculations ---
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_hours if chp_installed else 0
hp_thermal = hp_th * hp_hours if hp_installed else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas_input = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# --- Metrics ---
st.title("📊 Output Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Heat Demand", f"{heat_demand:.1f} kWh/day")
col2.metric("CHP Thermal", f"{chp_thermal:.1f} kWh")
col3.metric("HP Thermal", f"{hp_thermal:.1f} kWh")
col4.metric("Boiler Thermal", f"{boiler_thermal:.1f} kWh")

# --- Forecasting ---
st.header("📅 Monthly Forecast")
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

# Plot
fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
              title="Monthly Forecast", markers=True)
st.plotly_chart(fig, use_container_width=True)

# Table (safe formatting)
st.dataframe(df.round(0).astype("Int64"), use_container_width=True)
