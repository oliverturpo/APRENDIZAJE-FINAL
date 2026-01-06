import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  CheckCircle2,
  TrendingUp,
  Calculator,
  Activity,
  Car,
  Calendar,
  Fuel,
  Settings,
  MapPin,
  Tag,
  ArrowLeft,
  Repeat,
  AlertCircle,
  Sparkles,
  DollarSign,
} from 'lucide-react';

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;
  const [imageErrors, setImageErrors] = useState({});

  if (!result) {
    return (
      <div className="space-y-6">
        <div className="rounded-xl border border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-900/20 p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="h-6 w-6 text-orange-600 dark:text-orange-400 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-orange-900 dark:text-orange-100 mb-1">
                No hay datos de predicción disponibles
              </h3>
              <p className="text-sm text-orange-700 dark:text-orange-300">
                Debes completar el formulario de predicción primero.
              </p>
            </div>
          </div>
        </div>
        <button
          onClick={() => navigate('/predictor')}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-white font-medium hover:bg-blue-700 transition-colors"
        >
          Hacer Predicción
        </button>
      </div>
    );
  }

  const { predicted_price, input_data, metrics, similar_cars } = result;

  // Debug: Ver qué datos llegan
  console.log('Similar cars data:', similar_cars);

  const carDetails = [
    { label: 'Marca', value: input_data.brand, icon: Car },
    { label: 'Año', value: input_data.year, icon: Calendar },
    { label: 'Combustible', value: input_data.fuel, icon: Fuel },
    { label: 'Transmisión', value: input_data.transmission, icon: Settings },
    { label: 'Ubicación', value: input_data.location, icon: MapPin },
    { label: 'Tipo', value: input_data.subcategory, icon: Tag },
  ];

  const modelMetrics = [
    {
      label: 'R² Score',
      value: metrics.test_r2.toFixed(4),
      description: 'Coeficiente de determinación',
      icon: TrendingUp,
      color: 'blue',
    },
    {
      label: 'MAE',
      value: `$${Math.round(metrics.test_mae).toLocaleString()}`,
      description: 'Error Promedio',
      icon: Calculator,
      color: 'green',
    },
    {
      label: 'RMSE',
      value: `$${Math.round(metrics.test_rmse).toLocaleString()}`,
      description: 'Error Cuadrático Medio',
      icon: Activity,
      color: 'orange',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-gradient-to-br from-green-500 to-green-600 p-3">
          <CheckCircle2 className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Resultado de Predicción
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            El modelo ha estimado el precio basándose en las especificaciones proporcionadas
          </p>
        </div>
      </div>

      {/* Success Alert */}
      <div className="rounded-xl border border-green-200 bg-gradient-to-r from-green-50 to-emerald-50 dark:border-green-800 dark:from-green-900/20 dark:to-emerald-900/20 p-6">
        <div className="flex items-start gap-4">
          <div className="rounded-lg bg-green-500 p-2">
            <CheckCircle2 className="h-5 w-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-green-900 dark:text-green-100 mb-1">
              ¡Predicción Exitosa!
            </h3>
            <p className="text-sm text-green-700 dark:text-green-300">
              El modelo de Machine Learning ha procesado los datos y generado una estimación precisa del valor del vehículo.
            </p>
          </div>
        </div>
      </div>

      {/* Predicted Price - Hero Card */}
      <div className="relative overflow-hidden rounded-2xl border-2 border-blue-200 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 p-10 text-white shadow-2xl dark:border-blue-700">
        <div className="absolute top-0 right-0 opacity-5">
          <DollarSign className="h-64 w-64 -rotate-12" />
        </div>
        <div className="absolute -bottom-10 -left-10 opacity-10">
          <Sparkles className="h-48 w-48" />
        </div>
        <div className="relative text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="rounded-full bg-white/20 px-4 py-1.5 backdrop-blur-sm">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 animate-pulse" />
                <p className="text-sm font-semibold uppercase tracking-wider">
                  Precio Estimado
                </p>
              </div>
            </div>
          </div>
          <div className="mb-4">
            <h2 className="text-7xl font-black mb-2 drop-shadow-lg">
              ${predicted_price.toLocaleString('en-US', { maximumFractionDigits: 0 })}
            </h2>
            <div className="inline-block rounded-full bg-white/20 px-6 py-2 backdrop-blur-sm">
              <p className="text-lg font-semibold">
                Dólares Estadounidenses
              </p>
            </div>
          </div>
          <div className="flex items-center justify-center gap-8 mt-6">
            <div className="rounded-xl bg-white/10 px-6 py-3 backdrop-blur-sm">
              <p className="text-xs opacity-75 mb-1">Margen de Error</p>
              <p className="text-xl font-bold">
                ±${Math.round(metrics.test_mae).toLocaleString()}
              </p>
            </div>
            <div className="rounded-xl bg-white/10 px-6 py-3 backdrop-blur-sm">
              <p className="text-xs opacity-75 mb-1">Precisión (R²)</p>
              <p className="text-xl font-bold">
                {(metrics.test_r2 * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Car Characteristics */}
      <div className="rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 p-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
          Características del Vehículo
        </h3>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {carDetails.map((detail, index) => {
            const Icon = detail.icon;
            return (
              <div
                key={index}
                className="flex items-center gap-3 rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-700/50"
              >
                <div className="rounded-lg bg-blue-100 p-2 dark:bg-blue-900/30">
                  <Icon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {detail.label}
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {detail.value}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Similar Cars */}
      {similar_cars && similar_cars.length > 0 && (
        <div className="rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 p-2">
              <Car className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                Autos Similares en el Mercado
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Comparación con vehículos reales del mercado peruano
              </p>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {similar_cars.map((car, index) => (
              <a
                key={`car-${index}-${car.brand}-${car.year}`}
                href={car.link || '#'}
                target={car.link ? '_blank' : '_self'}
                rel="noopener noreferrer"
                className="group relative overflow-hidden rounded-xl border border-gray-200 bg-gradient-to-br from-white to-gray-50 hover:shadow-xl transition-all dark:border-gray-700 dark:from-gray-800 dark:to-gray-700/50 cursor-pointer"
              >
                {/* Imagen del auto */}
                <div className="relative h-48 w-full overflow-hidden bg-gray-100 dark:bg-gray-700">
                  {car.image && !imageErrors[index] ? (
                    <img
                      src={car.image}
                      alt={`${car.brand} ${car.year}`}
                      className="h-full w-full object-cover transition-transform group-hover:scale-110"
                      onError={() => setImageErrors(prev => ({ ...prev, [index]: true }))}
                    />
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Car className="h-16 w-16 text-gray-400" />
                    </div>
                  )}
                </div>

                {/* Contenido */}
                <div className="p-5">
                  <div className="mb-3">
                    <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                      {car.brand} {car.year}
                    </h4>
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400">
                        <Fuel className="h-3.5 w-3.5" />
                        <span>{car.fuel}</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400">
                        <Settings className="h-3.5 w-3.5" />
                        <span>{car.transmission}</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400">
                        <Tag className="h-3.5 w-3.5" />
                        <span>{car.subcategory}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-600">
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                      Precio Real
                    </span>
                    <span className="rounded-lg bg-gradient-to-r from-green-500 to-emerald-500 px-4 py-2 text-base font-bold text-white shadow-lg">
                      ${car.price.toLocaleString('en-US', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Model Metrics */}
      <div className="rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 p-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
          Métricas del Modelo
        </h3>
        <div className="grid gap-4 md:grid-cols-3">
          {modelMetrics.map((metric, index) => {
            const Icon = metric.icon;
            const colors = {
              blue: 'from-blue-500 to-blue-600',
              green: 'from-green-500 to-green-600',
              orange: 'from-orange-500 to-orange-600',
            };

            return (
              <div
                key={index}
                className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${colors[metric.color]} p-6 text-white shadow-lg`}
              >
                <div className="absolute right-4 top-4 opacity-20">
                  <Icon className="h-12 w-12" />
                </div>
                <div className="relative">
                  <p className="text-sm font-medium opacity-90 mb-1">
                    {metric.label}
                  </p>
                  <h3 className="text-3xl font-bold mb-1">
                    {metric.value}
                  </h3>
                  <p className="text-xs opacity-75">
                    {metric.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4">
        <button
          onClick={() => navigate('/predictor')}
          className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 text-base font-semibold text-white shadow-lg hover:from-blue-700 hover:to-indigo-700 transition-all hover:shadow-xl"
        >
          <Repeat className="h-5 w-5" />
          Nueva Predicción
        </button>
        <button
          onClick={() => navigate('/dashboard')}
          className="flex-1 flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-6 py-4 text-base font-semibold text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
          Volver al Dashboard
        </button>
      </div>
    </div>
  );
}
