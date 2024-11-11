import streamlit as st
import altair as alt
from st_pages import EV_Infrastructure, EVSales, emissions, green_energy, home, EV_Prices_DE, EV_em_and_sales


st.set_page_config(
    page_title="EV Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
col = st.columns((1.5, 6, 2), gap='medium')


with st.sidebar:
    st.title("Electric Vehicle Dashboard")
    selected_kpi = st.selectbox("Select a KPI", ["---", "Number of charging stations", "EV sales", "EV prices", "Fossil fuel emissions by cars", "Green energy usage", "EV Emissions and sales"])
    

if selected_kpi == "---":
    home.main()
    
if selected_kpi == "Number of charging stations":
    st.title("EV Infrastructure - Number of Charging Stations")
    EV_Infrastructure.main()

elif selected_kpi == "EV sales":
    st.title("Increasing EV adoption - EV Sales")
    EVSales.main()

elif selected_kpi == "Fossil fuel emissions by cars":
    st.title("Increasing EV adoption - Fossil fuel emissions by cars")
    emissions.main()

elif selected_kpi == "Green energy usage":
    st.title("Increasing EV adoption - Green energy usage")
    green_energy.main()

elif selected_kpi == "EV prices":
    st.title("Increasing EV adoption - EV prices")
    EV_Prices_DE.main()

elif selected_kpi == "EV Emissions and sales":
    st.title("EV Emissions and sales")
    EV_em_and_sales.main()
