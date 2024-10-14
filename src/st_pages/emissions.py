import pandas as pd
import streamlit as st
import random
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# Load and process the data
csv_file_path = 'data/reduced_energyc1.csv'
df = pd.read_csv(csv_file_path)

# Select specific columns and filter data for the year 2023
selected_columns = df[['ID', 'Country', 'Mk', 'Ft', 'z (Wh/km)', 'year', 'Electric range (km)']]
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

# Create the pyecharts bar chart
bar_chart = (
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
        toolbox_opts=opts.ToolboxOpts(),  # Add toolbox options for interaction
    )
)

# Display the bar chart in Streamlit using st_pyecharts
st_pyecharts(bar_chart, key="echarts")

# Add a button to randomize the data (for demonstration)
if st.button("Randomize data"):
    random_values = random.sample(range(100), len(countries))  # Randomize values just for fun
    bar_chart.add_yaxis("Total Energy Consumption (z Wh/km)", random_values, label_opts=opts.LabelOpts(is_show=False))  # Hide labels
    st_pyecharts(bar_chart, key="randomized_chart")

st.write("This is an interactive chart of the total electric energy consumption per country in 2023.")
