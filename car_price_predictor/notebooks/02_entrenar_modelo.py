"""
Entrenamiento del Modelo de Predicción de Precios
Proyecto: Predicción de Precios de Autos Usados
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuración
load_dotenv()
print("=" * 80)
print("ENTRENAMIENTO DEL MODELO DE PREDICCIÓN DE PRECIOS")
print("=" * 80)

# Conexión a la base de datos
usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}"
)

# Cargar datos
print("\n📊 Cargando datos de PostgreSQL...")
df = pd.read_sql("SELECT * FROM tbl_auto_raw_taller", engine)
engine.dispose()
print(f"✅ Datos cargados: {len(df)} registros")

# Filtrar registros con precio
df_model = df[df['price'].notna()].copy()
print(f"✅ Registros con precio: {len(df_model)}")

# Seleccionar features
print("\n" + "=" * 80)
print("1. PREPARACIÓN DE FEATURES")
print("=" * 80)

features = ['brand', 'year', 'fuel', 'transmission', 'location', 'subcategory']
target = 'price'

# Limpiar datos faltantes en features
print("\nLimpiando datos faltantes...")
for col in features:
    missing = df_model[col].isna().sum()
    if missing > 0:
        print(f"  - {col}: {missing} faltantes -> rellenando con 'Unknown'")
        df_model[col] = df_model[col].fillna('Unknown')

# Preparar dataset
X = df_model[features].copy()
y = df_model[target].copy()

print(f"\n✅ Dataset preparado:")
print(f"   - Features: {features}")
print(f"   - Registros: {len(X)}")
print(f"   - Target: {target}")

# Codificar variables categóricas
print("\n" + "=" * 80)
print("2. CODIFICACIÓN DE VARIABLES CATEGÓRICAS")
print("=" * 80)

# Guardar los encoders para usar en producción
encoders = {}
X_encoded = X.copy()

categorical_features = ['brand', 'fuel', 'transmission', 'location', 'subcategory']

for col in categorical_features:
    print(f"\nCodificando {col}... ({X[col].nunique()} categorías únicas)")
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le
    print(f"  ✅ {col}: {len(le.classes_)} clases")

# 'year' ya es numérico
print(f"\n✅ year: ya numérico (no requiere encoding)")

# Split train/test
print("\n" + "=" * 80)
print("3. DIVISIÓN TRAIN/TEST")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

print(f"✅ Train set: {len(X_train)} registros ({len(X_train)/len(X_encoded)*100:.1f}%)")
print(f"✅ Test set: {len(X_test)} registros ({len(X_test)/len(X_encoded)*100:.1f}%)")

# Entrenar modelo
print("\n" + "=" * 80)
print("4. ENTRENAMIENTO DEL MODELO - RANDOM FOREST")
print("=" * 80)

print("\nEntrenando Random Forest Regressor...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train, y_train)
print("✅ Modelo entrenado exitosamente")

# Evaluar modelo
print("\n" + "=" * 80)
print("5. EVALUACIÓN DEL MODELO")
print("=" * 80)

# Predicciones en train
y_train_pred = model.predict(X_train)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

print("\n📊 Métricas en TRAIN:")
print(f"   - MAE:  ${train_mae:,.2f}")
print(f"   - RMSE: ${train_rmse:,.2f}")
print(f"   - R²:   {train_r2:.4f}")

# Predicciones en test
y_test_pred = model.predict(X_test)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)

print("\n📊 Métricas en TEST:")
print(f"   - MAE:  ${test_mae:,.2f}")
print(f"   - RMSE: ${test_rmse:,.2f}")
print(f"   - R²:   {test_r2:.4f}")

# Importancia de features
print("\n" + "=" * 80)
print("6. IMPORTANCIA DE FEATURES")
print("=" * 80)

feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n" + str(feature_importance))

# Ejemplos de predicción
print("\n" + "=" * 80)
print("7. EJEMPLOS DE PREDICCIÓN")
print("=" * 80)

# Tomar 5 ejemplos del test set
ejemplos = X_test.head(5)
ejemplos_original = X.loc[ejemplos.index].head(5)
predicciones = model.predict(ejemplos)
precios_reales = y_test.head(5)

print("\n")
for i, (idx, ejemplo) in enumerate(ejemplos_original.iterrows()):
    print(f"Ejemplo {i+1}:")
    print(f"  - Marca: {ejemplo['brand']}, Año: {ejemplo['year']}, Combustible: {ejemplo['fuel']}")
    print(f"  - Precio Real: ${precios_reales.iloc[i]:,.0f}")
    print(f"  - Precio Predicho: ${predicciones[i]:,.0f}")
    print(f"  - Diferencia: ${abs(precios_reales.iloc[i] - predicciones[i]):,.0f}")
    print()

# Guardar modelo y encoders
print("=" * 80)
print("8. GUARDANDO MODELO Y ENCODERS")
print("=" * 80)

# Crear directorio si no existe
model_dir = os.path.join(os.path.dirname(__file__), '..', 'apps', 'predictor', 'ml')
os.makedirs(model_dir, exist_ok=True)

# Guardar modelo
model_path = os.path.join(model_dir, 'model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"✅ Modelo guardado en: {model_path}")

# Guardar encoders
encoders_path = os.path.join(model_dir, 'encoders.pkl')
with open(encoders_path, 'wb') as f:
    pickle.dump(encoders, f)
print(f"✅ Encoders guardados en: {encoders_path}")

# Guardar métricas
metrics = {
    'train_mae': train_mae,
    'train_rmse': train_rmse,
    'train_r2': train_r2,
    'test_mae': test_mae,
    'test_rmse': test_rmse,
    'test_r2': test_r2,
    'feature_importance': feature_importance.to_dict()
}

metrics_path = os.path.join(model_dir, 'metrics.pkl')
with open(metrics_path, 'wb') as f:
    pickle.dump(metrics, f)
print(f"✅ Métricas guardadas en: {metrics_path}")

print("\n" + "=" * 80)
print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"""
RESUMEN:
- Modelo: Random Forest Regressor
- Registros entrenamiento: {len(X_train)}
- Registros test: {len(X_test)}
- R² en test: {test_r2:.4f}
- MAE en test: ${test_mae:,.2f}
- Modelo listo para predicciones en producción
""")
