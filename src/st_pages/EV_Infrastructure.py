import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

import geopandas as gpd

def main(df: pd.DataFrame) -> None:
   col = st.columns((8, 2), gap='small')
   df = pd.read_csv("data/cleaned_NoC_data.csv")
    
   is_scale_values = col[1].checkbox("Scale logarithmically", value=False)
   df_1 = df.copy()

   if is_scale_values:
    df_1['Recharging Points'] = np.log10(df['Recharging Points'])
    df_1['Power per station (kW)'] = np.log10(df['Power per station (kW)'])

   with col[0]:
        bubble_chart_1 = alt.Chart(df_1).mark_circle().encode(
            x='Recharging Points',
            y='Power per station (kW)',
            size=alt.Size('Total Recharging Power Output (kW)', scale=alt.Scale(range=[60, 1300]), legend=None),  
            color=alt.Color('Country', legend=None), 
            tooltip=['Country', 'Recharging Points', 'Power per station (kW)', 'Total Recharging Power Output (kW)']
        ).properties(
            title='Recharging Points vs. Power per Station by Country',
            width=850,
            height=650,
        ).interactive()

        bubble_chart_1.encoding.x.scale = alt.Scale(domain=[df_1['Recharging Points'].min(), df_1['Recharging Points'].max()])

        text_labels_1 = alt.Chart(df_1).mark_text(
            align='center',
            baseline='top',
            dy=15,
            color='white'  # Adjust this value to position the text below the bubble
        ).encode(
            x='Recharging Points',
            y='Power per station (kW)',
            text='Country'
        )

        # Combine the bubble chart and text labels
        final_chart_1 = bubble_chart_1 + text_labels_1
        
        st.altair_chart(final_chart_1)
        
        #df['Power available per fleet'] = np.log(df['Power available per fleet'])
        # plot power available per station against power per fleet
        bubble_chart_2 = alt.Chart(df).mark_circle().encode(
            x='Power per station (kW)',
            y='Power available per fleet',
            size=alt.Size('Total Recharging Power Output (kW)', scale=alt.Scale(range=[60, 1300]), legend=None),  
            color=alt.Color('Country', legend=None), 
            tooltip=['Country', 'Recharging Points', 'Power per station (kW)', 'Total Recharging Power Output (kW)']
        ).properties(
            title='EV recharging power distribution among european countries',
            width=850,
            height=650,
        ).interactive()

        #bubble_chart.encoding.x.scale = alt.Scale(domain=[df['Recharging Points'].min(), df['Recharging Points'].max()])

        text_labels_2 = alt.Chart(df).mark_text(
            align='center',
            baseline='top',
            dy=15,
            color='white'  # Adjust this value to position the text below the bubble
        ).encode(
            x='Power per station (kW)',
            y='Power available per fleet',
            text='Country'
        )
        final_chart_2 = bubble_chart_2 + text_labels_2
        
        st.altair_chart(final_chart_2)
        st.write("<h1 style='font-size: 25px;'>Interactive chloropleth map of charging stations in europe</h1>", unsafe_allow_html=True)
        # perhaps move to a combining dataframes script
        geo_df = gpd.read_file("data/geodata/europe.geojson")
       
        
        merged = geo_df.set_index('NAME').join(df.set_index('Country'))
        merged = merged.dropna()
        
        fig = px.choropleth(merged,
                            geojson=merged.geometry,
                            locations=merged.index,
                            color='Recharging Points',
                            projection="natural earth",
                            width=1000,
                            height=800,
                            color_continuous_scale="Viridis",
                            )
       
        
        fig.update_geos(fitbounds="locations", visible=False, bgcolor="#8b8b8b")
        st.plotly_chart(fig, use_container_width=True)
        
