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

        # Country filtering
        selected_countries = ['Germany', 'France', 'Netherlands', 'Sweden', 'Norway', 'Italy', 'Belgium', 'Denmark']
        filtered_data = data[data['Country'].isin(selected_countries)]

        # Melt data together
        filtered_data_melted = filtered_data.melt(id_vars='Country', var_name='Year', value_name='Number of New Passenger Cars Sold')

        # Year to numeric
        filtered_data_melted['Year'] = pd.to_numeric(filtered_data_melted['Year'], errors='coerce')

        # Create a selection for highlighting based on country
        highlight = alt.selection_point(on='pointerover', fields=['Country'], nearest=True)

        # create chart base
        base = alt.Chart(filtered_data_melted).encode(
            x='Year:O',
            y='Number of New Passenger Cars Sold:Q',
            color='Country:N'
        )

        # Adding invisible points for selection
        points = base.mark_circle().encode(
            opacity=alt.value(0)
        ).add_params(
            highlight
        ).properties(
            width=1200,
            height=600
        )

        # Adding line charts with size change on highlight
        lines = base.mark_line().encode(
            size=alt.condition(~highlight, alt.value(1), alt.value(3))
        )

        # Combine points and lines
        chart2 = points + lines

        final_chart = chart

        st.altair_chart(final_chart)
        st.altair_chart(chart2)



