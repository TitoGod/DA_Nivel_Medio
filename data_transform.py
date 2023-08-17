# Importar las librerías

import pandas as pd
from sqlalchemy import create_engine

# Función que transforma los datos y los guarda en un DataFrame

def transform(ruta_archivo_json):

    # Ruta del archivo JSON para transformarlo
    ruta_archivo = ruta_archivo_json

    # Utiliza pd.read_json() para leer el json:
    df1 = pd.read_json(ruta_archivo)

    # Tomar las claves 'dt', 'sunrise' y 'sunset' del dataframe
    dt_value = df1['data'][0]['dt']
    sunrise_value = df1['data'][0]['sunrise']
    sunset_value = df1['data'][0]['sunset']

    # Crear un DataFrame con los datos para transformarlos
    data_dts = {'Fecha': [dt_value], 'Amanecer': [sunrise_value], 'Atardecer': [sunset_value]}
    df2 = pd.DataFrame(data_dts)

    # Con lambda x podemos extraer esas 3 columnas y cambiarlas al formato de datetime
    datecols = ['Fecha', 'Amanecer', 'Atardecer']
    df2[datecols] = df2[datecols].apply(lambda x: pd.to_datetime(x, unit='s'))

    # Primero poner en variables los valores a agregar al DataFrame final, en este caso estos datos
    temp = df1['data'][0]['temp']
    pressure = df1['data'][0]['pressure']
    feels_like = df1['data'][0]['pressure']
    humidity = df1['data'][0]['pressure']
    visibility = df1['data'][0]['pressure']
    wind_speed = df1['data'][0]['pressure']
    main = df1['data'][0]['weather'][0]['main']
    description = df1['data'][0]['weather'][0]['description']
    
    # Agregar varias columnas al mismo tiempo
    new_columns = {
        'Temperatura': [temp],
        'Presion': [pressure],
        'Sensacion_termica': [feels_like],
        'Humedad': [humidity],
        'Visibilidad': [visibility],
        'Velocidad_viento': [wind_speed],
        'Principal': [main],
        'Descripcion': [description]
    }

    # Finalmente agrego los datos al DataFrame final
    df3 = df2.assign(**new_columns)

    return df3