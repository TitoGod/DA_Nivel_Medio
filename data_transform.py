import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta

# Lee el archivo JSON (Tendria que recorrer los archivos JSON con un for)
ruta_archivo = "weather_data\Bogota_1_2023-08-11_weather.json"

# Utiliza pd.read_json() para leer el json:
df = pd.read_json(ruta_archivo)
print(df)

# Tomar las claves 'dt', 'sunrise' y 'sunset' del dataframe
dt_value = df['data'][0]['dt']
sunrise_value = df['data'][0]['sunrise']
sunset_value = df['data'][0]['sunset']

# Crear un DataFrame con los datos
data_dts = {'dt': [dt_value], 'sunrise': [sunrise_value], 'sunset': [sunset_value]}
df_dts = pd.DataFrame(data_dts)
print(df_dts)

# Acá mostramos como con lambda x podemos extraer esas 3 columnas y cambiarlas al formato de datetime.
datecols = ['dt', 'sunrise', 'sunset']
df_dts[datecols] = df_dts[datecols].apply(lambda x: pd.to_datetime(x, unit='s'))
print(df_dts)