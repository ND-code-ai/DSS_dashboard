"""
Main dashboard application for Electric Vehicle (EV) analytics.
This script creates an interactive dashboard using Streamlit to visualize various EV-related KPIs.

Dependencies:
    - streamlit
    - altair
    - pandas
    - pickle
    - sqlalchemy
"""

import streamlit as st
import altair as alt
from st_pages import EV_Infrastructure, EVSales, emissions, home, EV_Prices_DE, EV_em_and_sales
import pandas as pd
import pickle as pkl

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="EV Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the KPIs and corresponding table names
kpis = ["EV infrastructure", "EV sales", "Fossil fuel emissions by cars", "EV prices", "EV Emissions and sales"]
table_names = [table_name.replace(" ", "") for table_name in kpis]

# Enable dark theme for Altair charts
alt.themes.enable("dark")

# Create layout columns
col = st.columns((1.5, 6, 2), gap='medium')

# Load preprocessed data from pickle file
imported_data = pkl.load(open("data/temp_export.pkl", "rb"))
imported_data = {key.replace(" ", ""): value for key, value in imported_data.items()}
imported_data["EVEmissionsandsales"] = pd.read_csv("data/EV_em_and_sales.csv")

# Sidebar configuration
with st.sidebar:
    st.title("Electric Vehicle Dashboard")
    kpis.insert(0, "---")
    kpis[3] = "EV electric usage"
    selected_kpi = st.selectbox("Select a KPI", kpis)

# Main content based on selected KPI
if selected_kpi == "---":
    home.main()

elif selected_kpi == "EV infrastructure":
    st.title("EV Infrastructure")
    EV_Infrastructure.main(imported_data[table_names[0]])

elif selected_kpi == "EV sales":
    st.title("Increasing EV adoption - EV Sales")
    EVSales.main(imported_data[table_names[1]])

elif selected_kpi == "EV electric usage":
    st.title("Increasing EV adoption - Electric usage by EVs")
    emissions.main(imported_data[table_names[2]])

elif selected_kpi == "EV prices":
    st.title("Increasing EV adoption - EV prices")
    EV_Prices_DE.main(imported_data[table_names[3]])

elif selected_kpi == "EV Emissions and sales":
    st.title("EV Emissions and sales")
    EV_em_and_sales.main(imported_data[table_names[4]])
