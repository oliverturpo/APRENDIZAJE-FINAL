import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Car,
  TrendingUp,
  Calculator,
  Activity,
  ArrowUpRight,
  Loader2,
  ExternalLink,
} from 'lucide-react';
import { getDashboardStats } from '../services/api';

export default function DashboardTailwind() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Vehículos',
      value: stats?.total_cars?.toLocaleString() || '0',
      subtitle: 'scrapeados de NeoAuto',
      icon: Car,
      color: 'blue',
    },
    {
      title: 'Precisión Modelo',
      value: `${Math.round((stats?.model_r2 || 0) * 100)}%`,
      subtitle: 'R² score',
      icon: TrendingUp,
      color: 'green',
    },
    {
      title: 'Error Promedio',
      value: `$${Math.round(stats?.model_mae || 0).toLocaleString()}`,
      subtitle: 'MAE',
      icon: Calculator,
      color: 'orange',
    },
    {
      title: 'Predicciones',
      value: stats?.total_predictions?.toLocaleString() || '0',
      subtitle: 'realizadas',
      icon: Activity,
      color: 'purple',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header con Logo NeoAuto */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Datos scrapeados de NeoAuto Perú
          </p>
        </div>
        <a
          href="https://neoauto.com"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          <img
            src="https://cde.neoauto.pe/neoauto3/img/logo/logo-neored.svg"
            alt="NeoAuto"
            className="h-6"
          />
          <ExternalLink className="h-4 w-4 text-gray-400" />
        </a>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          const colors = {
            blue: 'from-blue-500 to-blue-600',
            green: 'from-green-500 to-green-600',
            orange: 'from-orange-500 to-orange-600',
            purple: 'from-purple-500 to-purple-600',
          };

          return (
            <div
              key={index}
              className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${colors[stat.color]} p-6 text-white shadow-lg`}
            >
              <div className="absolute right-4 top-4 opacity-20">
                <Icon className="h-16 w-16" />
              </div>
              <div className="relative">
                <p className="text-sm font-medium opacity-90 mb-1">
                  {stat.title}
                </p>
                <h3 className="text-3xl font-bold mb-1">
                  {stat.value}
                </h3>
                <p className="text-xs opacity-75">
                  {stat.subtitle}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Últimos Autos Scrapeados */}
      <div className="rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Últimos Vehículos Scrapeados
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Datos reales de NeoAuto con imágenes y precios
            </p>
          </div>
          <Link
            to="/predictor"
            className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            Predecir Precio
            <ArrowUpRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {stats?.recent_cars?.map((car) => (
            <a
              key={car.id}
              href={car.detail_url}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative overflow-hidden rounded-lg border border-gray-200 bg-white transition-all hover:shadow-xl dark:border-gray-700 dark:bg-gray-800"
            >
              {/* Imagen */}
              <div className="relative aspect-[4/3] overflow-hidden bg-gray-100 dark:bg-gray-700">
                <img
                  src={car.image_url}
                  alt={`${car.brand} ${car.year}`}
                  className="h-full w-full object-cover transition-transform group-hover:scale-110"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/400x300?text=No+Image';
                  }}
                />
                <div className="absolute top-2 right-2">
                  <span className="rounded-full bg-green-500 px-2 py-1 text-xs font-bold text-white shadow-lg">
                    ${car.price?.toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Info */}
              <div className="p-3">
                <h3 className="font-bold text-gray-900 dark:text-white line-clamp-1">
                  {car.brand}
                </h3>
                <div className="mt-2 flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
                  <span>{car.year}</span>
                  <span className="truncate">{car.fuel}</span>
                </div>
                <div className="mt-1 text-xs text-gray-500 dark:text-gray-500">
                  {car.transmission}
                </div>
              </div>

              {/* Hover overlay */}
              <div className="absolute inset-0 flex items-center justify-center bg-black/60 opacity-0 transition-opacity group-hover:opacity-100">
                <div className="flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-900">
                  Ver en NeoAuto
                  <ExternalLink className="h-4 w-4" />
                </div>
              </div>
            </a>
          ))}
        </div>

        {(!stats?.recent_cars || stats.recent_cars.length === 0) && (
          <div className="text-center py-12">
            <Car className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              No hay autos disponibles para mostrar
            </p>
          </div>
        )}
      </div>

      {/* Model Info */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            Métricas del Modelo
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  R² Score
                </p>
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {stats?.model_r2?.toFixed(4) || '0.0000'}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  MAE
                </p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                  ${Math.round(stats?.model_mae || 0).toLocaleString()}
                </p>
              </div>
              <Calculator className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg bg-orange-50 dark:bg-orange-900/20">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  RMSE
                </p>
                <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                  ${Math.round(stats?.model_rmse || 0).toLocaleString()}
                </p>
              </div>
              <Activity className="h-8 w-8 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            Fuente de Datos
          </h3>
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
              <img
                src="https://cde.neoauto.pe/neoauto3/img/logo/logo-neored.svg"
                alt="NeoAuto"
                className="h-8"
              />
              <div className="flex-1">
                <p className="font-medium text-gray-900 dark:text-white">
                  NeoAuto Perú
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Marketplace #1 de autos en Perú
                </p>
              </div>
              <a
                href="https://neoauto.com"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
              >
                Visitar
              </a>
            </div>

            <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                Datos Scrapeados
              </h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li className="flex items-center gap-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-green-600"></div>
                  155 páginas procesadas
                </li>
                <li className="flex items-center gap-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-green-600"></div>
                  {stats?.total_cars?.toLocaleString() || '0'} vehículos catalogados
                </li>
                <li className="flex items-center gap-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-green-600"></div>
                  Imágenes y precios reales
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
