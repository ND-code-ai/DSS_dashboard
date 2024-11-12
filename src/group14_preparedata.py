import numpy as np
import pandas as pd
import requests


def get_outlier_indices_IQR_method(data:np.array) -> np.array:
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = np.where((data < lower_bound) | (data > upper_bound))

    return outliers


def preprocess_EV_infrastructure(df: pd.DataFrame) -> pd.DataFrame:
    df.rename({'Recharging Power / Recharging Point': 'Power per station (kW)', 'Recharging Power / Total Light Duty PEV fleet': 'Power available per fleet'}, axis=1, inplace=True)
    
    df.loc[:, 'Power per station (kW)'] = df['Power per station (kW)'].str.replace(',', '.').astype(float)
    df.loc[:, 'Power available per fleet'] = df['Power available per fleet'].str.replace(',', '.').astype(float)
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

def preprocess_EV_em_and_sales(df: pd.DataFrame) -> pd.DataFrame:
        ############################
    ## EMISSIONS DATASET
    ############################

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

    # Create a sorted list countries based on the index
    sorted_countries = [geo_labels[code] for code in sorted(geo_indices, key=geo_indices.get)]
    sorted_times = sorted(time_indices, key=time_indices.get)

    # Convert time_labels (years) to integers
    time_years = [int(time_labels[code]) for code in sorted_times]

    # Create a DataFrame to store data from the JSON response
    df = pd.DataFrame(index=sorted_countries, columns=time_years)

    # Insert the values from the JSON response in the DataFrame
    for index, value in values.items():
        country_id = int(index) // len(time_indices)  # Determine which country the value belongs to
        time_idx = int(index) % len(time_indices)      # Determine which time period the value belongs to

        # Get the actual country name and time label
        country_code = list(geo_indices.keys())[country_id]
        country = geo_labels[country_code]
        time = int(time_labels[list(time_indices.keys())[time_idx]])

        # Insert the value into the correct place in the DataFrame
        df.loc[country, time] = value

    ##########################################
    ## Impute missing values using regression
    ##########################################

    # define a function to fill NaN values with linear regression
    
    def predict_missing_values(country: str, proportion_nan_allowed: float = 0.5):
        is_nan = df.loc[country].isna()
        proportion_nan = is_nan.sum() / len(is_nan)

        if proportion_nan > proportion_nan_allowed:
            print(f"Skipping {country} because {proportion_nan:.2f} of the values are missing")
            return (None, None)
        elif proportion_nan == 0:
            print(f"Skipping {country} because there are no missing values")
            return (None, None)
        
        print(f"Predicting missing values for {country}")
        filtered_nan_year_index = df.loc[country,:].loc[is_nan].index
        filtered_non_nan: pd.Series = df.loc[country,:].dropna().astype(float)
        filtered_non_nan_values: np.ndarray = filtered_non_nan.values.reshape(-1, 1)

        non_nan_years = np.array([int(year) for year in filtered_non_nan.index]).reshape(-1, 1)
        model = LinearRegression().fit(non_nan_years, filtered_non_nan_values)

        predicted_values = model.predict(np.array([int(year) for year in filtered_nan_year_index]).reshape(-1, 1))
        return filtered_nan_year_index, predicted_values.flatten()

    for country in df.index:
        filtered_nan_year_index, predicted_values = predict_missing_values(country)
        if filtered_nan_year_index is not None:
            df.loc[country, filtered_nan_year_index] = predicted_values
            
    df = df.dropna()
   
    # Exploring the data
    print(df.head())  
    print(type(df))
    print(str(df))
    print(df.describe())
    print(df.columns)

    # Melting the data such that the seperate column years will become one column: "Year"
    df_em = pd.melt(df.reset_index(), id_vars='index', value_vars= df.iloc[1:],
                                    var_name = 'Year', value_name = 'Emissions').rename(columns={'index': 'Country'})
    df_em = df_em.sort_values(by=['Country', 'Year'])

    # Exploring the trend of emissions over the years for each country
    # Bar plots
    lst = df_em['Country'].unique()
    input_dropdown = alt.binding_select(options=lst, name='Country ')
    selection = alt.selection_point(fields=['Country'], bind=input_dropdown, value = 'Austria')

    # Interactive bar chart for just emissions
    bar_chart = alt.Chart(df_em).mark_bar().encode(
        x='Year:O', 
        y='Emissions:Q',
        tooltip=['Year', 'Emissions']
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title=(f'Average C02 emissions per year for selected country'),
        width=400,
        height=450
    )    
        
    bar_chart 
        
    # A peculiar trend was shown around the year 2018 for each country that had data from before and after 2018. When analysing the metadata, it appeared a new 
    # measuring system was used such that only the years 2000-2016 are comparable with each other and the years 2017 and up are comparable with each other.
    # To obtain reliable insights regarding the trend, later on the data will be split for these two time periods.

    ############################
    ## NEW EVs DATASET
    ############################

    # Fetching data that was cleaned and saved prior
    csv_file_path = 'data/cleaned_NoEVS_data.csv'
    df2 = pd.read_csv(csv_file_path)

    # Melting the data such that the seperate column years will become one column: "Year"
    df_EV = pd.melt(df2, id_vars='Country', value_vars= df2.iloc[1:],
                                    var_name = 'Year', value_name = 'Nr_of_new_EVs')
    df_EV = df_EV.sort_values(by=['Country', 'Year'])

    ############################
    ## BOTH DATASETS
    ############################

    # Left joining the data on emissions per country per year and data on new EVs and total new cars per country per year
    df_all = df_em.merge(df_EV, how='left', on=['Country', 'Year'])

    # Checking data types of dataframe
    print(df_all.dtypes)

    # Turning year into an integer for easier subsetting later on
    df_all['Year'] = df_all['Year'].astype('int')

    # Turning Nr_of_new_EVs into an integer for easier working with the data
    df_all['Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].astype('str').str.replace(".", "") # Turning it into a string and removing the thousands seperators
    df_all['Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].replace(":", np.nan).astype('float').astype('Int64') # due to NaN's, turning the variable first into floats necessary
    
    # Cutting the years at 2017, as the metadata states that data is only comparable for 2000 - 2016 and for 2017 - now
        # Subsetting data for years 2000 - 2016
    df_00_16 = df_all[df_all['Year'] <= 2016]

        # Subsetting data for years 2017 - now
    df_17_up = df_all[df_all['Year'] >= 2017]
    
    return df_17_up

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
    
    #sales_data = scrape_sales_data()
    #cleaned_sales_data = preprocess_EV_sales(sales_data)
    #all_dataframes['EV sales'] = cleaned_sales_data

    #emissions_data = preprocess_emissions_data('data/reduced_energyc1.csv')
    #all_dataframes['Emissions'] = emissions_data
    
    #df_17_up = preprocess_EV_sales(df_17_up)
    #all_dataframes['EV emissions and sales'] = df_17_up

    noc_data = pd.read_csv('data/scraped_NoC_data.csv')
    cleaned_noc_data = preprocess_EV_infrastructure(noc_data)
    all_dataframes['EV infrastructure'] = cleaned_noc_data

    return all_dataframes


   
