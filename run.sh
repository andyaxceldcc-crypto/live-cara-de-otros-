#!/bin/bash
# DeepFaceLive - Script de Ejecución Rápida
# Uso: bash run.sh [opciones]

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración
VENV_NAME="deepfacelive_env"
DATA_DIR="./data"

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cuda)
            NO_CUDA="--no-cuda"
            shift
            ;;
        --data-dir)
            DATA_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: bash run.sh [opciones]"
            echo ""
            echo "Opciones:"
            echo "  --no-cuda       Usar solo CPU (sin GPU)"
            echo "  --data-dir DIR  Directorio de datos (default: ./data)"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Verificar que el entorno virtual existe
if [ ! -d "$VENV_NAME" ]; then
    echo -e "${BLUE}[INFO]${NC} Entorno virtual no encontrado. Ejecutando install.sh..."
    bash install.sh
fi

# Activar entorno virtual
echo -e "${BLUE}[INFO]${NC} Activando entorno virtual..."
source "$VENV_NAME/bin/activate"

# Crear directorio de datos si no existe
mkdir -p "$DATA_DIR"

# Ejecutar
echo -e "${GREEN}[RUN]${NC} Iniciando DeepFaceLive..."
echo -e "${GREEN}[RUN]${NC} Directorio de datos: $DATA_DIR"
echo ""

python main.py run DeepFaceLive --userdata-dir "$DATA_DIR" $NO_CUDA

# Si la aplicación se cierra, mostrar mensaje
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${BLUE}[INFO]${NC} DeepFaceLive se ha cerrado."
    echo -e "${BLUE}[INFO]${NC} Para reiniciar, usa: bash run.sh"
fi