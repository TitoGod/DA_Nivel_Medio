# Importar las librerías necesarias.
import time
from functions import get_weatherdata, listar_rutas, transform, create_table, agregar_datos

# Lista de ciudades y coordenadas:
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tiflis", "Bogota", "Tokio"]
coordList = ["lat=51.5085&lon=-0.1257", "lat=40.7143&lon=-74.006", "lat=-31.4135&lon=-64.1811", "lat=25.0478&lon=121.5319", "lat=-34.6132&lon=-58.3772", "lat=19.4285&lon=-99.1277", "lat=53.344&lon=-6.2672", "lat=41.6941&lon=44.8337", "lat=4.6097&lon=-74.0817", "lat=35.6895&lon=139.6917"]


# Ejecución
if __name__ == "__main__":
    # 1: Traer todos los datos de la API
    get_weatherdata(cityList, coordList)
    time.sleep(5)

    # 2: Listar las rutas de los archivos JSON para sacar los datos
    lista_de_rutas = listar_rutas('weather_data_')
    time.sleep(2)

    # 3: Transformar todos esos datos y dejarlos en una lista que contenga todos los DataFrame
    lista_de_dfs = []
    for ruta in lista_de_rutas:
        dfs = transform(ruta)
        lista_de_dfs.append(dfs)
    time.sleep(2)

    # 3: Crear la estructura de la tabla en la base de datos
    create_table()
    time.sleep(2)

    # 4: Agregar todos los datos de los DataFrame a la base de datos
    agregar_datos(lista_de_dfs)