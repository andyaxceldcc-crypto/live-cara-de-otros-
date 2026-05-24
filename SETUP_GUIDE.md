# DeepFaceLive - Guía de Instalación Profesional

## Requisitos del Sistema

### Hardware
- **GPU**: Cualquier tarjeta gráfica compatible con DirectX 12 (recomendado: NVIDIA RTX 2070+ / AMD Radeon RX 5700 XT+)
- **CPU**: CPU moderno con instrucciones AVX
- **RAM**: 4GB mínimo, 32GB+ de archivo de paginación recomendado
- **SO**: Windows 10 (build oficial) o Linux (con Docker)

---

## Instalación Paso a Paso

### Paso 1: Python 3.9+ (o usar conda/env)

**Opción A: Python nativo**
```bash
# Instalar Python 3.11 (recomendado)
# Descargar de: https://www.python.org/downloads/

# Verificar instalación
python --version  # Debe mostrar Python 3.9+
```

**Opción B: Conda (recomendado para gestión de dependencias)**
```bash
# Instalar Miniconda
# Descargar de: https://docs.conda.io/en/latest/miniconda.html

# Crear entorno
conda create -n deepfacelive python=3.11
conda activate deepfacelive
```

**Opción C: venv**
```bash
python -m venv deepfacelive_env
source deepfacelive_env/bin/activate  # Linux/macOS
# deepfacelive_env\Scripts\activate   # Windows
```

---

### Paso 2: FFmpeg (Sistema)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Fedora:**
```bash
sudo dnf install ffmpeg
```

**Arch:**
```bash
sudo pacman -S ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```powershell
# Opción 1: Chocolatey
choco install ffmpeg

# Opción 2: Manual
# Descargar de: https://ffmpeg.org/download.html
# Agregar al PATH de Windows
```

---

### Paso 3: NVIDIA CUDA (si tienes GPU NVIDIA)

1. Descargar CUDA Toolkit 11.8+ de: https://developer.nvidia.com/cuda-downloads
2. Instalar drivers más recientes para tu tarjeta gráfica
3. Verificar con:
```bash
nvidia-smi
```

---

### Paso 4: Instalar Dependencias de Python

```bash
# Clonar repositorio
git clone https://github.com/iperov/DeepFaceLive.git
cd DeepFaceLive

# Crear/activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Paso 5: Versiones Específicas (Importante)

| Paquete | Versión | Notas |
|---------|---------|-------|
| Python | 3.9-3.12 | Python 3.13 tiene problemas de compatibilidad |
| numpy | 1.21.6 - 1.26.x | No usar 2.x (incompatible) |
| onnxruntime-gpu | 1.15.1 | Requiere CUDA 11.x |
| opencv-python | 4.8.0.74 | Verificar que opencv-contrib sea la misma versión |
| torch | 1.13.1 | Verificar con torchvision 0.14.1 |
| protobuf | 3.20.1 | No usar 4.x+ |
| PyQt6 | 6.5.1 | Alternativa: PyQt5 5.15+ |

---

## Ejecutar la Aplicación

### Uso Básico

```bash
# Ejecutar desde el directorio del proyecto
python main.py run DeepFaceLive --userdata-dir ./data
```

### Opciones de Ejecución

```bash
# Con directorio de datos personalizado
python main.py run DeepFaceLive --userdata-dir /ruta/a/tus/datos

# Sin CUDA (usar solo CPU)
python main.py run DeepFaceLive --userdata-dir ./data --no-cuda

# Entrenar FaceAligner
python main.py train FaceAligner --workspace-dir ./workspace --faceset-path ./faces.dfs
```

---

## Docker (Linux)

Si prefieres usar Docker:

```bash
cd build/linux/

# Construir imagen
docker build . -t deepfacelive

# Ejecutar (Linux con NVIDIA GPU)
docker run --gpus all --runtime=nvidia deepfacelive

# Con cámara web
./start.sh -c

# Con directorio de datos personalizado
./start.sh -d /home/user/data
```

---

## Solución de Problemas

### Error: "CUDA not found"
```bash
# Verificar que CUDA esté instalado
nvcc --version

# Verificar drivers NVIDIA
nvidia-smi

# Si no tienes GPU, usa --no-cuda
python main.py run DeepFaceLive --no-cuda
```

### Error: "ModuleNotFoundError"
```bash
# Reinstalar pip y dependencias
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error: "numpy.int64" problemas
```bash
# Usar numpy 1.x, no 2.x
pip install 'numpy<2.0.0'
```

### Error: "protobuf" incompatibility
```bash
# Versión específica requerida
pip install 'protobuf>=3.20.1,<4.0.0'
```

---

## Descargas Rápidas de Versiones Específicas

### NVIDIA CUDA 11.8
https://developer.nvidia.com/cuda-11-8-0-download-archive

### Python 3.11 (Windows)
https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

### FFmpeg (Windows)
https://www.gyan.dev/ffmpeg/builds/

---

## Resumen de Comandos Rápidos

```bash
# 1. Clonar
git clone https://github.com/iperov/DeepFaceLive.git
cd DeepFaceLive

# 2. Crear entorno
python -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Instalar FFmpeg (sistema)
# Ubuntu: sudo apt install ffmpeg

# 5. Ejecutar
python main.py run DeepFaceLive --userdata-dir ./data
```