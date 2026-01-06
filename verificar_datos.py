import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}"
)

# Verificar datos
df = pd.read_sql("SELECT * FROM tbl_auto_raw_taller LIMIT 10", engine)

print(f"✅ Total de registros en la tabla: {pd.read_sql('SELECT COUNT(*) as total FROM tbl_auto_raw_taller', engine)['total'][0]}")
print(f"\n📋 Columnas: {list(df.columns)}")
print(f"\n🔍 Primeros 10 registros:\n")
print(df.head(10))

engine.dispose()
