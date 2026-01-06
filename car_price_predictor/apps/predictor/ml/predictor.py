"""
Módulo Predictor de Precios de Autos
Carga el modelo entrenado y realiza predicciones
"""

import pickle
import os
import pandas as pd
import numpy as np


class CarPricePredictor:
    """Predictor de precios de autos usando Random Forest"""

    def __init__(self):
        """Inicializa el predictor cargando el modelo y encoders"""
        self.model = None
        self.encoders = None
        self.metrics = None
        self.is_loaded = False

        # Cargar modelo automáticamente
        self.load_model()

    def load_model(self):
        """Carga el modelo y encoders desde archivos pickle"""
        try:
            # Directorio del modelo
            model_dir = os.path.dirname(__file__)

            # Cargar modelo
            model_path = os.path.join(model_dir, 'model.pkl')
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

            # Cargar encoders
            encoders_path = os.path.join(model_dir, 'encoders.pkl')
            with open(encoders_path, 'rb') as f:
                self.encoders = pickle.load(f)

            # Cargar métricas
            metrics_path = os.path.join(model_dir, 'metrics.pkl')
            with open(metrics_path, 'rb') as f:
                self.metrics = pickle.load(f)

            self.is_loaded = True
            print("✅ Modelo cargado exitosamente")

        except FileNotFoundError as e:
            print(f"❌ Error: Modelo no encontrado. Ejecuta primero el script de entrenamiento.")
            print(f"   Archivo faltante: {e.filename}")
            self.is_loaded = False
        except Exception as e:
            print(f"❌ Error cargando modelo: {str(e)}")
            self.is_loaded = False

    def predict(self, brand, year, fuel, transmission, location, subcategory):
        """
        Predice el precio de un auto basado en sus características

        Args:
            brand (str): Marca del auto (ej: 'TOYOTA')
            year (int): Año del auto (ej: 2020)
            fuel (str): Tipo de combustible (ej: 'Gasolina')
            transmission (str): Tipo de transmisión (ej: 'Automática')
            location (str): Ubicación (ej: 'Lima, Lima')
            subcategory (str): Subcategoría (ej: 'Sedan')

        Returns:
            float: Precio predicho en USD
        """
        if not self.is_loaded:
            raise Exception("Modelo no cargado. No se puede realizar predicción.")

        # Calcular features derivados
        current_year = 2026
        car_age = current_year - year
        price_per_year = 20000 / (year - 1990 + 1)

        # Categoría de precio estimada
        if year >= 2020:
            price_category = 'alto'
        elif year >= 2015:
            price_category = 'medio'
        else:
            price_category = 'economico'

        # Crear DataFrame con los datos de entrada
        input_data = pd.DataFrame({
            'brand': [brand],
            'year': [year],
            'fuel': [fuel],
            'transmission': [transmission],
            'location': [location],
            'subcategory': [subcategory],
            'car_age': [car_age],
            'price_per_year': [price_per_year],
            'price_category': [price_category]
        })

        # Codificar variables categóricas
        input_encoded = input_data.copy()

        categorical_features = ['brand', 'fuel', 'transmission', 'location', 'subcategory', 'price_category']

        for col in categorical_features:
            try:
                # Intentar transformar usando el encoder
                input_encoded[col] = self.encoders[col].transform(input_data[col].astype(str))
            except ValueError:
                # Si la categoría no existe en el encoder, usar la primera clase
                print(f"⚠️  Advertencia: '{input_data[col].iloc[0]}' no visto en entrenamiento para {col}. Usando valor por defecto.")
                input_encoded[col] = 0  # Valor por defecto

        # Realizar predicción
        prediction = self.model.predict(input_encoded)[0]

        return float(prediction)

    def predict_batch(self, data):
        """
        Predice precios para múltiples autos

        Args:
            data (pd.DataFrame): DataFrame con columnas: brand, year, fuel, transmission, location, subcategory

        Returns:
            np.array: Array de precios predichos
        """
        if not self.is_loaded:
            raise Exception("Modelo no cargado. No se puede realizar predicción.")

        # Calcular features derivados
        current_year = 2026
        data_with_features = data.copy()
        data_with_features['car_age'] = current_year - data_with_features['year']
        data_with_features['price_per_year'] = 20000 / (data_with_features['year'] - 1990 + 1)

        # Categoría de precio
        data_with_features['price_category'] = pd.cut(
            data_with_features['year'],
            bins=[0, 2010, 2015, 2020, 3000],
            labels=['economico', 'medio', 'alto', 'premium']
        )

        # Codificar variables categóricas
        data_encoded = data_with_features.copy()

        categorical_features = ['brand', 'fuel', 'transmission', 'location', 'subcategory', 'price_category']

        for col in categorical_features:
            data_encoded[col] = self.encoders[col].transform(data_with_features[col].astype(str))

        # Realizar predicciones
        predictions = self.model.predict(data_encoded)

        return predictions

    def get_metrics(self):
        """Retorna las métricas del modelo"""
        if not self.is_loaded:
            return None
        return self.metrics

    def get_available_brands(self):
        """Retorna lista de marcas disponibles"""
        if not self.is_loaded:
            return []
        return sorted(self.encoders['brand'].classes_.tolist())

    def get_available_fuels(self):
        """Retorna lista de tipos de combustible disponibles"""
        if not self.is_loaded:
            return []
        return sorted(self.encoders['fuel'].classes_.tolist())

    def get_available_transmissions(self):
        """Retorna lista de transmisiones disponibles"""
        if not self.is_loaded:
            return []
        return sorted(self.encoders['transmission'].classes_.tolist())

    def get_available_locations(self):
        """Retorna lista de ubicaciones disponibles"""
        if not self.is_loaded:
            return []
        return sorted(self.encoders['location'].classes_.tolist())

    def get_available_subcategories(self):
        """Retorna lista de subcategorías disponibles"""
        if not self.is_loaded:
            return []
        return sorted(self.encoders['subcategory'].classes_.tolist())


# Instancia global del predictor
predictor = CarPricePredictor()


# Función de conveniencia para predicciones rápidas
def predict_price(brand, year, fuel, transmission, location, subcategory):
    """
    Función de conveniencia para predicción rápida

    Returns:
        float: Precio predicho en USD
    """
    return predictor.predict(brand, year, fuel, transmission, location, subcategory)
