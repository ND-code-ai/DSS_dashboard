import pandas as pd
import altair as alt
import streamlit as st

def main():

    # Load the data
    df = pd.read_csv('data/EV_cars.csv')

    # Define price categories
    price_bins = [0, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 200000]
    price_labels = ['<30k', '30-40k', '40-50k', '50-60k', '60-70k', '70k-80k', '80k-900k', '>90k']
    df['Price_category'] = pd.cut(df['Price.DE.'], bins=price_bins, labels=price_labels)

    # Title and Dropdown Menus for Chart Selection
    st.title('Electric Vehicle Data Visualizations')
    
    # Dropdown for price category charts
    price_category_option = st.selectbox('Choose a Price Category vs Attribute Chart', [
        'Price Categories vs Range',
        'Price Categories vs Efficiency',
        'Price Categories vs Fast-Charging Time'
    ])

# Display the selected price category chart

    #Price Categories vs. Range
    if price_category_option == 'Price Categories vs Range':
        st.subheader('Price Categories vs. Range')
        boxplot = alt.Chart(df).mark_boxplot().encode(
            x=alt.X('Price_category', title='Price Category (EUR)'),
            y=alt.Y('Range:Q', title='Range (km)'),
            color='Price_category'
        ).properties(width=600, height=400).interactive()
        st.altair_chart(boxplot)

    #Price Categories vs. Efficiency
    elif price_category_option == 'Price Categories vs Efficiency':
        st.subheader('Price Categories vs. Efficiency')
        efficiency_by_price = df.groupby('Price_category')['Efficiency'].mean().reset_index()
        efficiency_bar = alt.Chart(efficiency_by_price).mark_bar().encode(
            x=alt.X('Efficiency:Q', title='Average Efficiency (Wh/km)'),
            y=alt.Y('Price_category', title='Price Range (EUR)'),
            color=alt.Color('Efficiency:Q', scale=alt.Scale(scheme='blues'))
        ).properties(width=600, height=400).interactive()
        st.altair_chart(efficiency_bar)

    #Price Categories vs. Fast-Charging Time
    elif price_category_option == 'Price Categories vs Fast-Charging Time':
        st.subheader('Price Categories vs. Fast-Charging Time')
        avg_fast_charge = df.groupby('Price_category')['Fast_charge'].mean().reset_index()
        fast_charge_bar = alt.Chart(avg_fast_charge).mark_bar().encode(
            x=alt.X('Price_category', title='Price Category (EUR)'),
            y=alt.Y('Fast_charge:Q', title='Fast-Charging Time (minutes)'),
            color=alt.Color('Fast_charge:Q', scale=alt.Scale(scheme='blues'))
        ).properties(width=600, height=400).interactive()
        st.altair_chart(fast_charge_bar)
