import pandas as pd
import streamlit as st
import random
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

def main():
    csv_file_path = 'data/reduced_energyc1.csv'
    df = pd.read_csv(csv_file_path)

    # Select specific columns and filter data for the year 2023
    selected_columns = df[['ID', 'Country', 'z (Wh/km)', 'year']]
    data_2023 = selected_columns[selected_columns['year'] == 2023]

    # Group by 'Country' and sum 'z (Wh/km)' for 2023
    total_z_per_country = data_2023.groupby('Country')['z (Wh/km)'].sum().reset_index()

    # Round the values to the nearest thousand
    total_z_per_country['z (Wh/km)'] = (total_z_per_country['z (Wh/km)'] / 1000).round(0)

    # Create a mapping of country abbreviations to full names
    country_mapping = {
        'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
        'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia',
        'ES': 'Spain', 'FI': 'Finland', 'FR': 'France', 'GR': 'Greece',
        'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland', 'IS': 'Iceland',
        'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia',
        'MT': 'Malta', 'NL': 'Netherlands', 'NO': 'Norway', 'PL': 'Poland',
        'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden', 'SI': 'Slovenia',
        'SK': 'Slovakia'
    }

    # Replace country abbreviations with full names
    total_z_per_country['Country'] = total_z_per_country['Country'].replace(country_mapping)

    # Sort by the values to have the largest on the left
    total_z_per_country.sort_values(by='z (Wh/km)', ascending=False, inplace=True)

    # Prepare the data for pyecharts
    countries = total_z_per_country['Country'].tolist()
    values = total_z_per_country['z (Wh/km)'].tolist()

    # Create the pyecharts bar chart for 2023
    bar_chart_2023 = (
        Bar()
        .add_xaxis(countries)  # Use countries on x-axis
        .add_yaxis("Total Energy Consumption (z Wh/km)", values, label_opts=opts.LabelOpts(is_show=False))  # Hide labels
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Total Electric Energy Consumption by Country", 
                subtitle="Data for 2023 (in thousands of Wh/km)"
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(is_show=True, font_size=8, rotate=45),  # Show labels, reduce font size, and rotate
                splitline_opts=opts.SplitLineOpts(is_show=True),  # Optional: Show grid lines for better readability
                interval=0  # Show all labels without skipping
            ),
            legend_opts=opts.LegendOpts(
                pos_bottom="0%",  # Position the legend at the bottom
                pos_left="center",  # Center the legend horizontally
            ),
            toolbox_opts=opts.ToolboxOpts(),  # Add toolbox options for interaction
        )
    )

    # Display the bar chart for 2023
    st_pyecharts(bar_chart_2023, key="chart_2023")

    # Add a button to randomize the data (for demonstration)
    if st.button("Randomize data for 2023"):
        random_values = random.sample(range(100), len(countries))  # Randomize values just for fun
        bar_chart_2023.add_yaxis("Total Energy Consumption (z Wh/km)", random_values, label_opts=opts.LabelOpts(is_show=False))  # Hide labels
        st_pyecharts(bar_chart_2023, key="randomized_chart_2023")

    st.write("This is an interactive chart of the total electric energy consumption per country in 2023.")


    # Load and process the data for the multiple-year chart
    selected_columns = df[['ID', 'Country', 'z (Wh/km)', 'year']]

    # Replace country abbreviations with full names
    selected_columns['Country'] = selected_columns['Country'].replace(country_mapping)

    # Create a list of countries for selection
    countries = selected_columns['Country'].unique().tolist()

    # Multiselect for countries
    selected_countries = st.multiselect("Choose countries", countries)

    if not selected_countries:
        st.error("Please select at least one country.")
    else:
        # Filter the data based on the selected countries
        filtered_data = selected_columns[selected_columns['Country'].isin(selected_countries)]

        # Group by 'year' and 'Country' to get the sum of 'z (Wh/km)'
        grouped_data = filtered_data.groupby(['year', 'Country'])['z (Wh/km)'].sum().reset_index()

        # Round the values to the nearest thousand
        grouped_data['z (Wh/km)'] = (grouped_data['z (Wh/km)'] / 1000).round(0)

        # Prepare data for pyecharts
        years = grouped_data['year'].unique().tolist()
        values_by_country = {country: grouped_data[grouped_data['Country'] == country]['z (Wh/km)'].tolist() for country in selected_countries}

        # Create the pyecharts bar chart for multiple years
        bar_chart_years = Bar()

        # Add data to the bar chart for each selected country
        for country, values in values_by_country.items():
            bar_chart_years.add_xaxis(years)  # Use years on x-axis
            bar_chart_years.add_yaxis(country, values, label_opts=opts.LabelOpts(is_show=False))  # Hide labels

        bar_chart_years.set_global_opts(
            title_opts=opts.TitleOpts(
                title="Total Electric Energy Consumption by Country Over Years", 
                subtitle="Data in thousands of Wh/km"
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(is_show=True, font_size=8, rotate=45),  # Rotate labels
                splitline_opts=opts.SplitLineOpts(is_show=True),  # Optional: Show grid lines for better readability
                interval=0  # Show all labels without skipping
            ),
            legend_opts=opts.LegendOpts(
                pos_bottom="0%",  # Move the legend to the bottom
                pos_left="center"  # Center the legend horizontally
            ),
            toolbox_opts=opts.ToolboxOpts(),  # Add toolbox options for interaction
        )

        # Display the bar chart for multiple years
        st_pyecharts(bar_chart_years, key="chart_years")

        # Add a button to randomize the data for the multi-year chart (for demonstration)
        if st.button("Randomize data for years"):
            random_values = random.sample(range(100), len(years))  # Randomize values just for fun
            for country in selected_countries:
                bar_chart_years.add_yaxis(country, random_values, label_opts=opts.LabelOpts(is_show=False))  # Hide labels
            st_pyecharts(bar_chart_years, key="randomized_chart_years")

        st.write("This is an interactive chart of the total electric energy consumption per country over the selected years.")
