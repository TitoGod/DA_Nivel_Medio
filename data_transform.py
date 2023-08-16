import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta

# Lee el archivo JSON (Tendria que recorrer los archivos JSON con un for)
ruta_archivo = "weather_data\Bogota_1_2023-08-11_weather.json"

# Utiliza pd.read_json() para leer el json:
df = pd.read_json(ruta_archivo)

#Funcion para transformar los ts en datetime de ARG:
def ts_to_dtArg(ts):
    unix_timestamp = ts
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp)
    gmt3_offset = timedelta(hours=-3)
    argentina_datetime = utc_datetime + gmt3_offset
    return argentina_datetime

# Tomar las claves 'dt', 'sunrise' y 'sunset' del dataframe
dt_value = df['data'][0]['dt']
sunrise_value = df['data'][0]['sunrise']
sunset_value = df['data'][0]['sunset']

# Crear lista con los valores de ts del json:

lista_de_ts = [dt_value, sunrise_value, sunset_value]

# Recorrer esa lista y transformarla en dt_ARG:

lista_de_dt = []
for i in lista_de_ts:
    x = ts_to_dtArg(i)
    lista_de_dt.append(x)

# Recorrer la lista nueva para corroborar:

for j in lista_de_dt:
    print(j)