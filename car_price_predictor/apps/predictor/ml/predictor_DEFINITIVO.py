"""
Predictor DEFINITIVO - Compatible con modelo optimizado
"""

import pickle
import os
import pandas as pd
import numpy as np


class CarPricePredictor:
    """Predictor optimizado de precios de autos"""

    def __init__(self):
        self.model = None
        self.encoders = None
        self.metrics = None
        self.is_loaded = False
        self.load_model()

    def load_model(self):
        """Carga el modelo y encoders"""
        try:
            model_dir = os.path.dirname(__file__)

            with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
                self.model = pickle.load(f)

            with open(os.path.join(model_dir, 'encoders.pkl'), 'rb') as f:
                self.encoders = pickle.load(f)

            with open(os.path.join(model_dir, 'metrics.pkl'), 'rb') as f:
                self.metrics = pickle.load(f)

            self.is_loaded = True
            print("✅ Modelo DEFINITIVO cargado")

        except FileNotFoundError as e:
            print(f"❌ Modelo no encontrado: {e.filename}")
            self.is_loaded = False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.is_loaded = False

    def predict(self, brand, year, fuel, transmission, location, subcategory):
        """
        Predice el precio de un auto

        Args:
            brand (str): Marca (ej: 'TOYOTA')
            year (int): Año (ej: 2017)
            fuel (str): Combustible (ej: 'Diesel')
            transmission (str): Transmisión (ej: 'Mecánica')
            location (str): Ubicación (ej: 'Arequipa, Arequipa')
            subcategory (str): Tipo (ej: 'Camioneta')

        Returns:
            float: Precio predicho en USD
        """
        if not self.is_loaded:
            raise Exception("Modelo no cargado")

        # Calcular features derivados
        current_year = 2026
        car_age = current_year - year
        price_per_year = 20000 / (year - 1990 + 1)  # Estimación inicial

        # Determinar categoría de precio estimada (basada en marca/año)
        if year >= 2020:
            price_category = 'alto'
        elif year >= 2015:
            price_category = 'medio'
        else:
            price_category = 'economico'

        # Crear DataFrame
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

        # Codificar
        input_encoded = input_data.copy()
        categorical = ['brand', 'fuel', 'transmission', 'location', 'subcategory', 'price_category']

        for col in categorical:
            try:
                input_encoded[col] = self.encoders[col].transform(input_data[col].astype(str))
            except ValueError:
                # Valor no visto en entrenamiento
                print(f"⚠️  '{input_data[col].iloc[0]}' no conocido en {col}")
                input_encoded[col] = 0

        # Predicción
        prediction = self.model.predict(input_encoded)[0]

        return float(prediction)

    def predict_batch(self, data):
        """Predicción en lote"""
        if not self.is_loaded:
            raise Exception("Modelo no cargado")

        current_year = 2026
        data_with_features = data.copy()

        # Features derivados
        data_with_features['car_age'] = current_year - data_with_features['year']
        data_with_features['price_per_year'] = 20000 / (data_with_features['year'] - 1990 + 1)

        # Categoría de precio
        data_with_features['price_category'] = pd.cut(
            data_with_features['year'],
            bins=[0, 2010, 2015, 2020, 3000],
            labels=['economico', 'medio', 'alto', 'premium']
        )

        # Codificar
        data_encoded = data_with_features.copy()
        categorical = ['brand', 'fuel', 'transmission', 'location', 'subcategory', 'price_category']

        for col in categorical:
            data_encoded[col] = self.encoders[col].transform(data_with_features[col].astype(str))

        return self.model.predict(data_encoded)

    def get_metrics(self):
        """Retorna métricas del modelo"""
        return self.metrics if self.is_loaded else None

    def get_available_brands(self):
        return sorted(self.encoders['brand'].classes_.tolist()) if self.is_loaded else []

    def get_available_fuels(self):
        return sorted(self.encoders['fuel'].classes_.tolist()) if self.is_loaded else []

    def get_available_transmissions(self):
        return sorted(self.encoders['transmission'].classes_.tolist()) if self.is_loaded else []

    def get_available_locations(self):
        return sorted(self.encoders['location'].classes_.tolist()) if self.is_loaded else []

    def get_available_subcategories(self):
        return sorted(self.encoders['subcategory'].classes_.tolist()) if self.is_loaded else []


# Instancia global
predictor = CarPricePredictor()


def predict_price(brand, year, fuel, transmission, location, subcategory):
    """Función de conveniencia"""
    return predictor.predict(brand, year, fuel, transmission, location, subcategory)
