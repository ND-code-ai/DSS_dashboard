# Libraries
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import altair as alt
import requests
from sklearn.linear_model import LinearRegression

def new_values(country_data, start_period, end_period):
        # Filter the data by the time period
        period_data = country_data.loc[start_period:end_period]
        
        # Drop NaNs so we can use the remaining data to train our model
        non_nan = period_data.dropna()
        
        # in case of less than 2 values in the period, we do not fill the missing values, but use 0.0
        if len(non_nan) < 2:
            period_data = period_data.astype(float)
            period_data.fillna(0.0, inplace=True)
            return period_data
        
        # makes a numpy array which is used to prepare the data for the regression model
        x = np.array([year for year in non_nan.index]).reshape(-1, 1)  # years
        y = non_nan.values  #emissions data
        
        '''
        Here we use the linear regression function to predict the emissions for the missing years.
        First we train the model, then we use a loop to predict the missing values that had NaN 
        '''
        model = LinearRegression().fit(x, y)
        missing_years = period_data[period_data.isna()].index
        for year in missing_years:
            predicted_value = model.predict([[year]])
            period_data[year] = round(predicted_value[0], 1)
        
        return period_data

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

    ############################
    # Fill missing values using regression
    ############################

    # define a function to fill NaN values with linear regression
    

    # we apply the function to two periods, because after 2016 there is an different measurement model in the data from eurostats
    Latest_year=df.columns[-1]

    for country in df.index:
        period_2000_2016 = df.loc[country, 2000:2016]
        period_2017_onwards = df.loc[country, 2017:Latest_year]
        
        # Fill NaN values with linear regression
        df.loc[country, 2000:2016] = new_values(period_2000_2016, 2000, 2016)
        df.loc[country, 2017:Latest_year] = new_values(period_2017_onwards, 2017, Latest_year)

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
        # Line plots
    lst = df_em['Country'].unique()
    for ls in lst:
        df_em_a = df_em[df_em['Country'] == ls]
        plt.plot('Year','Emissions',data=df_em_a)
        plt.title(f'Emissions {ls}')
        plt.xticks(rotation=75)
        plt.show()

        # Bar plots
    lst = df_em['Country'].unique()
    for ls in lst:
        df_em_b = df_em[df_em['Country'] == ls]
        plt.bar('Year','Emissions',data=df_em_b)
        plt.title(f'Emissions {ls}')
        plt.xticks(rotation=75)
        plt.show()

    lst = df_em['Country'].unique()
    input_dropdown = alt.binding_select(options=lst, name='Country ')
    selection = alt.selection_point(fields=['Country'], bind=input_dropdown)


    # Trying out a interactive bar chart for just emissions
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
    print(df_EV.head())
    print(df_EV.tail())

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

    print(df_all)
    
    
    
    ###############################################
    ## VERY PROFESSIONAL TRYOUT REMOVING NA'S
    ################################################
    #n = 1     # check previous and next (1) entry
    # rolling window size is (2n + 1)
    #try_out = (df_all['Nr_of_new_EVs'].rolling(n * 2 + 1, min_periods=1, center=True)
    #                                  .mean())
    # Update into a new column `Consumption_New` for demo purpose
    #df_all['Nr_of_new_EVs_New'] = df_all['Nr_of_new_EVs']    
    #df_all.loc[df_all['Nr_of_new_EVs'] == 0, 'Nr_of_new_EVs_New'] = Consumption_mean
    #df_all




    # Cutting the years at 2017, as the metadata states that data is only comparable for 2000 - 2016 and for 2017 - now
        # Subsetting data for years 2000 - 2016
    df_00_16 = df_all[df_all['Year'] <= 2016]
    print(df_00_16.head)

        # Subsetting data for years 2017 - now
    df_17_up = df_all[df_all['Year'] >= 2017]
    print(df_17_up.head)

    ############################
    ## PLOTS PLOTS PLOTS
    ############################

    # Dropdown for price charts
    chart_option = st.selectbox('Choose a Period of Time', [
        '2000 - 2016',
        '2017 and up'
        ])

    if chart_option == '2000 - 2016':
        base = alt.Chart(df_00_16).encode(
            alt.X('Year:O').title('Year'))

        bar_chart2 = base.mark_bar().encode(
            alt.Y('Emissions:Q').title('Emissions'),
            tooltip=['Year', 'Emissions']
        ).add_params(
            selection
        ).transform_filter(
            selection
        ).properties(
            title=(f'Average C02 emissions per km from new passenger cars for selected country'),
            width=400,
            height=450
        )    

        line_chart = base.mark_line(stroke='#57A44C', interpolate='monotone').encode(
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
            
        full_chart = alt.layer(bar_chart2, line_chart).resolve_scale(y='independent')
            
        full_chart
        
        
    if chart_option == '2017 and up':
        base2 = alt.Chart(df_17_up).encode(
            alt.X('Year:O').title('Year'))

        bar_chart3 = base2.mark_bar().encode(
            alt.Y('Emissions:Q').title('Emissions'),
            tooltip=['Year', 'Emissions']
        ).add_params(
            selection
        ).transform_filter(
            selection
        ).properties(
            title=(f'Average C02 emissions per km from new passenger cars for selected country'),
            width=400,
            height=450
        )    

        line_chart2 = base2.mark_line(stroke='#57A44C', interpolate='monotone').encode(
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
            
        full_chart2 = alt.layer(bar_chart3, line_chart2).resolve_scale(y='independent')
            
        full_chart2
        
        st.altair_chart(full_chart, full_chart2)
