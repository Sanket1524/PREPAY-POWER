# district_heating_dark.py

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Prepay Power: District Heating Forecast (Dark Mode)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dark Mode Styling ---
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #f8fafc;
}

h1, h2, h3, h4, h5, h6 {
    color: #f472b6;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 800;
}

.sidebar .sidebar-content {
    background-color: #1e293b;
    color: #f1f5f9;
}

[data-testid="metric-container"] {
    background-color: #1f2937;
    color: #f1f5f9;
    border-radius: 12px;
    border: 1px solid #334155;
}

[data-testid="metric-container"] div[data-testid="metric-value"] {
    color: #f472b6;
}

/* Chart tweaks */
.js-plotly-plot text {
    fill: #f8fafc !important;
}
</style>
""", unsafe_allow_html=True)

# --- Site Defaults ---
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

# --- Sidebar Config ---
st.sidebar.title("⚙️ Configuration")
site = st.sidebar.selectbox("Choose Site", list(sites.keys()))
values = sites[site]

area = st.sidebar.number_input("Area (m²)", value=values.get("area", 10000))
u_value = st.sidebar.number_input("U-Value", value=values.get("u_value", 0.15))
indoor_temp = st.sidebar.number_input("Indoor Temp (°C)", value=values.get("indoor_temp", 20))
outdoor_temp = st.sidebar.number_input("Outdoor Temp (°C)", value=values.get("outdoor_temp", 5))
system_loss = st.sidebar.slider("System Loss (%)", 0, 100, int(values.get("system_loss", 0.5) * 100)) / 100
boiler_eff = st.sidebar.slider("Boiler Efficiency (%)", 50, 100, int(values.get("boiler_eff", 0.85) * 100)) / 100
co2_factor = st.sidebar.number_input("CO₂ Emission Factor (kg/kWh)", value=values.get("co2_factor", 0.23))
elec_price = st.sidebar.number_input("Electricity Price (€/kWh)", value=values.get("elec_price", 0.25))

chp_installed = st.sidebar.checkbox("CHP Installed", value=values.get("chp_installed", False))
chp_th = st.sidebar.number_input("CHP Thermal Output (kW)", value=values.get("chp_th", 0.0), disabled=not chp_installed)
chp_hours = st.sidebar.slider("CHP Hours/Day", 0, 24, value=values.get("chp_hours", 0), disabled=not chp_installed)

hp_installed = st.sidebar.checkbox("Heat Pump Installed", value=values.get("hp_installed", False))
hp_th = st.sidebar.number_input("Heat Pump Thermal Output (kW)", value=values.get("hp_th", 0.0), disabled=not hp_installed)
hp_hours = st.sidebar.slider("Heat Pump Hours/Day", 0, 24, value=values.get("hp_hours", 0), disabled=not hp_installed)
hp_cop = st.sidebar.number_input("Heat Pump COP", value=values.get("hp_cop", 1.0), disabled=not hp_installed)

# --- Calculations ---
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_hours if chp_installed else 0
hp_thermal = hp_th * hp_hours if hp_installed else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# --- Output ---
st.title("💡 Prepay Power – District Heating Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Heat Demand", f"{heat_demand:.0f} kWh")
col2.metric("CHP Output", f"{chp_thermal:.0f} kWh")
col3.metric("Heat Pump Output", f"{hp_thermal:.0f} kWh")
col4.metric("Boiler Output", f"{boiler_thermal:.0f} kWh")

# --- Pie Chart ---
data = pd.DataFrame({
    "Source": ["CHP", "Heat Pump", "Boiler"],
    "kWh": [chp_thermal, hp_thermal, boiler_thermal]
})
data = data[data["kWh"] > 0]
if not data.empty:
    fig = px.pie(data, values="kWh", names="Source", title="Energy Breakdown", color_discrete_sequence=px.colors.sequential.RdPu)
    st.plotly_chart(fig, use_container_width=True)

# --- Monthly Forecast ---
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
temps = [5.0, 5.5, 7.0, 9.0, 11.0, 13.5, 15.0, 15.0, 13.0, 10.0, 7.0, 5.5]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
forecast = []

for m, t, d in zip(months, temps, days):
    h = (u_value * area * (indoor_temp - t) * 24 / 1000) * (1 + system_loss) * d
    c = chp_th * chp_hours * d if chp_installed else 0
    p = hp_th * hp_hours * d if hp_installed else 0
    b = max(0, h - c - p)
    forecast.append({"Month": m, "Heating": h, "CHP": c, "HP": p, "Boiler": b})

df = pd.DataFrame(forecast)
fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"], markers=True,
              title="📈 Monthly Heating Forecast", color_discrete_sequence=px.colors.sequential.RdPu)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df.style.format("{:.0f}"), use_container_width=True)
