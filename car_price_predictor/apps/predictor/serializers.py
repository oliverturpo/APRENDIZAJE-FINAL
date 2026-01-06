from rest_framework import serializers


class PredictionInputSerializer(serializers.Serializer):
    """Serializer para los datos de entrada de la predicción"""
    brand = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    fuel = serializers.CharField(max_length=50)
    transmission = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    subcategory = serializers.CharField(max_length=100)


class PredictionOutputSerializer(serializers.Serializer):
    """Serializer para el resultado de la predicción"""
    predicted_price = serializers.FloatField()
    input_data = serializers.DictField()
    metrics = serializers.DictField()
    similar_cars = serializers.ListField()
