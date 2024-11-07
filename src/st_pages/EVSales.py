import streamlit as st
import pandas as pd
import altair as alt
import requests

def main():
    # URL to fetch the data from Eurostat
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_eqr_carpda/?format=JSON&lang=en&freq=A&unit=NR&mot_nrg=ELC&geo=EU27_2020&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=LI&geo=NO&geo=CH&geo=UK&geo=BA&geo=ME&geo=MD&geo=GE&geo=AL&geo=TR&geo=UA&geo=XK&geo=BE&time=2012&time=2013&time=2014&time=2015&time=2016&time=2017&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023"

    # Request the data
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    values = data['value']
    geo_labels = data['dimension']['geo']['category']['label']
    geo_indices = data['dimension']['geo']['category']['index']
    time_labels = data['dimension']['time']['category']['label']
    time_indices = data['dimension']['time']['category']['index']

    # Create a sorted list of full country names based on the index
    sorted_countries = [geo_labels[code] for code in sorted(geo_indices, key=geo_indices.get)]
    sorted_times = sorted(time_indices, key=time_indices.get)

    # Create an empty DataFrame to store the data with full country names
    df = pd.DataFrame(index=sorted_countries, columns=sorted_times)

    # Populate the DataFrame with the values
    for index, value in values.items():
        # Since the index is a single key, we need to map it to the correct country and time
        country_idx = int(index) // len(time_indices)  # Determinec which country the value belongs to
        time_idx = int(index) % len(time_indices)      # Determine which time period the value belongs to

        # Get the actual country name and time label
        country_code = list(geo_indices.keys())[country_idx]
        country = geo_labels[country_code]  # Use full country name
        time = time_labels[list(time_indices.keys())[time_idx]]

        # Insert the value into the correct place in the DataFrame
        df.loc[country, time] = value

    with st.container():
        # Input field for selecting the country
        country = st.text_input("Please enter an European country (e.g. Spain) for a tailored bar chart (case sensitive!):", "European Union")
    
        if country.lower() == "european union":
            country = "European Union - 27 countries (from 2020)"

        # Check if the entered country is in the DataFrame
        if country == "":
            st.warning("Please enter a country name.") # Give warning if no input is provided
        elif country not in df.index:
            st.warning("European country not found. Please check your spelling.") # Give warning that the input is not recognized 
        elif country in df.index:
            # Filter the data for the selected country
            country_df = df.loc[country].reset_index()
            country_df.columns = ['Year', 'Value']  # Rename columns for easier access in Altair

            # Create the bar chart with Altair
            chart = alt.Chart(country_df).mark_bar().encode(
                x=alt.X('Year:O', title='Year'),
                y=alt.Y('Value:Q', title= 'Number of New Passenger Cars Sold'),
                tooltip=['Year', 'Value']
            ).properties(
                title=f'New EV passenger car sales in {country}',
                width=1200,
                height=600  
            )

        final_chart = chart
        st.altair_chart(final_chart)
    
    with st.container():

        # Rename the index column to Country for filtering
        df = df.reset_index().rename(columns={'index': 'Country'})
        # Create a df_long to include year numbers
        df_long = df.melt(id_vars='Country', var_name='Year', value_name='Number of New Passenger Cars Sold')

        # Multi-select dropdown to choose up to 8 countries
        selected_countries = st.multiselect(
            "Select up to 8 countries to generate a line chart for comparison:",
            options=df_long['Country'].unique(),
            max_selections=8
        )

        # Filter the data based on selected countries
        filtered_df = df_long[df_long['Country'].isin(selected_countries)]

        # Debug: Display filtered DataFrame to ensure correct filtering
        st.write("Filtered Data:", filtered_df)

        # Check if any countries are selected
        if not filtered_df.empty:
            # Ensure data types are compatible with Altair
            filtered_df['Year'] = filtered_df['Year'].astype(str)  # Convert Year to string if it's categorical
            filtered_df['Number of New Passenger Cars Sold'] = pd.to_numeric(filtered_df['Number of New Passenger Cars Sold'], errors='coerce')

            # Create a selection parameter for highlighting on hover
            highlight = alt.selection_point(on='pointerover', fields=['Country'], nearest=True)

            # Create chart base
            base = alt.Chart(filtered_df).encode(
                x=alt.X('Year:O', title='Year'),  # Use 'O' (ordinal) or 'T' (temporal) depending on data format
                y=alt.Y('Number of New Passenger Cars Sold:Q', title='Number of New Passenger Cars Sold'),
                color=alt.Color('Country:N', legend=alt.Legend(title="Country"))
            )

            # Adding invisible points for selection with hover highlight
            points = base.mark_circle().encode(
                opacity=alt.value(0)
            ).add_params(
                highlight
            ).properties(
                width=1200,
                height=600
            )

            # Adding line charts with size change on hover highlight
            lines = base.mark_line().encode(
                size=alt.condition(~highlight, alt.value(1), alt.value(3))
            )

            # Combine points and lines
            chart2 = points + lines

            # Display the chart
            st.altair_chart(chart2)
        else:
            # Show a message if no countries are selected or if filtered_df is empty
            st.warning("Please select at least one country to view the chart.")





