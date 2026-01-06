from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionInputSerializer, PredictionOutputSerializer
from .ml.predictor import predictor
from .models import Prediction
from apps.cars.models import Car


@api_view(['GET'])
def get_form_options(request):
    """Obtener todas las opciones disponibles para el formulario"""
    try:
        options = {
            'brands': predictor.get_available_brands(),
            'fuels': predictor.get_available_fuels(),
            'transmissions': predictor.get_available_transmissions(),
            'locations': predictor.get_available_locations(),
            'subcategories': predictor.get_available_subcategories(),
            'years': list(range(2026, 1989, -1)),
        }
        return Response(options)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def predict_price(request):
    """Endpoint para hacer predicción de precio"""
    serializer = PredictionInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        data = serializer.validated_data

        # Realizar predicción
        predicted_price = predictor.predict(
            brand=data['brand'],
            year=data['year'],
            fuel=data['fuel'],
            transmission=data['transmission'],
            location=data['location'],
            subcategory=data['subcategory']
        )

        # Guardar predicción en BD
        Prediction.objects.create(
            marca=data['brand'],
            anio=data['year'],
            combustible=data['fuel'],
            transmision=data['transmission'],
            ubicacion=data['location'],
            subcategoria=data['subcategory'],
            precio_predicho=predicted_price,
            ip_address=request.META.get('REMOTE_ADDR')
        )

        # Obtener métricas
        metrics = predictor.get_metrics()

        # Buscar autos similares - MUY similares (misma marca, combustible, transmisión, tipo)
        similar_cars_raw = Car.objects.filter(
            brand=data['brand'],
            fuel=data['fuel'],
            transmission=data['transmission'],
            subcategory=data['subcategory'],
            year__gte=data['year']-3,
            year__lte=data['year']+3,
            price__isnull=False
        ).exclude(price=0).order_by('?')[:5]

        # Si no hay suficientes, buscar solo por marca y año
        if similar_cars_raw.count() < 3:
            similar_cars_raw = Car.objects.filter(
                brand=data['brand'],
                year__gte=data['year']-3,
                year__lte=data['year']+3,
                price__isnull=False
            ).exclude(price=0).order_by('?')[:5]

        similar_cars = [
            {
                'brand': car.brand,
                'year': car.year,
                'fuel': car.fuel,
                'transmission': car.transmission,
                'subcategory': car.subcategory,
                'price': float(car.price) if car.price else None,
                'image': car.image if car.image else None,
                'link': car.link if car.link else None,
            }
            for car in similar_cars_raw
        ]

        response_data = {
            'predicted_price': predicted_price,
            'input_data': data,
            'metrics': metrics,
            'similar_cars': similar_cars,
        }

        return Response(response_data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_dashboard_stats(request):
    """Obtener estadísticas para el dashboard"""
    try:
        total_cars = Car.objects.count()
        total_predictions = Prediction.objects.count()
        metrics = predictor.get_metrics()

        # Obtener últimos autos scrapeados con imágenes
        recent_cars_raw = Car.objects.filter(
            image__isnull=False,
            price__isnull=False
        ).exclude(image='').order_by('-id')[:12]

        # Mapear para el frontend
        recent_cars = [
            {
                'id': car.id,
                'brand': car.brand,
                'year': car.year,
                'price': float(car.price) if car.price else None,
                'fuel': car.fuel,
                'transmission': car.transmission,
                'image_url': car.image,
                'detail_url': car.link,
            }
            for car in recent_cars_raw
        ]

        stats = {
            'total_cars': total_cars,
            'total_predictions': total_predictions,
            'model_r2': metrics.get('test_r2', 0),
            'model_mae': metrics.get('test_mae', 0),
            'model_rmse': metrics.get('test_rmse', 0),
            'recent_cars': recent_cars,
        }

        return Response(stats)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
