#!/bin/sh

echo -e "Application is starting..."
echo -e "\e[1;31m WARNING:  \e[0m Access the app at:  http://localhost:8501/ OR other URL specified"

# Run Streamlit
streamlit run app.py --server.port=8501 --server.address=0.0.0.0