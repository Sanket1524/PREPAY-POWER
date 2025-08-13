import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Setup ---
st.set_page_config(page_title="Prepay Power: District Heating Forecast", layout="wide")

# --- Prepay Power Website Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 11px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 2rem 0;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(40, 167, 69, 0.2);
    }
    
    .header-title {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e9ecef;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    /* Frame Styling */
    .frame-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        min-height: 400px;
    }
    
    .frame-title {
        color: #28a745 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    
    /* Metric Styling */
    .stMetric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        font-weight: 600;
    }
    
    .stMetric > div {
        background: transparent !important;
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent !important;
    }
    
    /* Chart Styling */
    .stPlotlyChart {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Form Controls */
    .stSelectbox, .stNumberInput, .stSlider, .stRadio {
        background: white;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .stSelectbox > div, .stNumberInput > div {
        background: white;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Custom Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #218838 0%, #1ea085 100%);
        transform: translateY(-1px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem !important;
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
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #28a745;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #218838;
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

# --- Sidebar Styling ---
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
    <h3 style="color: white; margin: 0; font-weight: 600;">⚙️ Configuration Panel</h3>
</div>
""", unsafe_allow_html=True)

# --- Select Site ---
site = st.sidebar.selectbox("📍 Select Site", list(sites.keys()))
defaults = sites.get(site, {})

# --- Input Panel ---
st.sidebar.markdown('<div class="section-header">🔧 Input Parameters</div>', unsafe_allow_html=True)
area = st.sidebar.number_input("Area (m²)", value=defaults.get("area", 0))
indoor_temp = st.sidebar.number_input("Indoor Temp (°C)", value=defaults.get("indoor_temp", 20))
outdoor_temp = st.sidebar.number_input("Outdoor Temp (°C)", value=defaults.get("outdoor_temp", 5))
u_value = st.sidebar.number_input("U-Value (W/m²K)", value=defaults.get("u_value", 0.15))
system_loss = st.sidebar.slider("System Loss (%)", 0, 100, int(defaults.get("system_loss", 0.5) * 100)) / 100
boiler_eff = st.sidebar.slider("Boiler Efficiency (%)", 1, 100, int(defaults.get("boiler_eff", 85))) / 100
co2_factor = st.sidebar.number_input("CO₂ Emission Factor (kg/kWh)", value=defaults.get("co2_factor", 0.23))
elec_price = st.sidebar.number_input("Electricity Price (€/kWh)", value=defaults.get("elec_price", 0.25))

st.sidebar.markdown('<div class="section-header">⚙️ System Configuration</div>', unsafe_allow_html=True)
chp_on = st.sidebar.radio("CHP Installed?", ["Yes", "No"], index=0 if defaults.get("chp_installed") == "Yes" else 1)
chp_th = st.sidebar.number_input("CHP Thermal Output (kW)", value=defaults.get("chp_th", 0), disabled=chp_on == "No")
chp_el = st.sidebar.number_input("CHP Elec Output (kW)", value=defaults.get("chp_el", 0), disabled=chp_on == "No")
chp_gas = st.sidebar.number_input("CHP Gas Input (kW)", value=defaults.get("chp_gas", 0), disabled=chp_on == "No")
chp_hours = st.sidebar.slider("CHP Hours/Day", 0, 24, value=defaults.get("chp_hours", 0), disabled=chp_on == "No")
chp_adj = st.sidebar.slider("CHP Adjustment (%)", 0, 100, int(defaults.get("chp_adj", 0.95) * 100), disabled=chp_on == "No") / 100

hp_on = st.sidebar.radio("Heat Pump Installed?", ["Yes", "No"], index=0 if defaults.get("hp_installed") == "Yes" else 1)
hp_th = st.sidebar.number_input("HP Thermal Output (kW)", value=defaults.get("hp_th", 0), disabled=hp_on == "No")
hp_hours = st.sidebar.slider("HP Hours/Day", 0, 24, value=defaults.get("hp_hours", 0), disabled=hp_on == "No")
hp_cop = st.sidebar.number_input("HP COP", value=defaults.get("hp_cop", 1), disabled=hp_on == "No")

# --- Dynamic Visualization Controls ---
st.sidebar.markdown('<div class="section-header">📊 Visualization Settings</div>', unsafe_allow_html=True)
chart_type = st.sidebar.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"])
show_metrics = st.sidebar.checkbox("Show Metrics", value=True)
show_forecast = st.sidebar.checkbox("Show Monthly Forecast", value=True)
show_breakdown = st.sidebar.checkbox("Show Energy Breakdown", value=True)
show_efficiency = st.sidebar.checkbox("Show Efficiency Analysis", value=True)

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
                        color_discrete_sequence=['#28a745', '#20c997', '#17a2b8'])
        elif chart_type == "Pie Chart":
            fig = px.pie(energy_df, values="Energy (kWh)", names="Source", 
                        title="Energy Source Distribution",
                        color_discrete_sequence=['#28a745', '#20c997', '#17a2b8'])
        else:
            fig = px.bar(energy_df, x="Source", y="Energy (kWh)", 
                        title="Daily Energy Breakdown", color="Source",
                        color_discrete_sequence=['#28a745', '#20c997', '#17a2b8'])
        
        fig.update_layout(
            font=dict(size=11, family="Inter"),
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=14,
            title_font_color='#28a745'
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
                    color_discrete_sequence=['#28a745', '#20c997', '#17a2b8', '#6f42c1'])
        fig.update_layout(
            font=dict(size=11, family="Inter"),
            height=300,
            yaxis_title="Efficiency (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=14,
            title_font_color='#28a745'
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
                color_continuous_scale=['#dc3545', '#ffc107', '#28a745'])
    fig.update_layout(
        font=dict(size=11, family="Inter"),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=14,
        title_font_color='#28a745'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Monthly Forecast (Full Width) ---
if show_forecast:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 1.5rem; border-radius: 16px; margin: 2rem 0;">
        <h2 style="color: white; margin: 0; font-weight: 700;">📈 Monthly Forecast</h2>
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
                      color_discrete_sequence=['#28a745', '#20c997', '#17a2b8', '#6f42c1'])
    elif chart_type == "Bar Chart":
        fig = px.bar(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                     title="Monthly Heating Forecast (kWh)", barmode='stack',
                     color_discrete_sequence=['#28a745', '#20c997', '#17a2b8', '#6f42c1'])
    elif chart_type == "Area Chart":
        fig = px.area(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                      title="Monthly Heating Forecast (kWh)",
                      color_discrete_sequence=['#28a745', '#20c997', '#17a2b8', '#6f42c1'])
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x="Month", y=["Heating", "CHP", "HP", "Boiler"],
                         title="Monthly Heating Forecast (kWh)",
                         color_discrete_sequence=['#28a745', '#20c997', '#17a2b8', '#6f42c1'])
    
    fig.update_layout(
        yaxis_title="Energy (kWh)", 
        legend_title="Source", 
        template="plotly_white",
        font=dict(size=11, family="Inter"),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16,
        title_font_color='#28a745'
    )
    
    # Add container styling for the chart
    st.markdown('<div style="background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive data table
    st.markdown("""
    <div style="background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 1rem;">
        <h3 style="color: #28a745; font-weight: 700; margin-bottom: 1rem;">📋 Forecast Data</h3>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
