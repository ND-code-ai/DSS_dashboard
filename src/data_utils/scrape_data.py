import requests
import pandas as pd

def scrape_sales_data() -> pd.DataFrame:
    """
    Scrape EV sales data from the Eurostat API.

    Returns:
    pd.DataFrame: DataFrame containing the scraped EV sales data.
    """
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_eqr_carpda/?format=JSON&lang=en&freq=A&unit=NR&mot_nrg=ELC&geo=EU27_2020&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=LI&geo=NO&geo=CH&geo=UK&geo=BA&geo=ME&geo=MD&geo=GE&geo=AL&geo=TR&geo=UA&geo=XK&geo=BE&time=2012&time=2013&time=2014&time=2015&time=2016&time=2017&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023"

    response = requests.get(url)
    data = response.json()

    values = data['value']
    geo_labels = data['dimension']['geo']['category']['label']
    geo_indices = data['dimension']['geo']['category']['index']
    time_labels = data['dimension']['time']['category']['label']
    time_indices = data['dimension']['time']['category']['index']

    sorted_countries = [geo_labels[code] for code in sorted(geo_indices, key=geo_indices.get)]
    sorted_times = sorted(time_indices, key=time_indices.get)

    df = pd.DataFrame(index=sorted_countries, columns=sorted_times)

    for index, value in values.items():
        # Determine which country and time period the value belongs to
        country_idx = int(index) // len(time_indices)
        time_idx = int(index) % len(time_indices)

        # Get the actual country name and time label
        country_code = list(geo_indices.keys())[country_idx]
        country = geo_labels[country_code]
        time = time_labels[list(time_indices.keys())[time_idx]]

        # Insert the value into the correct place in the DataFrame
        df.loc[country, time] = value
    
    sales_data = df
    
    return sales_data

def scrape_em_and_sales() -> pd.DataFrame:
    """
    Scrape emissions and sales data from the Eurostat API and merge with local CSV data.

    Returns:
    pd.DataFrame: DataFrame containing the merged emissions and sales data.
    """
    # Get data "Average CO2 emissions per km from new passenger cars" with API
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_13_31/?format=JSON&lang=en"

    # Request the data
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    values = data['value']
    geo_labels = data['dimension']['geo']['category']['label']
    geo_indices = data['dimension']['geo']['category']['index']
    time_labels = data['dimension']['time']['category']['label']
    time_indices = data['dimension']['time']['category']['index']

    # Create a sorted list of countries based on the index
    sorted_countries = [geo_labels[code] for code in sorted(geo_indices, key=geo_indices.get)]
    sorted_times = sorted(time_indices, key=time_indices.get)

    # Convert time_labels (years) to integers
    time_years = [int(time_labels[code]) for code in sorted_times]

    # Create a DataFrame to store data from the JSON response
    df = pd.DataFrame(index=sorted_countries, columns=time_years)

    # Insert the values from the JSON response in the DataFrame
    for index, value in values.items():
        country_id = int(index) // len(time_indices)
        time_idx = int(index) % len(time_indices)

        # Get the actual country name and time label
        country_code = list(geo_indices.keys())[country_id]
        country = geo_labels[country_code]
        time = int(time_labels[list(time_indices.keys())[time_idx]])

        # Insert the value into the correct place in the DataFrame
        df.loc[country, time] = value

    # Load additional data from a local CSV file
    csv_file_path = 'data/cleaned_NoEVS_data.csv'
    df2 = pd.read_csv(csv_file_path)

    return df, df2
