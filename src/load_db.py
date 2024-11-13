from sqlalchemy import create_engine, text
import pandas as pd
import group14_preparedata as prep
import pickle as pkl

def load_data_to_db(tables: dict[str, pd.DataFrame]) -> None:
    """
    Load data into the PostgreSQL database.

    Parameters:
    tables (dict[str, pd.DataFrame]): Dictionary where keys are table names and values are DataFrames containing the data.
    """
    engine = create_engine("postgresql://student:infomdss@postgres:5432/postgres")
    all_table_names = list(tables.keys())

    clean_table_names = [table_name.replace(" ", "") for table_name in all_table_names]

    new_tables = dict(zip(clean_table_names, tables.values()))

    for table_name, table_data in new_tables.items():
        table_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_data_from_db(table_name: str) -> pd.DataFrame:
    """
    Load data from the PostgreSQL database.

    Parameters:
    table_name (str): Name of the table to load data from.

    Returns:
    pd.DataFrame: DataFrame containing the data from the specified table.
    """
    engine = create_engine("postgresql://student:infomdss@postgres:5432/postgres")
    if table_name == "EVsales":
        return pd.read_sql_table(table_name, con=engine, index_col="index")
    return pd.read_sql_table(table_name, con=engine)

def get_all_data(table_names: list[str]) -> dict[str, pd.DataFrame]:
    """
    Get all data from the specified tables in the PostgreSQL database.

    Parameters:
    table_names (list[str]): List of table names to fetch data from.

    Returns:
    dict[str, pd.DataFrame]: Dictionary where keys are table names and values are DataFrames containing the data.
    """
    all_tables = {}

    for table_name in table_names:
        all_tables[table_name] = load_data_from_db(table_name)

    return all_tables

def main():
    """
    Main function to preprocess data, load it into the database, and export it to a pickle file.
    """
    all_data = prep.main()
    load_data_to_db(all_data)

    table_names = [table_name.replace(" ", "") for table_name in list(all_data.keys())]
    fetched_data = get_all_data(table_names)

    pkl.dump(fetched_data, open("data/temp_export.pkl", "wb"))

if __name__ == "__main__":
    main()
