import pandas as pd
import altair as alt
import streamlit as st


csv_file_path = 'data/reduced_energyc1.csv'
nieuwe_dataset = reduced_energyc1.csv.loc[year, z (Wh/km),ID]
df = pd.read_csv(csv_file_path)

# Select specific columns
selected_columns = df[['ID', 'Country', 'Mk', 'Ft', 'z (Wh/km)', 'year', 'Electric range (km)']]

# Filter data for the year 2023
data_2023 = selected_columns[selected_columns['year'] == 2023]

# Group by 'Country' and sum 'z (Wh/km)' for 2023
total_z_per_country = data_2023.groupby('Country')['z (Wh/km)'].sum().reset_index()

# Round the values to the nearest thousand
total_z_per_country['z (Wh/km)'] = (total_z_per_country['z (Wh/km)'] / 1000).round(0)  # Round to the nearest thousand

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

# Prepare the data for Altair, ensuring 'Country' is ordered based on 'values'
source = pd.DataFrame({
    "Country": total_z_per_country['Country'],
    "values": total_z_per_country['z (Wh/km)']
})

# Create a categorical type for the Country column based on the sorted values
source['Country'] = pd.Categorical(source['Country'], categories=source['Country'], ordered=True)

# Selection interactions
hover = alt.selection_single(name="hover", fields=['Country'], empty="none")

# Create an interactive bar chart
bars = alt.Chart(source).mark_bar(
    fill="#4C78A8", stroke="black", cursor="pointer"
).encode(
    x=alt.X('Country:N', title='Country'),  # Abbreviations on the X-axis
    y=alt.Y('values:Q', title='Total Electric Energy Consumption (z Wh/km)', axis=alt.Axis(format='~s')),  # Format axis
    fillOpacity=alt.condition(hover, alt.value(1), alt.value(0.3)),  # Adjust bar opacity on hover
    strokeWidth=alt.condition(hover, alt.value(2), alt.value(0.5)),  # Stroke width on hover
    color=alt.Color('Country:N', legend=None),  # Color bars by country
    tooltip=['Country:N', 'values:Q']  # Add tooltip to show country and value
).properties(
    title='Total Electric Energy Consumption (z Wh/km) per Country in 2023',
    width=600,
    height=400
).add_params(hover)

# Create a textbox for the values
text_background = alt.Chart(source).mark_rect(
    fill='lightgray',  # Background color
    opacity=0.8  # Background opacity
).encode(
    x=alt.X('Country:N'),
    y=alt.Y('values:Q'),
    size=alt.Size(value=40)  # Fixed size for the box
).transform_filter(hover)

# Add bold text to display values only on hover
text = alt.Chart(source).mark_text(
    align='center', dy=-10, color='black', fontWeight='bold'
).encode(
    x=alt.X('Country:N'),
    y=alt.Y('values:Q'),
    text=alt.condition(hover, 'values:Q', alt.value('')),  # Show text only on hover
    opacity=alt.condition(hover, alt.value(1), alt.value(0))  # Make text appear on hover
)

# Combine bars, text background, and text
chart = bars + text_background + text

# Display the interactive chart
chart

# Load your data
csv_file_path1 = 'data/energyc2.csv'  # Adjust the path as needed
df = pd.read_csv(csv_file_path1)

st.title("Energy Consumption Data")

# Display the first few rows of the dataframe
st.write(df.head())

# You can add more functionality here, like plotting, filtering, etc.

