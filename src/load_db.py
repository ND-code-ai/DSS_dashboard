from sqlalchemy import create_engine, text
import pandas as pd

def load_data_to_db(tables: dict[str, pd.DataFrame]) -> None:
    engine = create_engine("postgresql://student:infomdss@postgres:5432/postgres")
    all_table_names = list(tables.keys())
    print('LOADING TABLES!!!!')
    clean_table_names = [table_name.replace(" ", "") for table_name in all_table_names]

   
    new_tables = dict(zip(clean_table_names, tables.values()))

    with engine.connect() as connection:
        result = connection.execute(text(f"DROP TABLE IF EXISTS {','.join(clean_table_names)} CASCADE;"))
    
    for table_name, table_data in new_tables.items():
        print(table_name)
        table_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_data_from_db(table_name: str) -> pd.DataFrame:
    engine = create_engine("postgresql://student:infomdss@postgres:5432/postgres")
    try:
        pd.read_sql_table(table_name, con=engine)
    except:
        return pd.DataFrame()
    
