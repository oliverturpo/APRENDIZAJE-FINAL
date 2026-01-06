import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")

print("Conectando a PostgreSQL...")

# Crear conexión a la base de datos
engine = create_engine(
    f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}"
)

# Leer todos los datos de la tabla
print("Leyendo datos de la tabla tbl_auto_raw_taller...")
df = pd.read_sql("SELECT * FROM tbl_auto_raw_taller", engine)

# Exportar a CSV
nombre_archivo = "datos_autos_neoauto.csv"
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')

print(f"\n✅ Exportación exitosa!")
print(f"📁 Archivo: {nombre_archivo}")
print(f"📊 Total de registros exportados: {len(df)}")
print(f"📋 Columnas exportadas: {len(df.columns)}")
print(f"\nColumnas: {list(df.columns)}")

# Cerrar conexión
engine.dispose()

print(f"\n✨ Listo! Ahora puedes usar '{nombre_archivo}' para tu dashboard")
