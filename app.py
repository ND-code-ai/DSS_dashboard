import streamlit as st
import pandas as pd
 
st.write("""
Chart
""")
 
df = pd.read_csv("my_data.csv")
st.line_chart(df)
