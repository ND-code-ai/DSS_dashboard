import streamlit as st
import pandas as pd
import altair as alt

def main():
   col = st.columns((8, 1), gap='medium')
   df = pd.read_csv("data/cleaned_NoC_data.csv")

   with col[0]:
        bubble_chart = alt.Chart(df).mark_circle().encode(
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

        text_labels = alt.Chart(df).mark_text(
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
        final_chart = bubble_chart + text_labels


        st.altair_chart(final_chart)
        st.write("<h1 style='font-size: 25px;'>This is a temporary chloreopleth map of Europe, it will be replace with interactive map</h1>", unsafe_allow_html=True)
        st.image("data/map.png", use_column_width=True, caption="Electric Vehicle Charging Stations by Country", output_format="PNG")
