import pandas as pd
import pickle as pkl
import data_utils.scrape_data as scrape
import data_utils.preprocess as preprocess

def main() -> dict[str, pd.DataFrame]:
    all_dataframes = {}
    
    sales_data = scrape.scrape_sales_data()
    cleaned_sales_data = preprocess.preprocess_EV_sales(sales_data)
    all_dataframes['EV sales'] = cleaned_sales_data

    emissions_data = pd.read_csv("data/reduced_energyc1.csv")
    cleaned_emissions_data = preprocess.preprocess_emissions_data(emissions_data)
    all_dataframes["Fossil fuel emissions by cars"] = cleaned_emissions_data

    noc_data = pd.read_csv('data/scraped_NoC_data.csv', header=1)
    cleaned_noc_data = preprocess.preprocess_EV_infrastructure(noc_data)
    all_dataframes['EV infrastructure'] = cleaned_noc_data

    # placeholder df (see readme)
    all_dataframes['EV Emissions and sales'] = pd.DataFrame()

    ev_prices = pd.read_csv('data/EV_cars.csv')
    ev_prices_processed = preprocess.preprocess_EV_prices(ev_prices)
    all_dataframes['EV prices'] = ev_prices_processed

    pkl.dump(all_dataframes, open("data/temp_export.pkl", "wb"))

    return all_dataframes


   
