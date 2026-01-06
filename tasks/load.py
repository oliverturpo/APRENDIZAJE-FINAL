import pandas as pd
import os

from prefect import task
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
# Datos conexión
usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")



@task
def load(data_df):

    resultado = 0
    # conexion a bd
    # Motor SQLAlchemy
    engine = create_engine(
        f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}"
    )

    columnas = ['codigo','titulo','link','etiqueta','imagen','combustible','ubicacion','precio','marca','anio','anunciante','categoria','subcategoria','transmision','combustible','tag','slug']
    # Crear un DataFrame de pandas
    df = data_df.copy()
    print("DataFrame creado")
    print(df.head())
    #agregar columna de fecha de carga
    df['fecha'] = pd.Timestamp.now()
    # Cargar el DataFrame en la tabla de la base de datos
    df.to_sql('tbl_auto_raw_taller', engine, if_exists='replace', index=False)
    print("Datos cargados correctamente en la base de datos.")
    resultado = len(df)

    #cerrar la conexión
    engine.dispose()    
    
    return resultado
    