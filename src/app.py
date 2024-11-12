import streamlit as st
import altair as alt
from st_pages import EV_Infrastructure, EVSales, emissions,home, EV_Prices_DE, EV_em_and_sales
from load_db import load_data_to_db, load_data_from_db
import group14_preparedata as prep
import pandas as pd

st.set_page_config(
    page_title="EV Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

def get_all_data(table_names: list[str]) -> dict[str, pd.DataFrame]:
    all_tables = {}

    for table_name in table_names:
        all_tables[table_name] = load_data_from_db(table_name)

    return all_tables

kpis = ["EV infrastructure", "EV sales", "EV prices", "Fossil fuel emissions by cars", "EV Emissions and sales"]
table_names = [kpi.replace(" ", "") for kpi in kpis]
all_cleaned_tables = prep.main()

load_data_to_db(all_cleaned_tables)
all_data = get_all_data(table_names)

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
    EV_Infrastructure.main(all_data[table_names[0]])

elif selected_kpi == "EV sales":
    st.title("Increasing EV adoption - EV Sales")
    EVSales.main(all_data[table_names[1]])

elif selected_kpi == "Fossil fuel emissions by cars":
    st.title("Increasing EV adoption - Fossil fuel emissions by cars")
    emissions.main(all_data[table_names[2]])

elif selected_kpi == "EV prices":
    st.title("Increasing EV adoption - EV prices")
    EV_Prices_DE.main(all_data[table_names[4]])

elif selected_kpi == "EV Emissions and sales":
    st.title("EV Emissions and sales")
    EV_em_and_sales.main(all_data[table_names[5]])
