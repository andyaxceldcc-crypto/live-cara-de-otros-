# 🎭 DeepFaceLive - Intercambiador de Caras en Tiempo Real

**DeepFaceLive** es una aplicación que permite intercambiar caras en tiempo real desde una webcam o desde un archivo de video, utilizando modelos de caras entrenados o fotos únicas.

> ⚠️ **Nota:** Las personas que aparecen son ficticias. Cualquier parecido con personas reales es accidental. ¡Excepto Keanu Reeves! Él existe y es increíble.

---

## 📖 Tabla de Contenidos

1. [Características](#-características)
2. [Modelos Disponibles](#-modelos-disponibles)
3. [Intercambio de Caras (DFM)](#-intercambio-de-caras-dfm)
4. [Intercambio de Caras (Insight)](#-intercambio-de-caras-insight)
5. [Animador de Caras](#-animador-de-caras)
6. [Requisitos del Sistema](#-requisitos-del-sistema)
7. [Documentación](#-documentación)
8. [Descargas](#-descargas)
9. [Comunidad](#-comunidad)
10. [Cómo Ayudar](#-cómo-ayudar)
11. [Instalación Rápida](#-instalación-rápida)

---

## 🎯 Características Principales

### 🔄 Intercambio de Caras (DFM)
Intercambia tu cara desde una webcam o la cara en un video usando modelos de caras entrenados.

### 👤 Intercambio con Foto Única (Insight)
Intercambia tu cara desde una webcam o la cara en el video usando tu propia foto única.

### 🎬 Animador de Caras
Controla una imagen estática de una cara usando video o tu propia cara desde la cámara.

---

## 📦 Modelos Disponibles

La siguiente es una lista de modelos públicos listos para usar:

### Modelos de Celebridades

| Celebridad | Imagen |
|------------|--------|
| Keanu Reeves | ![](doc/celebs/Keanu_Reeves/Keanu_Reeves.png) |
| Irina Arty | ![](doc/celebs/Irina_Arty/Irina_Arty.png) |
| Millie Park | ![](doc/celebs/Millie_Park/Millie_Park.png) |
| Rob Doe | ![](doc/celebs/Rob_Doe/Rob_Doe.png) |
| Jesse Stat | ![](doc/celebs/Jesse_Stat/Jesse_Stat.png) |
| Bryan Greynolds | ![](doc/celebs/Bryan_Greynolds/Bryan_Greynolds.png) |
| Mr. Bean | ![](doc/celebs/Mr_Bean/Mr_Bean.png) |
| Ewon Spice | ![](doc/celebs/Ewon_Spice/Ewon_Spice.png) |
| Natasha Former | ![](doc/celebs/Natasha_Former/Natasha_Former.png) |
| Emily Winston | ![](doc/celebs/Emily_Winston/Emily_Winston.png) |

### Más Modelos Disponibles

- Ava de Addario
- Dilraba Dilmurat
- Matilda Bobbie
- Yohanna Coralson
- Amber Song
- Kim Jarrey
- David Kovalniy
- Jackie Chan
- Nicola Badge
- Joker
- Dean Wiesel
- Silwan Stillwone
- Tim Chrys
- Zahar Lupin
- Tim Norland
- Natalie Fatman
- Liu Lice
- Albica Johns
- Meggie Merkel
- Tina Shift

### 💡 ¿Quieres Mejor Calidad?

Si quieres mayor calidad o mejor coincidencia de caras, puedes entrenar tu propio modelo usando [DeepFaceLab](https://github.com/iperov/DeepFaceLab).

Aquí hay un [ejemplo de Arnold Schwarzenegger](https://www.tiktok.com/@arnoldschwarzneggar/video/6995538782204300545) entrenado en una cara particular y usado en una videollamada.

---

## 🖥️ Intercambio de Caras (DFM)

Puedes intercambiar tu cara desde una webcam o la cara en el video usando modelos de caras entrenados.

![](doc/insight_faceswap_example.gif)

---

## 👤 Intercambio de Caras (Insight)

Puedes intercambiar tu cara desde una webcam o la cara en el video usando tu propia foto única.

![](doc/lukashenko.png)
![](doc/insight_faceswap_example.gif)

---

## 🎬 Animador de Caras

También hay un módulo de Animador de Caras en DeepFaceLive. Puedes controlar una imagen estática de una cara usando video o tu propia cara desde la cámara.

La calidad no es la mejor y requiere una buena coincidencia de caras y ajustar parámetros para cada par de caras, pero es suficiente para videos divertidos y memes o streaming en tiempo real a 25 fps usando GPU de 35 TFLOPS.

![](doc/face_animator_example.gif)

[![Stranger Things intro acapella](doc/Ng1C78Ceyxg_screenshot.png)](https://www.youtube.com/watch?v=Ng1C78Ceyxg)

Aquí hay un [video tutorial](doc/FaceAnimator_tutor.webm?raw=true) mostrando el proceso de configurar el Animador de Caras para Obama controlando la cara de Kim Chen.

---

## 🔧 Requisitos del Sistema

| Componente | Requisito |
|-----------|-----------|
| **Gráficos** | Cualquier tarjeta compatible con DirectX 12 (Recomendado: RTX 2070+ / Radeon RX 5700 XT+) |
| **Procesador** | CPU moderno con instrucciones AVX |
| **Memoria** | 4GB RAM mínimo, 32GB+ de archivo de paginación recomendado |
| **Sistema** | Windows 10 |

---

## 📚 Documentación

### Windows
- [Configuración principal](doc/windows/main_setup.md)
- [Configuración adicional para streaming](doc/windows/for_streaming.md)
- [Configuración adicional para videollamadas](doc/windows/for_video_calls.md)
- [Usar cámara de teléfono Android](doc/windows/using_android_phone_camera.md)

### Linux
- [Información de construcción](build/linux/README.md)

### FAQ (Preguntas Frecuentes)
- [Para Usuarios](doc/user_faq/user_faq.md)
- [Para Desarrolladores](doc/developer_faq/developer_faq.md)

---

## 📥 Descargas

### Windows 10 x64

| Enlace | Descripción |
|--------|-------------|
| [Yandex](https://disk.yandex.ru/d/7i5XTKIKVg5UUg) | Compilación para Windows 10 x64 |
| [Mega.nz](https://mega.nz/folder/m10iELBK#Y0H6BflF9C4k_clYofC7yA) | Compilación para Windows 10 x64 |

**Contenido del paquete:**
- Compilación independiente sin dependencias, lista para usar
- Puerto autoextraíble portable
- **Build DirectX12:** NVIDIA, AMD, Intel
- **Build NVIDIA:** Solo tarjetas NVIDIA, GT730 y superior. Funciona más rápido que DX12.

---

## 👥 Comunidad

| Plataforma | Descripción |
|------------|-------------|
| [Discord](https://discord.gg/rxa7h9M6rH) | Canal oficial de Discord. Inglés / Ruso. |
| QQ群 124500433 | Grupo de discusión en chino, contacto de negocios al administrador del grupo |

---

## 🤝 Cómo Ayudar al Proyecto

1. **Entrena tu propio modelo** siguiendo las recomendaciones en la sección FAQ y compártelo en Discord. Si el modelo tiene la calidad adecuada, se agregará a la biblioteca pública.

2. **Regístrate en GitHub** y presiona el botón "Star".

3. **Dona:**
   - [Yoomoney](https://yoomoney.ru/to/41001142318065)
   - **Bitcoin:** `bc1qewl062v70rszulml3f0mjdjrys8uxdydw3v6rq`

---

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/iperov/DeepFaceLive.git
cd DeepFaceLive

# Instalar dependencias
bash install.sh

# Activar entorno virtual
source deepfacelive_env/bin/activate

# Ejecutar
python main.py run DeepFaceLive --userdata-dir ./data

# Sin GPU NVIDIA
python main.py run DeepFaceLive --userdata-dir ./data --no-cuda
```

### Versiones de Dependencias Importantes

| Paquete | Versión |
|---------|---------|
| numpy | 1.21.6 - 1.26.x (⚠️ NO usar 2.x) |
| onnxruntime-gpu | 1.15.1 (requiere CUDA 11.x) |
| opencv-python | 4.8.0.74 |
| torch | 1.13.1 |
| torchvision | 0.14.1 |
| protobuf | 3.20.1 (⚠️ NO usar 4.x+) |
| PyQt6 | 6.5.1 |

---

## 📄 Licencia

Ver archivo [LICENSE](LICENSE)
