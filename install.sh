#!/bin/bash
# DeepFaceLive - Script de Instalación Profesional
# Autor: AI Agent
# Uso: bash install.sh [opciones]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración por defecto
PYTHON_VERSION="3.11"
INSTALL_TYPE="full"  # full, cpu-only, minimal
FORCE_REINSTALL=false
SKIP_FFMPEG=false
USE_CUDA=true
VENV_NAME="deepfacelive_env"
PROJECT_DIR="$(pwd)"

# Funciones de utilidad
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Mostrar ayuda
show_help() {
    cat << EOF
DeepFaceLive - Script de Instalación Profesional

Uso: bash install.sh [opciones]

Opciones:
    -h, --help              Mostrar esta ayuda
    -p, --python VER        Versión de Python (default: 3.11)
    -t, --type TIPO         Tipo de instalación: full, cpu-only, minimal (default: full)
    -v, --venv NOMBRE       Nombre del entorno virtual (default: deepfacelive_env)
    -f, --force             Forzar reinstalación
    --no-ffmpeg             Omitir instalación de FFmpeg
    --no-cuda               Instalar versión CPU (sin GPU NVIDIA)
    --project DIR           Directorio del proyecto (default: $(pwd))

Ejemplos:
    bash install.sh                     # Instalación completa estándar
    bash install.sh -t cpu-only         # Solo CPU, sin GPU
    bash install.sh -p 3.10            # Python 3.10
    bash install.sh --no-cuda          # Sin soporte CUDA

EOF
}

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -p|--python)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        -t|--type)
            INSTALL_TYPE="$2"
            shift 2
            ;;
        -v|--venv)
            VENV_NAME="$2"
            shift 2
            ;;
        -f|--force)
            FORCE_REINSTALL=true
            shift
            ;;
        --no-ffmpeg)
            SKIP_FFMPEG=true
            shift
            ;;
        --no-cuda)
            USE_CUDA=false
            shift
            ;;
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        *)
            log_error "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificaciones previas
check_requirements() {
    log_info "Verificando requisitos del sistema..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 no está instalado. Por favor,instala Python 3.9+"
        exit 1
    fi
    
    PYTHON_VER=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
    if (( $(echo "$PYTHON_VER < 3.9" | bc -l) 2>/dev/null || [[ $(echo "$PYTHON_VER" | cut -d. -f1) -lt 3 ]] )); then
        log_error "Se requiere Python 3.9+. Versión actual: $PYTHON_VER"
        exit 1
    fi
    log_success "Python $PYTHON_VER detectado"
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
        log_error "pip no está instalado"
        exit 1
    fi
    log_success "pip detectado"
    
    # Verificar git
    if ! command -v git &> /dev/null; then
        log_error "git no está instalado"
        exit 1
    fi
    log_success "git detectado"
}

# Instalar FFmpeg
install_ffmpeg() {
    if [ "$SKIP_FFMPEG" = true ]; then
        log_warning "Omitiendo instalación de FFmpeg (--no-ffmpeg)"
        return
    fi
    
    log_info "Verificando/instalando FFmpeg..."
    
    if command -v ffmpeg &> /dev/null; then
        FFmpeg_VER=$(ffmpeg -version 2>&1 | head -1)
        log_success "FFmpeg ya instalado: $FFmpeg_VER"
        return
    fi
    
    # Detectar SO
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        OS="unknown"
    fi
    
    case "$OS" in
        ubuntu|debian|linuxmint)
            log_info "Instalando FFmpeg (Debian/Ubuntu)..."
            sudo apt update && sudo apt install -y ffmpeg
            ;;
        fedora)
            log_info "Instalando FFmpeg (Fedora)..."
            sudo dnf install -y ffmpeg
            ;;
        arch)
            log_info "Instalando FFmpeg (Arch)..."
            sudo pacman -S --noconfirm ffmpeg
            ;;
        centos|rhel)
            log_info "Instalando FFmpeg (CentOS/RHEL)..."
            sudo yum install -y epel-release
            sudo yum install -y ffmpeg
            ;;
        darwin)
            log_info "Instalando FFmpeg (macOS)..."
            if command -v brew &> /dev/null; then
                brew install ffmpeg
            else
                log_error "Homebrew no está instalado. Instálalo desde https://brew.sh"
                exit 1
            fi
            ;;
        *)
            log_warning "SO no detectado. Por favor, instala FFmpeg manualmente:"
            log_warning "https://ffmpeg.org/download.html"
            ;;
    esac
    
    if command -v ffmpeg &> /dev/null; then
        log_success "FFmpeg instalado correctamente"
    fi
}

