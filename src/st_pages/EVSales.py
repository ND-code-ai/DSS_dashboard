import streamlit as st
import pandas as pd
import altair as alt

def main():
    col = st.columns((8, 1), gap='medium')
    data = pd.read_csv("data/cleaned_NoEVS_data.csv")
    #Replaces the missing value
    data.replace(':', pd.NA, inplace=True)

    with col[0]:
        # Replace the '.' with '' to fix the number formatting and convert to float for numeric calculations
        data.replace({r'\.': ''}, regex=True, inplace=True)

        # Convert all year columns to numeric
        for year in data.columns[1:]:
            data[year] = pd.to_numeric(data[year], errors='coerce')
        
        eu_data = data[data['Country'] == 'European Union']
        eu_data_melted = eu_data.melt(id_vars='Country', var_name='Year', value_name='Number of New Passenger Cars Sold')
        eu_data_melted['Year'] = pd.to_numeric(eu_data_melted['Year'], errors='coerce')
        chart = alt.Chart(eu_data_melted).mark_bar().encode(
            x='Year:O',  # Ordinal encoding for year
            y='Number of New Passenger Cars Sold:Q',  # Quantitative encoding for values
            tooltip=['Year', 'Number of New Passenger Cars Sold']
        ).properties(
            title='New EV passenger car sales in the European Union (2014-2023)',
            width=1200,
            height=600
        )
        final_chart = chart

        st.altair_chart(final_chart)



