# Importar las librerías necesarias para el proyecto.

import requests
import pandas as pd
from config import password
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



