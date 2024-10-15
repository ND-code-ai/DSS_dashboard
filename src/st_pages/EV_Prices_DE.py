import pandas as pd
import altair as alt
import streamlit as st

def main():

    # Load the data
    df = pd.read_csv('data/EV_cars.csv')

    # Price Distribution of Electric Vehicles
    st.title('Electric Vehicle Data Visualizations')

    # Price Distribution
    """    st.subheader('Price Distribution of Electric Vehicles')
    price_hist = alt.Chart(df).mark_bar().encode(
        alt.X('Price.DE.', bin=alt.Bin(maxbins=30), title='Price (EUR)'),
        alt.Y('count()', title='Frequency'),
        tooltip=['Price.DE.', 'count()']
    ).properties(width=600, height=400).interactive()"""

    """"mean_price = df['Price.DE.'].mean()
    median_price = df['Price.DE.'].median()

    mean_rule = alt.Chart(pd.DataFrame({'Price': [mean_price]})).mark_rule(color='red').encode(x='Price')
    median_rule = alt.Chart(pd.DataFrame({'Price': [median_price]})).mark_rule(color='black').encode(x='Price')

    st.altair_chart(price_hist + mean_rule + median_rule)
    """
    # Price vs Range Scatter Plot
    """st.subheader('Price vs. Range')
    price_range_scatter = alt.Chart(df).mark_circle(size=60, color='blue').encode(
        x=alt.X('Range', title='Range (km)'),
        y=alt.Y('Price.DE.', title='Price (EUR)'),
        tooltip=['Price.DE.', 'Range']
    ).properties(width=600, height=400).interactive()
    st.altair_chart(price_range_scatter)"""

    # Price Categories vs Range Boxplot
    st.subheader('Price Categories vs. Range')
    price_bins = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 200000]
    price_labels = ['<30k', '30-40k', '40-50k', '50-60k', '60-70k', '70k-80k', '80k-100k', '>100k']
    df['Price_category'] = pd.cut(df['Price.DE.'], bins=price_bins, labels=price_labels)

    boxplot = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('Price_category', title='Price Category (EUR)'),
        y=alt.Y('Range', title='Range (km)'),
        color='Price_category'
    ).properties(width=600, height=400).interactive()
    st.altair_chart(boxplot)

    # Efficiency by Price Category
    st.subheader('Price Categories vs. Efficiency')
    efficiency_by_price = df.groupby('Price_category')['Efficiency'].mean().reset_index()
    efficiency_bar = alt.Chart(efficiency_by_price).mark_bar().encode(
        x=alt.X('Efficiency', title='Average Efficiency (Wh/km)'),
        y=alt.Y('Price_category', title='Price Range (EUR)'),
        color=alt.Color('Efficiency', scale=alt.Scale(scheme='blues'))
    ).properties(width=600, height=400).interactive()
    st.altair_chart(efficiency_bar)

    # Price vs. Fast-Charging Time
    """st.subheader('Price vs. Fast-Charging Time')
    charging_scatter = alt.Chart(df).mark_circle(size=60, color='blue').encode(
        x=alt.X('Price.DE.', title='Price (EUR)'),
        y=alt.Y('Fast_charge', title='Fast Charging Time (minutes)'),
        tooltip=['Price.DE.', 'Fast_charge']
    ).properties(width=600, height=400).interactive()
    st.altair_chart(charging_scatter)
    """
    # Fast-Charging Time by Price Category
    st.subheader('Price Categories vs. Fast-Charging Time')
    avg_fast_charge = df.groupby('Price_category')['Fast_charge'].mean().reset_index()
    fast_charge_bar = alt.Chart(avg_fast_charge).mark_bar().encode(
        x=alt.X('Price_category', title='Price Category (EUR)'),
        y=alt.Y('Fast_charge', title='Fast-Charging Time (minutes)'),
        color=alt.Color('Fast_charge', scale=alt.Scale(scheme='blues'))
    ).properties(width=600, height=400).interactive()
    st.altair_chart(fast_charge_bar)

    # Price vs Acceleration
    """st.subheader('Price vs Acceleration')
    acceleration_scatter = alt.Chart(df).mark_circle(size=60, color='blue').encode(
        x=alt.X('acceleration..0.100.', title='Acceleration (0-100 km/h, seconds)'),
        y=alt.Y('Price.DE.', title='Price (EUR)'),
        tooltip=['acceleration..0.100.', 'Price.DE.']
    ).properties(width=600, height=400).interactive()
    st.altair_chart(acceleration_scatter)"""

    # Price vs Top Speed
    """st.subheader('Price vs Top Speed')
    top_speed_scatter = alt.Chart(df).mark_circle(size=60, color='blue').encode(
        x=alt.X('Price.DE.', title='Price (EUR)'),
        y=alt.Y('Top_speed', title='Top Speed (km/h)'),
        tooltip=['Price.DE.', 'Top_speed']
    ).properties(width=600, height=400).interactive()
    st.altair_chart(top_speed_scatter)

    # Price vs Battery Capacity
    st.subheader('Price vs Battery Capacity')
    battery_scatter = alt.Chart(df).mark_circle(size=60, color='blue').encode(
        x=alt.X('Price.DE.', title='Price (EUR)'),
        y=alt.Y('Battery', title='Battery Capacity (kWh)'),
        tooltip=['Price.DE.', 'Battery']
    ).properties(width=600, height=400).interactive()
    st.altair_chart(battery_scatter)"""
