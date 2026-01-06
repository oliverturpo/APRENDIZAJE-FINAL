"""
MODELO DEFINITIVO - PREDICCIÓN DE PRECIOS DE AUTOS
- Filtrado inteligente de outliers
- Hyperparameter tuning automático
- Validación exhaustiva
- Modelo 100% optimizado
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

print("="*80)
print("MODELO DEFINITIVO - PREDICCIÓN DE PRECIOS DE AUTOS")
print("="*80)

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================
usuario = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{base_datos}")

print("\n📊 Cargando datos de PostgreSQL...")
df = pd.read_sql("SELECT * FROM tbl_auto_raw_taller", engine)
engine.dispose()
print(f"✅ {len(df)} registros cargados")

# ============================================================================
# 2. LIMPIEZA Y FILTRADO AGRESIVO
# ============================================================================
print("\n" + "="*80)
print("LIMPIEZA DE DATOS")
print("="*80)

# Solo registros con precio
df = df[df['price'].notna()].copy()
print(f"\n✅ Con precio: {len(df)}")

# Filtro de precios razonables (autos usados peruanos)
df = df[(df['price'] >= 3000) & (df['price'] <= 100000)].copy()
print(f"✅ Rango $3k-$100k: {len(df)}")

# Filtro de años
año_actual = 2026
df = df[(df['year'] >= 1995) & (df['year'] <= año_actual)].copy()
print(f"✅ Años 1995-{año_actual}: {len(df)}")

# Eliminar outliers por IQR
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['price'] >= Q1 - 1.5*IQR) & (df['price'] <= Q3 + 1.5*IQR)].copy()
print(f"✅ Sin outliers IQR: {len(df)}")

# Eliminar marcas/categorías con pocos datos (< 5 registros)
for col in ['brand', 'fuel', 'transmission', 'subcategory', 'location']:
    counts = df[col].value_counts()
    valid_values = counts[counts >= 5].index
    df = df[df[col].isin(valid_values)].copy()

print(f"✅ Sin categorías raras: {len(df)}")

if len(df) < 100:
    print(f"\n❌ ERROR: Solo quedan {len(df)} registros. Necesitas más datos limpios.")
    exit(1)

print(f"\n📊 Distribución final de precios:")
print(f"   Min: ${df['price'].min():,.0f}")
print(f"   Max: ${df['price'].max():,.0f}")
print(f"   Media: ${df['price'].mean():,.0f}")
print(f"   Mediana: ${df['price'].median():,.0f}")

# ============================================================================
# 3. FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("FEATURE ENGINEERING")
print("="*80)

# Edad del auto
df['car_age'] = año_actual - df['year']

# Precio por año (depreciación)
df['price_per_year'] = df['price'] / (df['year'] - 1990 + 1)

# Categoría de precio
df['price_category'] = pd.cut(df['price'],
                               bins=[0, 10000, 20000, 35000, 100000],
                               labels=['economico', 'medio', 'alto', 'premium'])

print(f"✅ Features creados: car_age, price_per_year, price_category")

# ============================================================================
# 4. PREPARAR DATOS
# ============================================================================
features = ['brand', 'year', 'fuel', 'transmission', 'location', 'subcategory',
            'car_age', 'price_per_year', 'price_category']

# Rellenar missing
for col in features:
    if df[col].isna().sum() > 0:
        df[col] = df[col].fillna('Unknown')

X = df[features].copy()
y = df['price'].copy()

print(f"\n✅ Dataset: {len(X)} registros x {len(features)} features")

# ============================================================================
# 5. ENCODING
# ============================================================================
print("\n" + "="*80)
print("ENCODING")
print("="*80)

encoders = {}
X_encoded = X.copy()

categorical = ['brand', 'fuel', 'transmission', 'location', 'subcategory', 'price_category']

for col in categorical:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le
    print(f"✅ {col}: {len(le.classes_)} clases")

# ============================================================================
# 6. SPLIT
# ============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

print(f"\n✅ Train: {len(X_train)} | Test: {len(X_test)}")

# ============================================================================
# 7. HYPERPARAMETER TUNING con GridSearchCV
# ============================================================================
print("\n" + "="*80)
print("OPTIMIZACIÓN DE HIPERPARÁMETROS (esto toma tiempo...)")
print("="*80)

param_grid = {
    'n_estimators': [150, 200, 250],
    'max_depth': [12, 15, 18],
    'min_samples_split': [8, 10, 12],
    'min_samples_leaf': [3, 4, 5],
    'max_features': ['sqrt', 'log2']
}

print(f"\n🔍 Probando {3*3*3*3*2} = 162 combinaciones...")
print("   (Esto puede tomar 5-10 minutos)")

rf = RandomForestRegressor(random_state=42, n_jobs=-1)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"\n✅ Mejores parámetros encontrados:")
for param, value in grid_search.best_params_.items():
    print(f"   - {param}: {value}")

best_model = grid_search.best_estimator_

# ============================================================================
# 8. EVALUACIÓN
# ============================================================================
print("\n" + "="*80)
print("EVALUACIÓN DEL MODELO OPTIMIZADO")
print("="*80)

# Train
y_train_pred = best_model.predict(X_train)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

print(f"\n📊 TRAIN:")
print(f"   MAE:  ${train_mae:,.2f}")
print(f"   RMSE: ${train_rmse:,.2f}")
print(f"   R²:   {train_r2:.4f}")

# Test
y_test_pred = best_model.predict(X_test)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)

print(f"\n📊 TEST:")
print(f"   MAE:  ${test_mae:,.2f}")
print(f"   RMSE: ${test_rmse:,.2f}")
print(f"   R²:   {test_r2:.4f}")

# Cross-validation
cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='r2')
print(f"\n📊 CROSS-VALIDATION (5-fold):")
print(f"   R² promedio: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Análisis de errores
errors = np.abs(y_test - y_test_pred)
print(f"\n📊 ERRORES:")
print(f"   < $3k:  {(errors < 3000).sum()/len(errors)*100:.1f}%")
print(f"   < $5k:  {(errors < 5000).sum()/len(errors)*100:.1f}%")
print(f"   < $10k: {(errors < 10000).sum()/len(errors)*100:.1f}%")

# Feature importance
importances = pd.DataFrame({
    'feature': features,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n📊 IMPORTANCIA DE FEATURES:")
print(importances.to_string(index=False))

# ============================================================================
# 9. VALIDACIÓN CON EJEMPLOS REALES
# ============================================================================
print("\n" + "="*80)
print("EJEMPLOS DE PREDICCIÓN")
print("="*80)

for i in range(min(5, len(X_test))):
    ejemplo = X.loc[X_test.index[i]]
    real = y_test.iloc[i]
    pred = y_test_pred[i]
    error = abs(real - pred)
    error_pct = (error / real) * 100

    print(f"\nEjemplo {i+1}:")
    print(f"  {ejemplo['brand']} {int(ejemplo['year'])} - {ejemplo['fuel']} - {ejemplo['transmission']}")
    print(f"  {ejemplo['subcategory']} | {ejemplo['location']}")
    print(f"  Real: ${real:,.0f} | Predicho: ${pred:,.0f}")
    print(f"  Error: ${error:,.0f} ({error_pct:.1f}%)")

# ============================================================================
# 10. GUARDAR MODELO
# ============================================================================
print("\n" + "="*80)
print("GUARDANDO MODELO DEFINITIVO")
print("="*80)

model_dir = os.path.join(os.path.dirname(__file__), '..', 'apps', 'predictor', 'ml')
os.makedirs(model_dir, exist_ok=True)

# Modelo
with open(os.path.join(model_dir, 'model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
print("✅ model.pkl")

# Encoders
with open(os.path.join(model_dir, 'encoders.pkl'), 'wb') as f:
    pickle.dump(encoders, f)
print("✅ encoders.pkl")

# Métricas
metrics = {
    'train_mae': train_mae,
    'train_rmse': train_rmse,
    'train_r2': train_r2,
    'test_mae': test_mae,
    'test_rmse': test_rmse,
    'test_r2': test_r2,
    'cv_r2_mean': cv_scores.mean(),
    'cv_r2_std': cv_scores.std(),
    'best_params': grid_search.best_params_,
    'feature_importance': importances.to_dict(),
    'total_records': len(df),
    'features_used': features
}

with open(os.path.join(model_dir, 'metrics.pkl'), 'wb') as f:
    pickle.dump(metrics, f)
print("✅ metrics.pkl")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("✅ MODELO DEFINITIVO COMPLETADO")
print("="*80)
print(f"""
RESULTADOS:
- Registros entrenamiento: {len(X_train)}
- Registros test: {len(X_test)}
- R² en test: {test_r2:.4f}
- MAE en test: ${test_mae:,.2f}
- RMSE en test: ${test_rmse:,.2f}
- Precisión < $5k: {(errors < 5000).sum()/len(errors)*100:.1f}%

MEJORES PARÁMETROS:
{chr(10).join([f"- {k}: {v}" for k, v in grid_search.best_params_.items()])}

FEATURES MÁS IMPORTANTES:
{importances.head(5).to_string(index=False)}

🎯 Modelo listo para producción!
""")
