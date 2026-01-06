import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  DirectionsCar,
  TrendingUp,
  Calculate,
  CheckCircle,
} from '@mui/icons-material';
import { getDashboardStats } from '../services/api';

export default function Dashboard() {
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
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <CircularProgress />
      </Box>
    );
  }

  const statCards = [
    {
      title: 'Total Vehículos',
      value: stats?.total_cars?.toLocaleString() || '0',
      subtitle: 'en base de datos',
      icon: <DirectionsCar sx={{ fontSize: 40 }} />,
      color: '#2563eb',
    },
    {
      title: 'Precisión Modelo',
      value: `${Math.round((stats?.model_r2 || 0) * 100)}%`,
      subtitle: 'R² score',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: '#10b981',
    },
    {
      title: 'Error Promedio',
      value: `$${Math.round(stats?.model_mae || 0).toLocaleString()}`,
      subtitle: 'MAE',
      icon: <Calculate sx={{ fontSize: 40 }} />,
      color: '#f59e0b',
    },
    {
      title: 'Predicciones',
      value: stats?.total_predictions?.toLocaleString() || '0',
      subtitle: 'realizadas',
      icon: <CheckCircle sx={{ fontSize: 40 }} />,
      color: '#10b981',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
        Dashboard
      </Typography>
      <Typography variant="body1" sx={{ color: '#666', mb: 4 }}>
        Sistema de predicción de precios de vehículos
      </Typography>

      {/* Stats Grid */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ height: '100%', border: '1px solid #e0e0e0' }}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography variant="caption" sx={{ color: '#999', textTransform: 'uppercase' }}>
                      {stat.title}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: stat.color, my: 1 }}>
                      {stat.value}
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#666' }}>
                      {stat.subtitle}
                    </Typography>
                  </Box>
                  <Box sx={{ color: stat.color, opacity: 0.3 }}>
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Main Cards */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                📥 Data Pipeline
              </Typography>
              <Typography variant="body2" sx={{ color: '#666', mb: 2 }}>
                Sistema automatizado de extracción y carga de datos del mercado de vehículos.
              </Typography>
              <Box component="ul" sx={{ pl: 2, mb: 3 }}>
                <li>Motor de web scraping</li>
                <li>Transformación de datos</li>
                <li>Almacenamiento PostgreSQL</li>
              </Box>
              <Button variant="contained" fullWidth sx={{ bgcolor: '#2563eb' }}>
                Ejecutar Pipeline
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                🤖 Price Predictor
              </Typography>
              <Typography variant="body2" sx={{ color: '#666', mb: 2 }}>
                Modelo Random Forest optimizado con GridSearchCV para estimación precisa de precios.
              </Typography>
              <Box component="ul" sx={{ pl: 2, mb: 3 }}>
                <li>Algoritmo Random Forest</li>
                <li>Análisis de 9 características</li>
                <li>Predicciones en tiempo real</li>
              </Box>
              <Button
                component={Link}
                to="/predictor"
                variant="contained"
                fullWidth
                sx={{ bgcolor: '#2563eb' }}
              >
                Hacer Predicción
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
