# Libraries
import streamlit as st
import pandas as pd
import altair as alt


def main(df_em: pd.DataFrame) -> None:

    # Exploring the trend of emissions over the years for each country
    # Bar plots
    
    lst = df_em['Country'].unique()
    input_dropdown = alt.binding_select(options=lst, name='Country ')
    selection = alt.selection_point(fields=['Country'], bind=input_dropdown, value = 'Austria')

    # A peculiar trend was shown around the year 2018 for each country that had data from before and after 2018. When analysing the metadata, it appeared a new 
    # measuring system was used such that only the years 2000-2016 are comparable with each other and the years 2017 and up are comparable with each other.
    # To obtain reliable insights regarding the trend, later on the data will be split for these two time periods.


        
    # Chart depicting relationship between emissions and number of new EVs over the years for period 2017 and up
    base2 = alt.Chart(df_em).encode(
        alt.X('Year:O').title('Year'))

    bar_chart3 = base2.mark_bar().encode(
        alt.Y('Emissions:Q').title('Emissions'),
        tooltip=['Year', 'Emissions'],
        color=alt.value('#93a8cc')
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title=(f'Average C02 emissions per km from new passenger cars for selected country'),
        width=500,
        height=550
    )    

    line_chart2 = base2.mark_line(stroke='#203864', interpolate='monotone').encode(
        alt.Y('Nr_of_new_EVs').title('Nr of new EVs'),
        tooltip=['Year', 'Nr_of_new_EVs']
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        width=500,
        height=550
    )    
            
    full_chart_17_up = alt.layer(bar_chart3, line_chart2).resolve_scale(
        y='independent'
    ).configure(background='#FFFFFF'
    ).configure_axis(
    labelColor='#000000', 
    titleColor='#000000'   
    ).configure_title(
    color='#000000' 
    )
            
    full_chart_17_up
        
    st.altair_chart(full_chart_17_up)
    
    
    
