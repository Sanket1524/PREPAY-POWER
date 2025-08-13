
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prepay Power: District Heating Forecast", layout="wide")

st.title("💡 Prepay Power: District Heating Forecast")

# Sample config
area = 22102
u_value = 0.15
indoor_temp = 20
outdoor_temp = 5
system_loss = 0.5
boiler_eff = 0.85
chp_th = 44.7
chp_hours = 15
hp_th = 60
hp_hours = 9
hp_cop = 4
chp_installed = True
hp_installed = True

# --- Calculations ---
heat_demand = (u_value * area * (indoor_temp - outdoor_temp) * 24 / 1000) * (1 + system_loss)
chp_thermal = chp_th * chp_hours if chp_installed else 0
hp_thermal = hp_th * hp_hours if hp_installed else 0
boiler_thermal = max(0, heat_demand - chp_thermal - hp_thermal)
boiler_gas_input = boiler_thermal / boiler_eff if boiler_eff > 0 else 0

# --- Forecast ---
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
        "Heating": heat, 
        "CHP": chp_m, 
        "HP": hp_m, 
        "Boiler": boiler
    })

df = pd.DataFrame(forecast)

# Fix: only cast numeric columns to Int64
df_display = df.copy()
numeric_cols = df_display.select_dtypes(include='number').columns
df_display[numeric_cols] = df_display[numeric_cols].round(0).astype("Int64")

st.dataframe(df_display, use_container_width=True)

# Optional chart
fig = px.line(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"], markers=True)
st.plotly_chart(fig, use_container_width=True)
