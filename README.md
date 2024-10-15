# Team 14 - Dashboard for Exploration of Adoption of EVs in Europe

---  

---  

# INFOMDDS - Dashboard
The current dashboard is an interim build, and is a work in progress

## Installation
To run the dashboard make sure you have a valid docker installation on machine. Run docker compose up in the root directory of the dashboard where the docker-compose.yml file is located (eg. in DSS_Dashboard/)

## Running the app
    In the project root folder, first download the initial dataset using:
        pip install -r mylib
        python groupxx-preparedata.py
    After the script runs, the dashboard can be launched using:
        docker-compose up -d

### Link to the video: https://youtube.com/our-project
### Link to the codebase: https://github.com/ND-code-ai/DSS_dashboard/tree/main
### Datasets: available under 'data'-folder
### Other links: NA

## Data Collection and Preparation
    Data collection and preparation is done within each file under "st_pages" for the plots generated in those files. 

    API_Eurostats.ipynb
    API fetches for the Eurostat data.

    emissions.py
    Data collection and preparation of total electric energy consumption per European country in 2023 and generated bar chart to visualise it.

    EV_Prices_DE.py
    Plots on EV prices and its relation to various factors in Germany.

    EVInfastructure.py
    Plots on EV charging stations per country.

    EVSales.py
    Data preparation on EV sales per country. Plots on number of new EV passenger cars sold per year per country.

    green_energy.py

    home.py    

## Data Sources
    1. ????????????????????????????????????????????- geodata
    2. Properties of Electric Vehicles - EV_cars.csv
    3. Properties of EV recharging stations infrastructure per country - cleaned - cleaned_NoC_data.csv
    4. ???????????????????????? - cleaned_NoEVS_data.csv
    5. ????????????? NOT A DATA SOURCE?????????????????????????- map.png
    6. Energy consumption per country - reduced_energyc1.csv
    7. Scraped data on recharging infrastructure - not cleaned - scraped_NoC_data.csv

## Existing Indicators and Visualizations
    1. 
    2.
    3.
    4.
    5.