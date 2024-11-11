import numpy as np
import pandas as pd
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
    pass

def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    pass

def main():
    all_dataframes = {}
    
    emissions_data = preprocess_emissions_data('data/reduced_energyc1.csv')
    all_dataframes['Emissions'] = emissions_data
    noc_data = pd.read_csv('src/data/scraped_NoC_data.csv')
    cleaned_noc_data = preprocess_EV_infrastructure(noc_data)
    all_dataframes['EV infrastructure'] = cleaned_noc_data

    # insert other preprocessing functions and dataframes here

    load_data_to_db(all_dataframes)


if __name__ == '__main__':
    main()

   
