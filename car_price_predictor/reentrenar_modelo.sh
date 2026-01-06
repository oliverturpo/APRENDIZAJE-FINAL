#!/bin/bash

echo "========================================================================"
echo "SCRIPT DE REENTRENAMIENTO DEL MODELO - AutoPredict"
echo "========================================================================"

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "Error: Este script debe ejecutarse desde el directorio car_price_predictor/"
    exit 1
fi

print_success "Directorio correcto confirmado"

# Verificar que PostgreSQL esté corriendo
echo ""
echo "========================================================================"
echo "VERIFICANDO POSTGRESQL"
echo "========================================================================"

# Leer credenciales del .env
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    print_success "Credenciales cargadas desde .env"
else
    print_error ".env no encontrado"
    exit 1
fi

# Verificar conexión a PostgreSQL (requiere psql instalado)
if command -v psql &> /dev/null; then
    PGPASSWORD=$DB_PWD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM tbl_auto_raw_taller;" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        TOTAL_RECORDS=$(PGPASSWORD=$DB_PWD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM tbl_auto_raw_taller;")
        print_success "Conexión a PostgreSQL OK - Total registros: $TOTAL_RECORDS"
    else
        print_error "No se pudo conectar a PostgreSQL. Verifica que esté corriendo."
        exit 1
    fi
else
    print_warning "psql no encontrado, omitiendo verificación de BD"
fi

# Verificar Python
echo ""
echo "========================================================================"
echo "VERIFICANDO PYTHON Y DEPENDENCIAS"
echo "========================================================================"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python3 no encontrado"
    exit 1
fi

# Verificar pip
if command -v pip3 &> /dev/null || python3 -m pip --version &> /dev/null; then
    print_success "pip encontrado"
else
    print_error "pip no encontrado. Instala pip primero."
    exit 1
fi

# Instalar dependencias necesarias para el script
echo ""
echo "========================================================================"
echo "INSTALANDO DEPENDENCIAS NECESARIAS"
echo "========================================================================"

REQUIRED_PACKAGES="pandas numpy scikit-learn sqlalchemy psycopg2-binary python-dotenv"

echo "Instalando: $REQUIRED_PACKAGES"
python3 -m pip install -q $REQUIRED_PACKAGES

if [ $? -eq 0 ]; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error instalando dependencias"
    exit 1
fi

# Ejecutar el script de entrenamiento mejorado
echo ""
echo "========================================================================"
echo "EJECUTANDO REENTRENAMIENTO DEL MODELO"
echo "========================================================================"
echo ""

python3 notebooks/03_entrenar_modelo_mejorado.py

if [ $? -eq 0 ]; then
    echo ""
    print_success "¡Reentrenamiento completado exitosamente!"
    echo ""
    echo "========================================================================"
    echo "PRÓXIMOS PASOS:"
    echo "========================================================================"
    echo "1. Reinicia el servidor Django:"
    echo "   python manage.py runserver"
    echo ""
    echo "2. Prueba una predicción en:"
    echo "   http://localhost:5173/predictor"
    echo ""
    echo "3. Verifica las nuevas métricas en:"
    echo "   http://localhost:5173/dashboard"
    echo "========================================================================"
else
    print_error "Error durante el reentrenamiento"
    exit 1
fi
