import { Link } from 'react-router-dom';
import {
  Sparkles,
  Database,
  Brain,
  Zap,
  ArrowRight,
  Code2,
  Server,
  BarChart3,
  CheckCircle2,
} from 'lucide-react';

export default function Home() {
  const techStack = [
    { name: 'Django REST API', icon: Server, color: 'text-green-600' },
    { name: 'React + Vite', icon: Code2, color: 'text-blue-600' },
    { name: 'PostgreSQL', icon: Database, color: 'text-indigo-600' },
    { name: 'Machine Learning', icon: Brain, color: 'text-purple-600' },
    { name: 'Scikit-learn', icon: BarChart3, color: 'text-orange-600' },
    { name: 'Tailwind CSS', icon: Zap, color: 'text-cyan-600' },
  ];

  const features = [
    {
      title: 'Predicción Inteligente',
      description: 'Modelo Random Forest optimizado con GridSearchCV y feature engineering',
      icon: Brain,
    },
    {
      title: 'API REST Moderna',
      description: 'Backend robusto con Django REST Framework para integraciones',
      icon: Server,
    },
    {
      title: 'Interfaz Moderna',
      description: 'UI responsive construida con React y Tailwind CSS',
      icon: Sparkles,
    },
    {
      title: 'Alta Precisión',
      description: 'Error promedio de ±$8,951 USD con R² score de 0.44',
      icon: BarChart3,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 relative overflow-hidden">
      {/* Hero Section CON puntitos */}
      <div className="relative overflow-hidden bg-dot-pattern bg-grid-pattern">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-6 py-24 sm:py-32">
          {/* Badge */}
          <div className="flex justify-center mb-8 animate-fade-in">
            <div className="inline-flex items-center gap-2 rounded-full bg-blue-100 px-4 py-1.5 text-sm font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
              <Sparkles className="h-4 w-4" />
              Predicción de Precios con IA
            </div>
          </div>

          {/* Title */}
          <div className="text-center space-y-6 animate-fade-in-up">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-gray-900 dark:text-white">
              Bienvenido a{' '}
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AutoPredict
              </span>
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Calculadora inteligente de predicción de precios de autos usados en Perú
            </p>
            <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
              Utilizando Machine Learning y datos reales del mercado peruano para estimar el valor de tu vehículo
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-12 animate-fade-in-up animation-delay-200">
            <Link
              to="/predictor"
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:bg-blue-700 transition-all hover:scale-105 hover:shadow-xl"
            >
              Predecir Precio Ahora
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-8 py-4 text-base font-semibold text-gray-900 shadow-lg hover:bg-gray-50 transition-all hover:scale-105 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700"
            >
              Ver Dashboard
              <BarChart3 className="h-5 w-5" />
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Características Principales
            </h2>
            <p className="text-lg text-gray-300">
              Sistema completo de predicción con tecnología de punta
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="group relative rounded-2xl border border-gray-700 bg-gray-800/50 backdrop-blur-sm p-6 shadow-sm transition-all hover:shadow-xl hover:scale-105 animate-fade-in-up"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="mb-4 inline-flex rounded-lg bg-blue-500/20 p-3 text-blue-400">
                    <Icon className="h-6 w-6" />
                  </div>
                  <h3 className="mb-2 text-lg font-semibold text-white">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-400">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Tech Stack Section - SIN puntitos */}
      <div className="bg-gray-900">
        <div className="max-w-7xl mx-auto px-6 py-24 border-t border-gray-800">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Tecnologías Utilizadas
            </h2>
            <p className="text-lg text-gray-400">
              Stack moderno y robusto para aplicaciones de Machine Learning
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {techStack.map((tech, index) => {
              const Icon = tech.icon;
              return (
                <div
                  key={index}
                  className="flex flex-col items-center gap-3 rounded-xl border border-gray-700 bg-gray-800/50 p-6 transition-all hover:shadow-lg hover:scale-105 animate-fade-in-up"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <Icon className={`h-8 w-8 ${tech.color}`} />
                  <span className="text-sm font-medium text-white text-center">
                    {tech.name}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

      {/* Stats Section */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <div className="rounded-2xl border border-gray-200 bg-gradient-to-r from-blue-600 to-indigo-600 p-12 text-center shadow-2xl dark:border-gray-700">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-12">
            Datos del Sistema
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-2">
              <p className="text-5xl font-bold text-white">ML</p>
              <p className="text-blue-100">Modelo Optimizado</p>
            </div>
            <div className="space-y-2">
              <p className="text-5xl font-bold text-white">✓</p>
              <p className="text-blue-100">Modelo Mejorado</p>
            </div>
            <div className="space-y-2">
              <p className="text-5xl font-bold text-white">API</p>
              <p className="text-blue-100">REST Backend</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <div className="rounded-2xl border border-gray-700 bg-gray-800/50 p-12 text-center shadow-lg">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            ¿Listo para predecir el precio de tu auto?
          </h2>
          <p className="text-lg text-gray-400 mb-8 max-w-2xl mx-auto">
            Obtén una estimación precisa en segundos con nuestro modelo de Machine Learning
          </p>
          <Link
            to="/predictor"
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:bg-blue-700 transition-all hover:scale-105"
          >
            Comenzar Ahora
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </div>
      </div>
    </div>
  );
}
