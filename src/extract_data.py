import requests
import json
from pathlib import Path


def extract_weather_data(url:str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        output_path = 'data/weather_data.json'
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)

        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    

