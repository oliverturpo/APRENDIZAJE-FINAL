import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Brain,
  Car,
  Calendar,
  Fuel,
  Settings,
  MapPin,
  Tag,
  Loader2,
  Sparkles,
  TrendingUp,
} from 'lucide-react';
import { getFormOptions, predictPrice } from '../services/api';

export default function PredictForm() {
  const navigate = useNavigate();
  const [options, setOptions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    brand: '',
    year: '',
    fuel: '',
    transmission: '',
    location: '',
    subcategory: '',
  });

  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    try {
      const data = await getFormOptions();
      setOptions(data);
    } catch (error) {
      console.error('Error loading options:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const result = await predictPrice({
        ...formData,
        year: parseInt(formData.year),
      });

      // Navegar inmediatamente
      navigate('/results', { state: { result } });
    } catch (error) {
      console.error('Error predicting price:', error);
      alert('Error al realizar la predicción');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  const formFields = [
    {
      name: 'brand',
      label: 'Marca del Vehículo',
      icon: Car,
      options: options?.brands || [],
      placeholder: 'Selecciona la marca',
    },
    {
      name: 'year',
      label: 'Año de Fabricación',
      icon: Calendar,
      options: options?.years || [],
      placeholder: 'Selecciona el año',
    },
    {
      name: 'fuel',
      label: 'Tipo de Combustible',
      icon: Fuel,
      options: options?.fuels || [],
      placeholder: 'Selecciona el combustible',
    },
    {
      name: 'transmission',
      label: 'Transmisión',
      icon: Settings,
      options: options?.transmissions || [],
      placeholder: 'Selecciona la transmisión',
    },
    {
      name: 'location',
      label: 'Ubicación',
      icon: MapPin,
      options: options?.locations || [],
      placeholder: 'Selecciona la ubicación',
    },
    {
      name: 'subcategory',
      label: 'Tipo de Vehículo',
      icon: Tag,
      options: options?.subcategories || [],
      placeholder: 'Selecciona el tipo',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 p-3">
          <Brain className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Predictor de Precios
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Ingresa las características del vehículo para estimar su valor de mercado
          </p>
        </div>
      </div>

      {/* Info Banner */}
      <div className="rounded-xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 dark:border-blue-800 dark:from-blue-900/20 dark:to-indigo-900/20 p-6">
        <div className="flex items-start gap-4">
          <div className="rounded-lg bg-blue-500 p-2">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
              Modelo de Machine Learning
            </h3>
            <p className="text-sm text-blue-700 dark:text-blue-300">
              Random Forest optimizado con <strong>GridSearchCV</strong> en datos del mercado peruano.
              Modelo mejorado con filtrado de outliers y feature engineering.
            </p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {formFields.map((field) => {
              const Icon = field.icon;
              return (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <div className="flex items-center gap-2">
                      <Icon className="h-4 w-4 text-gray-400" />
                      {field.label}
                    </div>
                  </label>
                  <select
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    required
                    className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                  >
                    <option value="">{field.placeholder}</option>
                    {field.options.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </div>
              );
            })}
          </div>

          {/* Submit Button */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 text-base font-semibold text-white shadow-lg hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:shadow-xl"
            >
              {submitting ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Prediciendo...
                </>
              ) : (
                <>
                  <TrendingUp className="h-5 w-5" />
                  Predecir Precio
                </>
              )}
            </button>
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="rounded-lg border border-gray-300 bg-white px-6 py-4 text-base font-semibold text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>

      {/* Additional Info */}
      <div className="rounded-xl border border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-800/50 p-6">
        <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
          ¿Cómo funciona la predicción?
        </h3>
        <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
          <li className="flex items-start gap-2">
            <div className="mt-0.5 h-1.5 w-1.5 rounded-full bg-blue-600 flex-shrink-0"></div>
            <span>
              El modelo analiza las características del vehículo y las compara con miles de
              vehículos similares en el mercado peruano.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-0.5 h-1.5 w-1.5 rounded-full bg-blue-600 flex-shrink-0"></div>
            <span>
              Utiliza algoritmos de Random Forest para estimar el precio más probable basándose
              en datos reales de NeoAuto.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-0.5 h-1.5 w-1.5 rounded-full bg-blue-600 flex-shrink-0"></div>
            <span>
              El precio estimado incluye un margen de error promedio de $8,951 USD, que refleja
              la variabilidad del mercado.
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}
