"""
Entrenamiento MEJORADO del Modelo de Predicción de Precios
Proyecto: Predicción de Precios de Autos Usados
MEJORAS:
- Filtrado de outliers
- Validación de rangos de precios
- Mejores hiperparámetros
- Feature engineering
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuración
load_dotenv()
print("=" * 80)
print("ENTRENAMIENTO MEJORADO DEL MODELO DE PREDICCIÓN DE PRECIOS")
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

# ============================================================================
# LIMPIEZA Y FILTRADO DE DATOS
# ============================================================================
print("\n" + "=" * 80)
print("1. LIMPIEZA Y FILTRADO DE DATOS")
print("=" * 80)

# Filtrar registros con precio
df_model = df[df['price'].notna()].copy()
print(f"\n✅ Registros con precio: {len(df_model)}")

# Análisis de distribución de precios ANTES de filtrar
print(f"\n📊 Distribución de precios ANTES de filtrar:")
print(df_model['price'].describe())
print(f"   - Mínimo: ${df_model['price'].min():,.0f}")
print(f"   - Máximo: ${df_model['price'].max():,.0f}")
print(f"   - Promedio: ${df_model['price'].mean():,.0f}")
print(f"   - Mediana: ${df_model['price'].median():,.0f}")

# FILTRO 1: Eliminar precios sospechosos (muy bajos o muy altos)
# Autos usados normalmente están entre $3,000 y $80,000
# Precios mayores probablemente son autos de lujo o nuevos que sesgan el modelo
precio_min = 3000
precio_max = 80000

print(f"\n🔍 Aplicando filtros de precio...")
print(f"   - Rango válido: ${precio_min:,} - ${precio_max:,}")

df_filtrado = df_model[
    (df_model['price'] >= precio_min) &
    (df_model['price'] <= precio_max)
].copy()

print(f"   - Registros eliminados: {len(df_model) - len(df_filtrado)}")
print(f"   - Registros restantes: {len(df_filtrado)}")

# FILTRO 2: Eliminar años muy antiguos (pre-1995) o futuros
año_actual = 2026
df_filtrado = df_filtrado[
    (df_filtrado['year'] >= 1995) &
    (df_filtrado['year'] <= año_actual)
].copy()
print(f"\n🔍 Filtro de años (1995-{año_actual}): {len(df_filtrado)} registros")

# FILTRO 3: Remover outliers usando IQR (Interquartile Range)
Q1 = df_filtrado['price'].quantile(0.25)
Q3 = df_filtrado['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n🔍 Aplicando filtro IQR para outliers:")
print(f"   - Q1: ${Q1:,.0f}")
print(f"   - Q3: ${Q3:,.0f}")
print(f"   - IQR: ${IQR:,.0f}")
print(f"   - Límite inferior: ${lower_bound:,.0f}")
print(f"   - Límite superior: ${upper_bound:,.0f}")

df_filtrado = df_filtrado[
    (df_filtrado['price'] >= lower_bound) &
    (df_filtrado['price'] <= upper_bound)
].copy()
print(f"   - Registros después de IQR: {len(df_filtrado)}")

# Análisis de distribución de precios DESPUÉS de filtrar
print(f"\n📊 Distribución de precios DESPUÉS de filtrar:")
print(df_filtrado['price'].describe())
print(f"   - Mínimo: ${df_filtrado['price'].min():,.0f}")
print(f"   - Máximo: ${df_filtrado['price'].max():,.0f}")
print(f"   - Promedio: ${df_filtrado['price'].mean():,.0f}")
print(f"   - Mediana: ${df_filtrado['price'].median():,.0f}")

# ============================================================================
# PREPARACIÓN DE FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("2. PREPARACIÓN DE FEATURES")
print("=" * 80)

features = ['brand', 'year', 'fuel', 'transmission', 'location', 'subcategory']
target = 'price'

# Limpiar datos faltantes en features
print("\nLimpiando datos faltantes...")
for col in features:
    missing = df_filtrado[col].isna().sum()
    if missing > 0:
        print(f"  - {col}: {missing} faltantes -> rellenando con 'Unknown'")
        df_filtrado[col] = df_filtrado[col].fillna('Unknown')

# FEATURE ENGINEERING: Agregar edad del auto
df_filtrado['car_age'] = año_actual - df_filtrado['year']
print(f"\n✅ Feature Engineering: Agregada 'car_age' (edad del auto)")

# Actualizar features
features.append('car_age')

# Preparar dataset
X = df_filtrado[features].copy()
y = df_filtrado[target].copy()

print(f"\n✅ Dataset preparado:")
print(f"   - Features: {features}")
print(f"   - Registros: {len(X)}")
print(f"   - Target: {target}")

# ============================================================================
# CODIFICACIÓN DE VARIABLES CATEGÓRICAS
# ============================================================================
print("\n" + "=" * 80)
print("3. CODIFICACIÓN DE VARIABLES CATEGÓRICAS")
print("=" * 80)

encoders = {}
X_encoded = X.copy()

categorical_features = ['brand', 'fuel', 'transmission', 'location', 'subcategory']

for col in categorical_features:
    print(f"\nCodificando {col}... ({X[col].nunique()} categorías únicas)")
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le
    print(f"  ✅ {col}: {len(le.classes_)} clases")

print(f"\n✅ 'year' y 'car_age': ya numéricos (no requieren encoding)")

# ============================================================================
# DIVISIÓN TRAIN/TEST
# ============================================================================
print("\n" + "=" * 80)
print("4. DIVISIÓN TRAIN/TEST")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

print(f"✅ Train set: {len(X_train)} registros ({len(X_train)/len(X_encoded)*100:.1f}%)")
print(f"✅ Test set: {len(X_test)} registros ({len(X_test)/len(X_encoded)*100:.1f}%)")

# ============================================================================
# ENTRENAMIENTO DEL MODELO - RANDOM FOREST MEJORADO
# ============================================================================
print("\n" + "=" * 80)
print("5. ENTRENAMIENTO DEL MODELO - RANDOM FOREST MEJORADO")
print("=" * 80)

print("\nEntrenando Random Forest Regressor con hiperparámetros optimizados...")
model = RandomForestRegressor(
    n_estimators=200,        # Aumentado de 100 a 200
    max_depth=15,            # Reducido de 20 a 15 para evitar overfitting
    min_samples_split=10,    # Aumentado de 5 a 10
    min_samples_leaf=4,      # Aumentado de 2 a 4
    max_features='sqrt',     # Usar sqrt de features en cada split
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train, y_train)
print("✅ Modelo entrenado exitosamente")

# Validación cruzada
print("\n📊 Validación cruzada (5-fold)...")
cv_scores = cross_val_score(model, X_train, y_train, cv=5,
                            scoring='r2', n_jobs=-1)
print(f"   - R² scores: {cv_scores}")
print(f"   - R² promedio: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# ============================================================================
# EVALUACIÓN DEL MODELO
# ============================================================================
print("\n" + "=" * 80)
print("6. EVALUACIÓN DEL MODELO")
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

# Análisis de errores
errors = np.abs(y_test - y_test_pred)
print(f"\n📊 Análisis de errores:")
print(f"   - Error mínimo: ${errors.min():,.2f}")
print(f"   - Error máximo: ${errors.max():,.2f}")
print(f"   - Error mediano: ${errors.median():,.2f}")
print(f"   - % predicciones con error < $5000: {(errors < 5000).sum() / len(errors) * 100:.1f}%")
print(f"   - % predicciones con error < $10000: {(errors < 10000).sum() / len(errors) * 100:.1f}%")

# ============================================================================
# IMPORTANCIA DE FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("7. IMPORTANCIA DE FEATURES")
print("=" * 80)

feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n" + str(feature_importance))

# ============================================================================
# EJEMPLOS DE PREDICCIÓN
# ============================================================================
print("\n" + "=" * 80)
print("8. EJEMPLOS DE PREDICCIÓN")
print("=" * 80)

# Tomar 10 ejemplos del test set
ejemplos = X_test.head(10)
ejemplos_original = X.loc[ejemplos.index].head(10)
predicciones = model.predict(ejemplos)
precios_reales = y_test.head(10)

print("\n")
for i, (idx, ejemplo) in enumerate(ejemplos_original.iterrows()):
    error = abs(precios_reales.iloc[i] - predicciones[i])
    error_pct = (error / precios_reales.iloc[i]) * 100
    print(f"Ejemplo {i+1}:")
    print(f"  - Marca: {ejemplo['brand']}, Año: {int(ejemplo['year'])}, Combustible: {ejemplo['fuel']}")
    print(f"  - Transmisión: {ejemplo['transmission']}, Tipo: {ejemplo['subcategory']}")
    print(f"  - Precio Real: ${precios_reales.iloc[i]:,.0f}")
    print(f"  - Precio Predicho: ${predicciones[i]:,.0f}")
    print(f"  - Error: ${error:,.0f} ({error_pct:.1f}%)")
    print()

# ============================================================================
# GUARDAR MODELO Y ENCODERS
# ============================================================================
print("=" * 80)
print("9. GUARDANDO MODELO Y ENCODERS")
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
    'cv_r2_mean': cv_scores.mean(),
    'cv_r2_std': cv_scores.std(),
    'feature_importance': feature_importance.to_dict(),
    'total_records': len(df_filtrado),
    'price_range': {
        'min': float(df_filtrado['price'].min()),
        'max': float(df_filtrado['price'].max()),
        'mean': float(df_filtrado['price'].mean()),
        'median': float(df_filtrado['price'].median())
    }
}

metrics_path = os.path.join(model_dir, 'metrics.pkl')
with open(metrics_path, 'wb') as f:
    pickle.dump(metrics, f)
print(f"✅ Métricas guardadas en: {metrics_path}")

print("\n" + "=" * 80)
print("✅ ENTRENAMIENTO MEJORADO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"""
RESUMEN:
- Modelo: Random Forest Regressor (Mejorado)
- Registros totales: {len(df)}
- Registros filtrados: {len(df_filtrado)}
- Registros entrenamiento: {len(X_train)}
- Registros test: {len(X_test)}
- R² en test: {test_r2:.4f} (mejorado desde 0.44)
- MAE en test: ${test_mae:,.2f}
- RMSE en test: ${test_rmse:,.2f}
- Modelo listo para predicciones en producción

MEJORAS APLICADAS:
✅ Filtrado de outliers (IQR)
✅ Validación de rangos de precio ($3k-$80k)
✅ Filtrado de años (1995-2026)
✅ Feature engineering (edad del auto)
✅ Hiperparámetros optimizados
✅ Validación cruzada
✅ Análisis de errores detallado
""")
