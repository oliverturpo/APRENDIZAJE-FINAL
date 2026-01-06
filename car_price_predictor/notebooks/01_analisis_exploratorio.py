"""
Análisis Exploratorio de Datos (EDA)
Proyecto: Predicción de Precios de Autos Usados
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Configuración
load_dotenv()

# Conexión a la base de datos
usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}"
)

print("=" * 80)
print("ANÁLISIS EXPLORATORIO DE DATOS - AUTOS USADOS")
print("=" * 80)

# Cargar datos
print("\n📊 Cargando datos de PostgreSQL...")
df = pd.read_sql("SELECT * FROM tbl_auto_raw_taller", engine)
engine.dispose()

print(f"✅ Datos cargados: {len(df)} registros")

# Información general
print("\n" + "=" * 80)
print("1. INFORMACIÓN GENERAL DEL DATASET")
print("=" * 80)
print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"\nColumnas: {list(df.columns)}")
print(f"\nTipos de datos:")
print(df.dtypes)

# Datos faltantes
print("\n" + "=" * 80)
print("2. DATOS FALTANTES")
print("=" * 80)
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Columna': missing.index,
    'Faltantes': missing.values,
    'Porcentaje': missing_pct.values
})
print(missing_df[missing_df['Faltantes'] > 0])

# Estadísticas de la variable objetivo (precio)
print("\n" + "=" * 80)
print("3. ANÁLISIS DE LA VARIABLE OBJETIVO: PRECIO")
print("=" * 80)
df_con_precio = df[df['price'].notna()]
print(f"\nRegistros con precio: {len(df_con_precio)} de {len(df)}")
print(f"Registros sin precio: {df['price'].isna().sum()}")
print(f"\nEstadísticas del precio:")
print(df_con_precio['price'].describe())

# Distribución por marca
print("\n" + "=" * 80)
print("4. DISTRIBUCIÓN POR MARCA (Top 15)")
print("=" * 80)
marcas = df['brand'].value_counts().head(15)
print(marcas)

# Distribución por año
print("\n" + "=" * 80)
print("5. DISTRIBUCIÓN POR AÑO")
print("=" * 80)
anios = df['year'].value_counts().sort_index(ascending=False).head(10)
print(anios)

# Distribución por combustible
print("\n" + "=" * 80)
print("6. DISTRIBUCIÓN POR TIPO DE COMBUSTIBLE")
print("=" * 80)
combustibles = df['fuel'].value_counts()
print(combustibles)

# Distribución por transmisión
print("\n" + "=" * 80)
print("7. DISTRIBUCIÓN POR TRANSMISIÓN")
print("=" * 80)
transmisiones = df['transmission'].value_counts()
print(transmisiones)

# Distribución por ubicación
print("\n" + "=" * 80)
print("8. DISTRIBUCIÓN POR UBICACIÓN (Top 10)")
print("=" * 80)
ubicaciones = df['location'].value_counts().head(10)
print(ubicaciones)

# Análisis de precios por marca (Top 10)
print("\n" + "=" * 80)
print("9. PRECIO PROMEDIO POR MARCA (Top 10 marcas más caras)")
print("=" * 80)
precio_marca = df_con_precio.groupby('brand')['price'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False).head(10)
print(precio_marca)

# Análisis de precios por año
print("\n" + "=" * 80)
print("10. PRECIO PROMEDIO POR AÑO")
print("=" * 80)
precio_anio = df_con_precio.groupby('year')['price'].mean().sort_index(ascending=False).head(10)
print(precio_anio)

# Correlación numérica
print("\n" + "=" * 80)
print("11. CORRELACIÓN CON EL PRECIO")
print("=" * 80)
numeric_cols = ['year', 'price']
corr = df_con_precio[numeric_cols].corr()
print(corr)

# Resumen para el modelo
print("\n" + "=" * 80)
print("12. RESUMEN PARA EL MODELO DE ML")
print("=" * 80)
print(f"""
Features disponibles para el modelo:
- brand: {df['brand'].nunique()} categorías únicas
- year: Rango {df['year'].min()} - {df['year'].max()}
- fuel: {df['fuel'].nunique()} tipos
- transmission: {df['transmission'].nunique()} tipos
- location: {df['location'].nunique()} ubicaciones
- subcategory: {df['subcategory'].nunique()} subcategorías

Variable objetivo:
- price: {len(df_con_precio)} registros válidos ({len(df_con_precio)/len(df)*100:.1f}%)
- Rango: ${df_con_precio['price'].min():,.0f} - ${df_con_precio['price'].max():,.0f}
- Promedio: ${df_con_precio['price'].mean():,.0f}
- Mediana: ${df_con_precio['price'].median():,.0f}
""")

print("\n" + "=" * 80)
print("✅ ANÁLISIS EXPLORATORIO COMPLETADO")
print("=" * 80)
