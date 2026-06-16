import json
import pandas as pd
from pathlib import Path

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'

columns_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_to_normalize_datetime = ['datetime','sunrise','sunset']
columns_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }


def create_dataframe(path_name:str) -> pd.DataFrame:
    print('criando DataFrame do arquivo JSON...')
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f'Arquivo não encontrado: {path}')
    
    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    print(f'\nDataFrame criado com {len(df)} linha(s)')
    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    print(f"\n coluna 'df_weather' normalizada - {len(df.columns)} colunas")
    return df

def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    print(f'\nRemovendo colunas: {columns_names}')
    df = df.drop(columns=columns_names)
    print(f'\nColunas removidas - {len(df.columns)} colunas restantes')
    return df

def rename_columns(df: pd.DataFrame, columns_names:dict[str,str]) -> pd.DataFrame:
    print(f'\nRenomeando {len(columns_names)} colunas...')
    df = df.rename(columns=columns_names)
    print('\nColunas renomeadas')
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    print(f"\n Convertendo colunas para datetime: {columns_names}")
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
    print(f"\nColunas covertidas para datetime")
    return df

def data_transformation():
    print("\n Iniciando transformações")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df,columns_to_drop)
    df = rename_columns(df,columns_to_rename)
    df = normalize_datetime_columns(df,columns_to_normalize_datetime)
    print("\n Transformações concluídas")
    return df