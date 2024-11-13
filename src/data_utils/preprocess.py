import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def get_outlier_indices_IQR_method(data: np.array) -> np.array:
    """
    Identify outliers in the data using the Interquartile Range (IQR) method.

    Parameters:
    data (np.array): Array of numerical data.

    Returns:
    np.array: Indices of outliers in the data.
    """
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = np.where((data < lower_bound) | (data > upper_bound))

    return outliers

def predict_missing_values(df: pd.DataFrame, country: str, proportion_nan_allowed: float = 0.5):
    """
    Predict missing values for a given country using linear regression.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    country (str): Country for which to predict missing values.
    proportion_nan_allowed (float): Maximum allowed proportion of missing values.

    Returns:
    tuple: Indices of missing values and their predicted values.
    """
    is_nan = df.loc[country].isna()
    proportion_nan = is_nan.sum() / len(is_nan)

    if proportion_nan > proportion_nan_allowed:
        return (None, None)
    elif proportion_nan == 0:
        return (None, None)
    
    filtered_nan_year_index = df.loc[country, :].loc[is_nan].index
    filtered_non_nan: pd.Series = df.loc[country, :].dropna().astype(float)
    filtered_non_nan_values: np.ndarray = filtered_non_nan.values.reshape(-1, 1)

    non_nan_years = np.array([int(year) for year in filtered_non_nan.index]).reshape(-1, 1)
    model = LinearRegression().fit(non_nan_years, filtered_non_nan_values)

    predicted_values = model.predict(np.array([int(year) for year in filtered_nan_year_index]).reshape(-1, 1))
    return filtered_nan_year_index, predicted_values.flatten()

def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the EV infrastructure data.

    Parameters:
    df (pd.DataFrame): DataFrame containing the raw data.

    Returns:
    pd.DataFrame: Preprocessed DataFrame.
    """
    new_df = df.copy()
    new_df.rename({'Recharging Power / Recharging Point': 'Power per station (kW)', 'Recharging Power / Total Light Duty PEV fleet': 'Power available per fleet'}, axis=1, inplace=True)
    
    new_df.loc[:, 'Power per station (kW)'] = new_df['Power per station (kW)'].str.replace(',', '.').astype(float)
    new_df.loc[:, 'Power available per fleet'] = new_df['Power available per fleet'].str.replace(',', '.').astype(float)
    new_df = new_df.astype({'Country': 'str', 'Total Recharging Power Output (kW)': 'int32', 'Recharging Points': 'int32', 'Light Duty PEV Fleet': 'int32'}, copy=False)

    return new_df


def preprocess_emissions_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the emissions data.

    Parameters:
    df (pd.DataFrame): DataFrame containing the raw emissions data.

    Returns:
    pd.DataFrame: Preprocessed DataFrame with NaN values dropped and outliers removed.
    """
    # Drop rows with NaN values in the 'z (Wh/km)' column
    df.dropna(subset=['z (Wh/km)'], inplace=True)

    # Identify outliers in the 'z (Wh/km)' column using the IQR method
    outlier_indices = get_outlier_indices_IQR_method(df['z (Wh/km)'].to_numpy())

    # Drop the identified outliers from the DataFrame
    df = df.drop(index=outlier_indices[0])

    return df

def preprocess_EV_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the EV sales data.

    Parameters:
    df (pd.DataFrame): DataFrame containing the raw EV sales data.

    Returns:
    pd.DataFrame: Preprocessed DataFrame with NaN values replaced by 0.
    """
    df = df.copy()
    df.replace(np.nan, 0, inplace=True)
    
    return df
def preprocess_em_and_sales_data(df: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the emissions and sales data by predicting missing values, merging, and subsetting.

    Parameters:
    df (pd.DataFrame): DataFrame containing the emissions data.
    df2 (pd.DataFrame): DataFrame containing the EV sales data.

    Returns:
    pd.DataFrame: Preprocessed DataFrame containing merged and cleaned emissions and sales data.
    """
    for country in df.index:
        filtered_nan_year_index, predicted_values = predict_missing_values(df, country)
        if filtered_nan_year_index is not None:
            df.loc[country, filtered_nan_year_index] = predicted_values

    df = df.dropna()

    df_em = pd.melt(df.reset_index(), id_vars='index', value_vars=df.iloc[1:],
                    var_name='Year', value_name='Emissions').rename(columns={'index': 'Country'})
    df_em = df_em.sort_values(by=['Country', 'Year'])

    df_EV = pd.melt(df2, id_vars='Country', value_vars=df2.iloc[1:],
                    var_name='Year', value_name='Nr_of_new_EVs')
    df_EV = df_EV.sort_values(by=['Country', 'Year'])

    df_all = df_em.merge(df_EV, how='left', on=['Country', 'Year'])

    df_all['Year'] = df_all['Year'].astype('int')

    # Turning Nr_of_new_EVs into an integer for easier working with the data
    df_all.loc[:, 'Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].astype('str').str.replace(".", "")  # Removing thousands separators
    df_all['Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].astype('float')  # Converting to float due to NaNs

    # Subsetting data for years 2017 and onwards
    df_17_up = df_all[df_all['Year'] >= 2017]

    return df_17_up

def preprocess_EV_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the EV prices data by categorizing prices into bins.

    Parameters:
    df (pd.DataFrame): DataFrame containing the raw EV prices data.

    Returns:
    pd.DataFrame: Preprocessed DataFrame with an additional 'Price_category' column.
    """
    price_bins = [0, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 200000]
    price_labels = ['<30k', '30-40k', '40-50k', '50-60k', '60-70k', '70k-80k', '80k-90k', '>90k']
    df['Price_category'] = pd.cut(df['Price.DE.'], bins=price_bins, labels=price_labels)

    return df
