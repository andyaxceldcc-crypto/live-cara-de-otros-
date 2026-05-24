#!/usr/bin/env python3
"""
DeepFaceLive - Script de Instalación en Python
Funciona en Windows, Linux y macOS
Uso: python install.py [opciones]
"""

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path


def get_color_codes():
    """Retorna códigos de color ANSI."""
    return {
        'RED': '\033[0;31m',
        'GREEN': '\033[0;32m',
        'YELLOW': '\033[1;33m',
        'BLUE': '\033[0;34m',
        'NC': '\033[0m'
    }


def log(msg, level='INFO'):
    """Imprime mensaje con color."""
    colors = get_color_codes()
    color = {
        'INFO': colors['BLUE'],
        'SUCCESS': colors['GREEN'],
        'WARNING': colors['YELLOW'],
        'ERROR': colors['RED']
    }.get(level, colors['NC'])
    print(f"{color}[{level}]{colors['NC']} {msg}")


def run_command(cmd, check=True, shell=False):
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(
            cmd if shell else cmd.split(),
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        if check:
            raise
        return False, "", str(e)


def check_python_version():
    """Verifica que Python sea 3.9+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        log(f"Python 3.9+ requerido. Versión actual: {version.major}.{version.minor}", 'ERROR')
        sys.exit(1)
    log(f"Python {version.major}.{version.minor}.{version.micro} detectado")


def check_requirements():
    """Verifica requisitos previos."""
    log("Verificando requisitos del sistema...")
    
    # Python
    check_python_version()
    
    # pip
    has_pip, _, _ = run_command([sys.executable, '-m', 'pip', '--version'], check=False)
    if not has_pip:
        log("pip no está instalado", 'ERROR')
        sys.exit(1)
    log("pip detectado")
    
    # git
    has_git, _, _ = run_command(['git', '--version'], check=False)
    if not has_git:
        log("git no está instalado", 'WARNING')
        log("Se recomienda instalar git para actualizaciones", 'WARNING')


def install_ffmpeg():
    """Instala FFmpeg según el SO."""
    # Verificar si ya está instalado
    success, _, _ = run_command(['ffmpeg', '-version'], check=False)
    if success:
        log("FFmpeg ya instalado")
        return True
    
    log("Intentando instalar FFmpeg...")
    
    # Detectar SO
    if sys.platform == 'win32':
        log("Windows detectado", 'INFO')
        log("Por favor, instala FFmpeg manualmente:", 'WARNING')
        log("  Opción 1: chocolatey - choco install ffmpeg", 'INFO')
        log("  Opción 2: Descargar de https://ffmpeg.org/download.html", 'INFO')
        return False
    
    elif sys.platform == 'darwin':
        success, _, _ = run_command(['brew', '--version'], check=False)
        if success:
            log("Instalando FFmpeg (macOS)...")
            return run_command(['brew', 'install', 'ffmpeg'])[0]
        else:
            log("Homebrew no está instalado. Instálalo desde https://brew.sh", 'WARNING')
            return False
    
    else:  # Linux
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content:
                    log("Instalando FFmpeg (Debian/Ubuntu)...")
                    run_command(['sudo', 'apt', 'update'])
                    return run_command(['sudo', 'apt', 'install', '-y', 'ffmpeg'])[0]
                elif 'fedora' in content:
                    log("Instalando FFmpeg (Fedora)...")
                    return run_command(['sudo', 'dnf', 'install', '-y', 'ffmpeg'])[0]
                elif 'arch' in content:
                    log("Instalando FFmpeg (Arch)...")
                    return run_command(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'])[0]
        
        log("No se pudo detectar el SO para instalar FFmpeg", 'WARNING')
        return False


def create_virtualenv(venv_path):
    """Crea entorno virtual."""
    venv_path = Path(venv_path)
    
    if venv_path.exists():
        log(f"Entorno virtual ya existe: {venv_path}")
        return True
    
    log(f"Creando entorno virtual: {venv_path}")
    success, _, stderr = run_command([sys.executable, '-m', 'venv', str(venv_path)])
    
    if not success:
        log(f"Error creando entorno virtual: {stderr}", 'ERROR')
        return False
    
    log("Entorno virtual creado")
    return True


def get_venv_python(venv_path):
    """Obtiene la ruta al Python del entorno virtual."""
    venv_path = Path(venv_path)
    if sys.platform == 'win32':
        return venv_path / 'Scripts' / 'python.exe'
    else:
        return venv_path / 'bin' / 'python'


def install_dependencies(venv_path, cpu_only=False):
    """Instala dependencias de Python."""
    venv_python = get_venv_python(venv_path)
    
    log("Actualizando pip...")
    run_command([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    log("Instalando dependencias...")
    
    packages = [
        'numpy>=1.21.6,<2.0.0',
        'opencv-python==4.8.0.74',
        'opencv-contrib-python==4.8.0.74',
        'onnx>=1.14.0',
        'torch>=1.13.1',
        'torchvision>=0.14.1',
        'h5py>=3.7.0',
        'protobuf>=3.20.1,<4.0.0',
        'numexpr>=2.8.0',
        'PyQt6>=6.5.1',
        'scipy>=1.9.0',
        'Pillow>=9.0.0',
    ]
    
    if cpu_only:
        packages.append('onnxruntime>=1.15.1')
    else:
        packages.append('onnxruntime-gpu>=1.15.1')
    
    for package in packages:
        log(f"Instalando: {package}")
        run_command([str(venv_python), '-m', 'pip', 'install', package])
    
    log("Dependencias instaladas")


def verify_installation(venv_path):
    """Verifica que todo esté instalado."""
    venv_python = get_venv_python(venv_path)
    
    log("Verificando instalación...")
    
    modules = ['numpy', 'cv2', 'onnxruntime', 'torch', 'PyQt6']
    all_ok = True
    
    for module in modules:
        success, stdout, stderr = run_command(
            [str(venv_python), '-c', f'import {module}; print({module}.__version__)'],
            check=False
        )
        if success:
            log(f"{module}: OK")
        else:
            log(f"{module}: Error", 'WARNING')
            all_ok = False
    
    return all_ok


def setup_directories():
    """Crea directorios necesarios."""
    dirs = ['data', 'models', 'workspace']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
        log(f"Directorio creado: {d}/")


def main():
    parser = argparse.ArgumentParser(
        description='DeepFaceLive - Script de Instalación',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-v', '--venv', default='deepfacelive_env',
                        help='Nombre del entorno virtual (default: deepfacelive_env)')
    parser.add_argument('-c', '--cpu-only', action='store_true',
                        help='Instalar versión CPU (sin GPU NVIDIA)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Forzar reinstalación')
    parser.add_argument('--skip-ffmpeg', action='store_true',
                        help='Omitir instalación de FFmpeg')
    
    args = parser.parse_args()
    
    print("")
    print("=" * 60)
    print("   DeepFaceLive - Script de Instalación Profesional")
    print("=" * 60)
    print("")
    
    check_requirements()
    
    if not args.skip_ffmpeg:
        install_ffmpeg()
    
    create_virtualenv(args.venv)
    install_dependencies(args.venv, cpu_only=args.cpu_only)
    setup_directories()
    verify_installation(args.venv)
    
    print("")
    print("=" * 60)
    print("✓ Instalación completada!")
    print("=" * 60)
    print("")
    print("SIGUIENTES PASOS:")
    print("")
    if sys.platform == 'win32':
        print(f"1. Activar entorno:   {args.venv}\\Scripts\\activate")
    else:
        print(f"1. Activar entorno:   source {args.venv}/bin/activate")
    print("")
    print("2. Ejecutar aplicación:")
    print("   python main.py run DeepFaceLive --userdata-dir ./data")
    print("")
    print("3. Sin GPU, usar:")
    print("   python main.py run DeepFaceLive --userdata-dir ./data --no-cuda")
    print("")


if __name__ == '__main__':
    main()