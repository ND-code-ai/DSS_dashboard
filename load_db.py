from sqlalchemy import create_engine, text
import pandas as pd

def load_data_to_db(tables: dict[str, pd.DataFrame]) -> None:
    engine = create_engine("postgresql://student:infomdss@group14_db_dashboard:5432/postgres")
    all_tables = list(tables.keys())

    with engine.connect() as connection:
        result = connection.execute(text(f"DROP TABLE IF EXISTS {','.join(all_tables)} CASCADE;"))
    
    for table_name, table_data in tables.items():
        print(table_name)
        table_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_data_from_db(table_name: str) -> pd.DataFrame:
    engine = create_engine("postgresql://student:infomdss@group14_db_dashboard:5432/postgres")
    
    return pd.read_sql_table(table_name, con=engine, index_col='index')
