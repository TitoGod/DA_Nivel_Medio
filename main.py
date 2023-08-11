# Importar las librerías necesarias para el proyecto.

import requests
import json
from pandas import json_normalize
from datetime import datetime, timedelta
from config import password, url_base

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Lista de ciudades y coordenadas:
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tiflis", "Bogota", "Tokio"]
coordList = ["lat=51.5085&lon=-0.1257", "lat=40.7143&lon=-74.006", "lat=-31.4135&lon=-64.1811", "lat=25.0478&lon=121.5319", "lat=-34.6132&lon=-58.3772", "lat=19.4285&lon=-99.1277", "lat=53.344&lon=-6.2672", "lat=41.6941&lon=44.8337", "lat=4.6097&lon=-74.0817", "lat=35.6895&lon=139.6917"]

api_key = password
url = url_base

datos_climaticos = [] #Lista vacia para ir guardando las "responses"
for i in range(len(cityList)): # recorre la lista de ciudades (10 en total)
    dt = datetime.now() # Fecha actual
    ts = dt.timestamp() # Fecha actual en timestamp pero con decimales
    ts = int(ts) - 432000 # ts transformado en entero y restado 5 dias
    for j in range(5): # Recorre 5 veces cada ciudad
        date = dt.strftime("%Y-%m-%d") # Fecha actual en ese formato para el nombre del archivo
        url = f'{url}{coordList[i]}&dt={ts}&appid={api_key}&units=metric&lang=es'
        response = requests.get(url).json()
        datos_climaticos.append(response)
        with open(f"weather_data2/{cityList[i]}_{date}_weather.json", 'w') as outfile:
            json.dump(response, outfile, indent=4, separators=(',',': '))
        
        ts = ts + 86400 #aca ya tiene un día más
