# Importar las librerias y los archivos necesarios
import pandas as pd
from sqlalchemy import create_engine
from config import db_url

# Crear una conexión a la base de datos (en este caso postgreSQL)
engine = create_engine(db_url)

# Definir la consulta SQL
query = "SELECT * FROM weather_data"

# Ejecutar la consulta y obtener los resultados en un DataFrame
df_from_db = pd.read_sql(query, con=engine)

# Mostrar los datos en el DataFrame
print(df_from_db)

# Cerrar la conexión a la base de datos
engine.dispose()