print('esta parte foi apenas para testar se o Pipeline ETL esta funcionando')

# from src.extract_data import extract_weather_data
# from src.transform_data import data_transformation
# from src.load_data import load_weather_data

# from dotenv import load_dotenv
# from pathlib import Path
# from os import getenv

# env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# load_dotenv(env_path)

# API_KEY = getenv('api_key')

# url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'
# table_name = 'sp_weather'

# def pipeline():
#     try:
#         print("ETAPA 1: EXTRACT")
#         extract_weather_data(url)

#         print("ETAPA 2: TRANSFORM")
#         df = data_transformation()

#         print("ETAPA 3: LOAD")
#         load_weather_data(table_name, df)

#         print("\n" + "="*60)
#         print("Pipeline concluído com sucesso!")
#         print("="*60)

#     except Exception as e:
#         print(f'erro na pipeline: {e}')
#         import traceback
#         traceback.print_exc()

# pipeline()