# Importar las librerías

import os
import pandas as pd
from sqlalchemy import create_engine
import requests
import json
from datetime import datetime
from config import api_key, url_base, db_url

# Función para traer todos los datos:
def get_weatherdata(cityList, coordList):
    """
    Esta funcion trae los datos de 5 dias atras de cada ciudad que se le pase
    """
    datos_climaticos = [] #Lista vacia para ir guardando las "responses"
    for i in range(len(cityList)): # recorre la lista de ciudades (10 en total)
        dt = datetime.now() # Fecha actual
        ts = dt.timestamp() # Fecha actual en timestamp pero con decimales
        ts = int(ts) - 432000 # ts transformado en entero y restado 5 dias
        for j in range(5): # Recorre 5 veces cada ciudad
            date = dt.strftime("%Y-%m-%d") # Fecha actual en ese formato para el nombre del archivo
            url = f'{url_base}{coordList[i]}&dt={ts}&appid={api_key}&units=metric&lang=es'

            # Realizar la solicitud de los datos a la API
            response = requests.get(url).json()
            datos_climaticos.append(response)
            ts = ts + 86400 #aca ya tiene un día más

            # Definir la ruta y nombre del archivo .json
            with open(f"weather_data_/{cityList[i]}_{j+1}_{date}_weather.json", 'w') as outfile:
                json.dump(response, outfile, indent=4, separators=(',',': '))

# Funcion para listar las rutas de los archivos JSON que contienen los datos
def listar_rutas(directorio):
    
    # Obtener una lista de nombres de archivos y directorios en el directorio pasado por parametro
    lista_de_nombres = os.listdir(directorio)

    # Iterar sobre los elementos y agregar la ruta completa
    lista_de_rutas = []
    for elemento in lista_de_nombres:
        ruta_completa = os.path.join(directorio, elemento)
        lista_de_rutas.append(ruta_completa)

    return lista_de_rutas

# Función que transforma los datos y los guarda en un DataFrame
def transform(ruta_archivo):

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

    # Le agrego el nombre de la ciudad que no trae en los datos
    nombre_ciudad = ruta_archivo.split('_')[2]
    # Le elimino la "\" del nombre
    cadena_original = nombre_ciudad
    ciudad = cadena_original.replace("\\", "")
    
    # Le agrego al DataFrame en la posicion 0, o sea al inicio
    df3.insert(0, 'Ciudad', [ciudad])

    # Retorna el DataFrame totalmente transformado y listo para cargar a la base de datos
    return df3

# Funcion para agregar los datos a partir de una lista de DataFrames ya transformados a la base de datos
def agregar_datos(lista_dfs):

    engine = create_engine(db_url)
    for x in lista_dfs:
        x.to_sql(name='weather_data', con=engine, if_exists='append', index=False)
    engine.dispose()

# Funcion para crear la estructura de la tabla en la base de datos
def create_table():
    # Crear un DataFrame vacío
    empty_df = pd.DataFrame(columns=['Ciudad', 'Fecha', 'Amanecer', 'Atardecer', 'Temperatura', 'Presion', 'Sensacion_termica', 'Humedad', 'Visibilidad', 'Velocidad_viento', 'Principal', 'Descripcion'])

    # Conectar a la base de datos postgreSQL
    engine = create_engine(db_url)

    # Volcar el DataFrame vacío en una tabla existente llamada "personas"
    empty_df.to_sql(name='weather_data', con=engine, if_exists='replace', index=False)

    # Cerrar la conexión a la base de datos
    engine.dispose()
