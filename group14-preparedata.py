import numpy as np
import pandas as pd

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

def preprocess_EV_sales(df: pd.DataFrame) -> pd.DataFrame:
    pass

def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    pass

def main():
    all_dataframes = {}

    noc_data = pd.read_csv('data/src/scraped_NoC_data.csv')
    cleaned_noc_data = preprocess_EV_infrastructure(noc_data)
    all_dataframes['NoC'] = cleaned_noc_data

    # add more preprocessing function calls here

    return all_dataframes


   