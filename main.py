# Importar las librerías necesarias para el proyecto.

import requests
from pandas import json_normalize
from datetime import datetime, timedelta
from config import password, url_base

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Lista de ciudades y coordenadas:
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tiflis", "Bogota", "Tokio"]
coordList = ["lat=51.5085&lon=-0.1257", "lat=40.7143&lon=-74.006", "lat=-31.4135&lon=-64.1811", "lat=25.0478&lon=121.5319", "lat=-34.6132&lon=-58.3772", "lat=19.4285&lon=-99.1277", "lat=53.344&lon=-6.2672", "lat=41.6941&lon=44.8337", "lat=4.6097&lon=-74.0817", "lat=35.6895&lon=139.6917"]

# Función para traer los datos:
def get_weather_data(city, coords):
    """Esta función busca los datos de las ciudades y 
    coordenadas que se le pasa por parámetro y los guarda
    en un archivo con formato csv"""
    
    # Endpoint de OpenWeatherMap:
    BASE_URL = url_base
    api_key = password

    # La URL completa con las coordenadas:
    url = f"{BASE_URL}{coords}&appid={api_key}&units=metric"

    # Realizar la una solicitud HTTP a la API:
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa:
    if response.status_code == 200:
        data = response.json()
        # Convertir los datos JSON a un DataFrame de pandas:
        df = json_normalize(data)
    
    else:
        print(f"No se pudieron obtener los datos del clima de {city}")

    # Obtener la fecha actual para utilizarla en el nombre del archivo CSV:
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Definir la ruta y nombre del archivo CSV donde se almacenarán los datos:
    file_path = f"weather_data/{city.lower()}_{current_date}.csv".replace(" ", "_")

    # Guardas los datos en formato CSV:
    with open(file_path, 'w') as output_file:
        df.to_csv(output_file, index=False)


# Ejecución:

if __name__ == "__main__":
    for city, coords in zip(cityList, coordList):
        get_weather_data(city, coords)