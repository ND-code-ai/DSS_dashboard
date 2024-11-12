from sqlalchemy import create_engine, text
import pandas as pd

def load_data_to_db(conn, tables: dict[str, pd.DataFrame]) -> None:
    for table_name, table_data in tables.items():
        print(table_name)
        print(table_data.head())
        table_data.to_sql(table_name, con=conn, if_exists='replace', index=False)

def load_data_from_db(conn, table_name: str) -> pd.DataFrame:
    return pd.read_sql_table(table_name, con=conn, index_col='index')
