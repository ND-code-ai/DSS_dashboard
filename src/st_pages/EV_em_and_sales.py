# Libraries
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import requests
from sklearn.linear_model import LinearRegression

def main():

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
    print(df_em.head())

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
    df_all

    # Checking data types of dataframe
    print(df_all.dtypes)

    # Turning year into an integer for easier subsetting later on
    df_all['Year'] = df_all['Year'].astype('int')
    print(np.dtype(df_all['Year']))

    # Turning Nr_of_new_EVs into an integer for easier working with the data
    df_all['Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].astype('str').str.replace(".", "") # Turning it into a string and removing the thousands seperators
    df_all['Nr_of_new_EVs'] = df_all['Nr_of_new_EVs'].replace(":", np.nan).astype('float').astype('Int64') # due to NaN's, turning the variable first into floats necessary
    print(df_all.dtypes)  
    
    # Cutting the years at 2017, as the metadata states that data is only comparable for 2000 - 2016 and for 2017 - now
        # Subsetting data for years 2000 - 2016
    df_00_16 = df_all[df_all['Year'] <= 2016]

        # Subsetting data for years 2017 - now
    df_17_up = df_all[df_all['Year'] >= 2017]

    ############################
    ## PLOTS
    ############################

    # Chart depicting relationship between emissions and number of new EVs over the years for period 2000-2016

    base = alt.Chart(df_00_16).encode(
        alt.X('Year:O').title('Year'))

    bar_chart2 = base.mark_bar().encode(
        alt.Y('Emissions:Q').title('Emissions'),
        tooltip=['Year', 'Emissions'],
        color=alt.value('#93a8cc')
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title=(f'Average C02 emissions per km from new passenger cars for selected country'),
        width=400,
        height=450
    )    

    line_chart = base.mark_line(stroke='#203864', interpolate='monotone').encode(
        alt.Y('Nr_of_new_EVs').title('Nr of new EVs'),
        tooltip=['Year', 'Nr_of_new_EVs']
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        width=400,
        height=450
    )    
            
    full_chart_00_16 = alt.layer(bar_chart2, line_chart).resolve_scale(
        y='independent'
    )
            
    full_chart_00_16
        
        
    # Chart depicting relationship between emissions and number of new EVs over the years for period 2000-2016
    base2 = alt.Chart(df_17_up).encode(
        alt.X('Year:O').title('Year'))

    bar_chart3 = base2.mark_bar().encode(
        alt.Y('Emissions:Q').title('Emissions'),
        tooltip=['Year', 'Emissions'],
        color=alt.value('#93a8cc')
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title=(f'Average C02 emissions per km from new passenger cars for selected country'),
        width=400,
        height=450
    )    

    line_chart2 = base2.mark_line(stroke='#203864', interpolate='monotone').encode(
        alt.Y('Nr_of_new_EVs').title('Nr of new EVs'),
        tooltip=['Year', 'Nr_of_new_EVs']
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        width=400,
        height=450
    )    
            
    full_chart_17_up = alt.layer(bar_chart3, line_chart2).resolve_scale(
        y='independent'
    )
            
    full_chart_17_up
        
    st.altair_chart(full_chart_17_up)
    st.write("<h1 style='font-size: 25px;'>Interactive graph depicting the relationship between average C02 emissions from new passenger cars and number of new EVs</h1>", unsafe_allow_html=True)
    

    
    
    ########################
    ## Predictive analysis
    #########################

    # Due to time and experience constraints, we did not succeed in fully working out a predictive plot and analysis. 
    # However, we did think about it and tried, which we documented here to show in what direction we were thinking.
    # Additionally, while there are not enough observations such that we have to interpret the results with caution,
    # they do give us some insight in the relationship

    # We will only do this for the years of 2017 and up, as there is too much uncertainty on the missing values for EVs in the years prior to 2017
    # Additionally, in each country there are not enough observations to use train and test sets
    # Therefore, this part is inspiration for future use and analysis

    # Loading necessary libraries
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    # Remove European Union - aggregated instance, as it has no values for Nr of new EVs
    # create a Boolean mask for the rows to remove
    mask = df_17_up['Country'] == 'European Union - 27 countries (from 2020)'

    # select all rows except the ones that contain 'European Union - 27 countries (from 2020)'
    df_17_up = df_17_up[~mask]
    print(df_17_up.isnull().sum(axis = 0))

    # Changing vars to numeric, such that regressions can be done
    df_17_up['Emissions'] = pd.to_numeric(df_17_up['Emissions'])
    df_17_up['Nr_of_new_EVs'] = pd.to_numeric(df_17_up['Nr_of_new_EVs'])
    df_17_up['Year'] = pd.to_numeric(df_17_up['Year'])

    print(df_17_up.head())

    # Normalizing the data of interest
    df_17_up['Emissions_norm'] = df_17_up['Emissions']  / df_17_up['Emissions'].abs().max()
    df_17_up['New_EVs_norm'] = df_17_up['Nr_of_new_EVs']  / df_17_up['Nr_of_new_EVs'].abs().max()
    df_17_up['Year_norm'] = df_17_up['Year']  / df_17_up['Year'].abs().max()


    ## Multilevel model - relationships nested in countries
    # As the data is nested in countries, we  obtain model results from a multilevel model with country as the 
    # grouping variable

    model_ML = smf.mixedlm("Emissions_norm ~ New_EVs_norm", df_17_up, groups=df_17_up["Country"])
    #Fit the model
    result_ML = model_ML.fit()
    #Print model summary
    print(result_ML.summary())
    

