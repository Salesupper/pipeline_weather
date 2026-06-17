from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
import pandas as pd

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = getenv('user')
password = getenv('password')
database = getenv('database')
host = 'host.docker.internal'
# host = 'localhost'

def get_engine():
    print('conectando com o banco...')
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    print('dados carregados com sucesso!\n')

    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    print(f"total de registros na tabela: {len(df_check)}\n")
