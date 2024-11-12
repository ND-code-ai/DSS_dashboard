import numpy as np
import pandas as pd
import requests
from load_db import load_data_to_db
def get_outlier_indices_IQR_method(data:np.array) -> np.array:
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = np.where((data < lower_bound) | (data > upper_bound))

    return outliers


def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.iloc[1]
    df.columns.name = 'Index'

    df = df[2:]
    df.reset_index(drop=True, inplace=True)
    df.rename({'Recharging Power / Recharging Point': 'Power per station (kW)', 'Recharging Power / Total Light Duty PEV fleet': 'Power available per fleet'}, axis=1, inplace=True)
    
    df['Power per station (kW)'] = df['Power per station (kW)'].str.replace(',', '.').astype(float)
    df['Power available per fleet'] = df['Power available per fleet'].str.replace(',', '.').astype(float)
    df = df.astype({'Country': 'str', 'Total Recharging Power Output (kW)': 'int32', 'Recharging Points': 'int32', 'Light Duty PEV Fleet': 'int32'}, copy=False)


    print("NaN in NoC dataframe: ", df.isnull().sum().sum())
    print("Number of duplicates in NoC dataframe: ", df.duplicated().sum())
    print("\nSome outlier examples:")
    print("Power per station (kW): ", df.loc[get_outlier_indices_IQR_method(df['Power per station (kW)']), 'Country'].values)
    print("Power available per fleet: ", df.loc[get_outlier_indices_IQR_method(df['Power available per fleet']), 'Country'].values)
    
    return df

def preprocess_emissions_data(csv_file_path: str) -> pd.DataFrame: #dataframe
    df = pd.read_csv(csv_file_path)
    df = df[['ID', 'Country', 'z (Wh/km)', 'year']]
    df.dropna(subset=['z (Wh/km)'], inplace=True)
    
    outlier_indices = get_outlier_indices_IQR_method(df['z (Wh/km)'].to_numpy())
    print("Outliers in 'z (Wh/km)' at indices:", outlier_indices)
    
    df = df.drop(index=outlier_indices[0])

    return df

def preprocess_EV_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.replace(0, np.nan, inplace=True)
    
    return df

def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    pass

def scrape_sales_data() -> pd.DataFrame:
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
        # Since the index is a single key, we need to map it to the correct country and time
        country_idx = int(index) // len(time_indices)  # Determinec which country the value belongs to
        time_idx = int(index) % len(time_indices)      # Determine which time period the value belongs to

        # Get the actual country name and time label
        country_code = list(geo_indices.keys())[country_idx]
        country = geo_labels[country_code]  # Use full country name
        time = time_labels[list(time_indices.keys())[time_idx]]

        # Insert the value into the correct place in the DataFrame
        df.loc[country, time] = value
    
    sales_data = df

    return sales_data
def main():
    all_dataframes = {}
    
    sales_data = scrape_sales_data()
    cleaned_sales_data = preprocess_EV_sales(sales_data)
    all_dataframes['EV sales'] = cleaned_sales_data
    ### Sales data


    emissions_data = preprocess_emissions_data('data/reduced_energyc1.csv')
    all_dataframes['Emissions'] = emissions_data
    noc_data = pd.read_csv('src/data/scraped_NoC_data.csv')
    cleaned_noc_data = preprocess_EV_infrastructure(noc_data)
    all_dataframes['EV infrastructure'] = cleaned_noc_data

    # insert other preprocessing functions and dataframes here
    print(cleaned_noc_data.head())
    return all_dataframes


   