# Crear entorno virtual
create_venv() {
    log_info "Creando entorno virtual: $VENV_NAME"
    
    if [ -d "$VENV_NAME" ]; then
        if [ "$FORCE_REINSTALL" = true ]; then
            log_warning "Eliminando entorno existente..."
            rm -rf "$VENV_NAME"
        else
            log_info "El entorno ya existe. Usando existente (usa -f para reinstalar)"
            return
        fi
    fi
    
    python3 -m venv "$VENV_NAME"
    log_success "Entorno virtual creado"
}

# Activar entorno virtual
activate_venv() {
    log_info "Activando entorno virtual..."
    source "$VENV_NAME/bin/activate"
    log_success "Entorno virtual activado"
}

# Instalar dependencias de Python
install_python_deps() {
    log_info "Instalando dependencias de Python..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Instalar dependencias base
    pip install numpy>=1.21.6,\<2.0.0
    
    if [ "$INSTALL_TYPE" = "cpu-only" ] || [ "$USE_CUDA" = false ]; then
        log_info "Instalando versión CPU..."
        pip install onnxruntime>=1.15.1
    else
        log_info "Instalando versión GPU (CUDA)..."
        pip install onnxruntime-gpu>=1.15.1
    fi
    
    pip install \
        opencv-python==4.8.0.74 \
        opencv-contrib-python==4.8.0.74 \
        onnx>=1.14.0 \
        torch>=1.13.1 \
        torchvision>=0.14.1 \
        h5py>=3.7.0 \
        'protobuf>=3.20.1,<4.0.0' \
        numexpr>=2.8.0 \
        PyQt6>=6.5.1 \
        scipy>=1.9.0 \
        Pillow>=9.0.0
    
    log_success "Dependencias instaladas"
}

# Crear directorio de datos
setup_data_dir() {
    log_info "Creando directorio de datos..."
    mkdir -p data
    mkdir -p models
    mkdir -p workspace
    log_success "Directorios creados: data/, models/, workspace/"
}

# Verificar instalación
verify_installation() {
    log_info "Verificando instalación..."
    
    source "$VENV_NAME/bin/activate"
    
    python3 -c "
import sys
print(f'Python: {sys.version}')

errors = []

try:
    import numpy
    print(f'numpy: {numpy.__version__}')
except ImportError as e:
    errors.append(f'numpy: {e}')

try:
    import cv2
    print(f'opencv-python: {cv2.__version__}')
except ImportError as e:
    errors.append(f'opencv-python: {e}')

try:
    import onnxruntime
    print(f'onnxruntime: {onnxruntime.__version__}')
except ImportError as e:
    errors.append(f'onnxruntime: {e}')

try:
    import torch
    print(f'torch: {torch.__version__}')
except ImportError as e:
    errors.append(f'torch: {e}')

try:
    from PyQt6.QtWidgets import QApplication
    print('PyQt6: OK')
except ImportError as e:
    errors.append(f'PyQt6: {e}')

if errors:
    print()
    print('ERRORES ENCONTRADOS:')
    for err in errors:
        print(f'  - {err}')
    sys.exit(1)
else:
    print()
    print('✓ Todas las dependencias están instaladas correctamente')
"
    
    if [ $? -eq 0 ]; then
        log_success "Verificación completada"
        return 0
    else
        log_error "Verificación fallida"
        return 1
    fi
}

# Mostrar siguiente paso
show_next_steps() {
    cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${GREEN}✓ Instalación completada correctamente!${NC}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGUIENTES PASOS:

1. Activar el entorno virtual:
   ${BLUE}source $VENV_NAME/bin/activate${NC}

2. Ejecutar la aplicación:
   ${BLUE}python main.py run DeepFaceLive --userdata-dir ./data${NC}

3. (Opcional) Sin GPU NVIDIA, usar:
   ${BLUE}python main.py run DeepFaceLive --userdata-dir ./data --no-cuda${NC}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMANDOS ÚTILES:

   Activar entorno:     source $VENV_NAME/bin/activate
   Desactivar entorno:  deactivate
   Ver dependencias:    pip list
   
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
}

# Función principal
main() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "         DeepFaceLive - Script de Instalación Profesional"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    log_info "Tipo de instalación: $INSTALL_TYPE"
    log_info "Versión de Python: $PYTHON_VERSION"
    log_info "Soporte CUDA: $USE_CUDA"
    echo ""
    
    check_requirements
    install_ffmpeg
    create_venv
    activate_venv
    install_python_deps
    setup_data_dir
    verify_installation
    show_next_steps
}

# Ejecutar
main "$@"