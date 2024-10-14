import streamlit as st
import altair as alt
from st_pages import EVInfastructure, EVSales, emissions, green_energy, home


st.set_page_config(
    page_title="EV Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
col = st.columns((1.5, 6, 2), gap='medium')


with st.sidebar:
    st.title("Electric Vehicle Dashboard")
    selected_kpi = st.selectbox("Select a KPI", ["---", "Number of charging stations", "EV sales", "Fossil fuel emissions by cars", "Green energy usage"])
    

if selected_kpi == "---":
    home.main()
    
if selected_kpi == "Number of charging stations":
    st.title("EV Infrastructure - Number of Charging Stations")
    EVInfastructure.main()

elif selected_kpi == "EV sales":
    st.title("Increasing EV adoption - EV Sales")
    EVSales.main()

elif selected_kpi == "Fossil fuel emissions by cars":
    st.title("Increasing EV adoption - Fossil fuel emissions by cars")
    emissions.main()

elif selected_kpi == "Green energy usage":
    st.title("Increasing EV adoption - Green energy usage")
    green_energy.main()
