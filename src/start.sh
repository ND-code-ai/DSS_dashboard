#!/bin/sh

python load_db.py &&

echo -e "Application is starting..."
echo -e "\e[1;31m WARNING:  \e[0m Access the app at:  http://localhost:8501/ OR other URL specified"


streamlit run app.py --server.port=8501 --server.address=0.0.0.0
