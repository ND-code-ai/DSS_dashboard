import streamlit as st
import altair as alt
from st_pages import EV_Infrastructure, EVSales, emissions, green_energy, home, EV_Prices_DE, EV_em_and_sales
from load_db import load_data_from_db
import pandas as pd

st.set_page_config(
    page_title="EV Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

def gather_tables(kpis: list[str]) -> dict[str, pd.DataFrame]:
    tables = {}

    for kpi in kpis:
        tables[kpi] = load_data_from_db(kpi)
    
    return tables

kpis = ["EV infrastructure", "EV sales", "EV prices", "Fossil fuel emissions by cars", "Green energy usage", "EV Emissions and sales"]
all_tables = gather_tables(kpis)

alt.themes.enable("dark")
col = st.columns((1.5, 6, 2), gap='medium')

with st.sidebar:
    st.title("Electric Vehicle Dashboard")
    kpis.insert(0, "---")
    selected_kpi = st.selectbox("Select a KPI", kpis)
    

if selected_kpi == "---":
    home.main()
    
if selected_kpi == "EV infrastructure":
    st.title("EV Infrastructure")
    EV_Infrastructure.main(all_tables["EV infrastructure"])

elif selected_kpi == "EV sales":
    st.title("Increasing EV adoption - EV Sales")
    EVSales.main(all_tables["EV sales"])

elif selected_kpi == "Fossil fuel emissions by cars":
    st.title("Increasing EV adoption - Fossil fuel emissions by cars")
    emissions.main(all_tables["Fossil fuel emissions by cars"])

elif selected_kpi == "Green energy usage":
    st.title("Increasing EV adoption - Green energy usage")
    green_energy.main(all_tables["Green energy usage"])

elif selected_kpi == "EV prices":
    st.title("Increasing EV adoption - EV prices")
    EV_Prices_DE.main(all_tables["EV prices"])

elif selected_kpi == "EV Emissions and sales":
    st.title("EV Emissions and sales")
    EV_em_and_sales.main(all_tables["EV Emissions and sales"])
