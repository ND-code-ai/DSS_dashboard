# Team 14 - Dashboard for Exploring State of EV Adoption in Europe

---  

---  

# INFOMDDS - Dashboard
This dashboard shows the current state of EV usage among European countries.

## Running the App
To run the dashboard make sure you have a valid docker installation on machine. Run "docker compose up" in the root directory of the dashboard where the docker-compose.yml file is located (eg. in DSS_Dashboard/)
## !!! Docker compose takes long (because of the data preparation), please have patience

### Link to the Codebase: 
https://github.com/ND-code-ai/DSS_dashboard/tree/main

### Datasets: available under 'data'-folder
### Other links: NA

## Data Collection and Preparation
    app.py
    Sets up the dashboard and loads the plots
    
    group14_preparedata.py
    Data collection and preparation for plots. 
    Due to version issues, EV_em_and_sales.py makes use of a pre-loaded CSV file. Collection and preparation are still visible in both the group14_preparedata.py as well as in the notebook EV_em_and_sale.ipynb in the notebook branch.

    load_db.py
    Loads the files prepared by group14-preparedata.py and saves them in the postgre database in the docker container.

    DSS_dashboard\src\st_pages (folder)
    Contains python files that generate the plots for each KPI on separate streamlit pages:
        emissions.py
        Bar chart of total electric energy consumption per European country in 2023.

        EV_Prices_DE.py
        Plots on EV prices and its relation to various factors in Germany.

        EV_Infrastructure.py
        Plots on EV charging stations per country.

        EVSales.py
        Plots on number of new EV passenger cars sold per year per country.

        EV_em_and_sales.py
        Plot on average emissions of person vehicles and number of new EV passenger cars sold per country.

## Data Sources
    1. Vector data for plots on charging infrastructure - geodata
    2. Properties of Electric Vehicles - EV_cars.csv
    3. Properties of EV recharging stations infrastructure per country - cleaned - cleaned_NoC_data.csv
    4. New passenger car sales (EV) in Europe - cleaned_NoEVS_data.csv
    5. Energy consumption per country - reduced_energyc1.csv
    6. Scraped data on recharging infrastructure - not cleaned - scraped_NoC_data.csv
    7. Average emissions of new passenger vehicles in Europe and new EV sales in Europe - EV_em_and_sales.csv

## Existing Indicators and Visualizations
    1. Number of Charging Stations
        Number of recharging points to Power per station, by country. Map of Europe showing total recharging power output by country. 
        Generated by EVInfastructure.py
    2. EV Sales
        New passenger EV car sales in the EU over the years 2014 - 2023.
        Generated by EVSales.py
    3. EV Prices
        Price range of EV in relation to several related properties of EVs for Germany.
        Generated by EV_Prices_DE.py
    4. EV Electric Usage
        Total electric energy consumption compared between countries, as well as total electric energy consumption per country over several years.
        Generated by emissions.py
    5. EV Emissions and Sales
        Average C02 emissions of new passenger cars and EV sales trends per country per year. 
        Generated by EV_em_and_sale.py
        
