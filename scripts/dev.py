"""
Script de herramientas de desarrollo para DeepFaceLive.
Proporciona funciones para dividir/fundir archivos grandes y extraer datasets.
"""

from pathlib import Path

import numpy as np
from xlib import console as lib_con
from xlib import face as lib_face
from xlib import path as lib_path
from xlib.file import SplittedFile
from xlib import cv as lib_cv


# Raíz del repositorio
repo_root = Path(__file__).parent.parent

# Lista de archivos grandes que pueden estar divididos
large_files_list = [
    (repo_root / 'modelhub' / 'onnx' / 'S3FD' / 'S3FD.onnx', 48*1024*1024),
    (repo_root / 'modelhub' / 'onnx' / 'LIA' / 'generator.onnx', 48*1024*1024),
    (repo_root / 'modelhub' / 'onnx' / 'InsightFaceSwap' / 'inswapper_128.onnx', 48*1024*1024),
    (repo_root / 'modelhub' / 'onnx' / 'InsightFaceSwap' / 'w600k_r50.onnx', 48*1024*1024),
    (repo_root / 'modelhub' / 'torch' / 'S3FD' / 'S3FD.pth', 48*1024*1024),
    (repo_root / 'modelhub' / 'cv' / 'FaceMarkerLBF' / 'lbfmodel.yaml', 34*1024*1024),
]


def merge_large_files(delete_parts=False):
    """
    Une archivos grandes que fueron previamente divididos.

    Args:
        delete_parts: Si True, elimina las partes después de unir.
    """
    for filepath, _ in large_files_list:
        print(f'Uniendo {filepath}...')
        SplittedFile.merge(filepath, delete_parts=delete_parts)
    print('Completado')


def split_large_files(delete_original=False):
    """
    Divide archivos grandes en partes más pequeñas.

    Args:
        delete_original: Si True, elimina el archivo original después de dividir.
    """
    for filepath, part_size in large_files_list:
        print(f'Dividiendo {filepath}...')
        if filepath.exists():
            SplittedFile.split(filepath, part_size=part_size, delete_original=delete_original)
        else:
            print(f'{filepath} no encontrado. Omitiendo.')

    print('Completado')


def extract_FaceSynthetics(inputdir_path: Path, faceset_path: Path):
    """
    Extrae el dataset FaceSynthetics de Microsoft.

    Este dataset contiene caras sintéticas con landmarks faciales.
    Los landmarks están definidos por los códigos de segmento:

    Códigos de segmento:
        FONDO = 0
        PIEL = 1
        NARIZ = 2
        OJO_DERECHO = 3
        OJO_IZQUIERDO = 4
        CEJA_DERECHA = 5
        CEJA_IZQUIERDA = 6
        OREJA_DERECHA = 7
        OREJA_IZQUIERDA = 8
        INTERIOR_BOCA = 9
        LABIO_SUPERIOR = 10
        LABIO_INFERIOR = 11
        CUELLO = 12
        CABELLO = 13
        BARBA = 14
        ROPA = 15
        GAFAS = 16
        SOMBRERERO = 17
        PROTECTOR_FACIAL = 18
        IGNORAR = 255

    Args:
        inputdir_path: Ruta al directorio del dataset FaceSynthetics.
        faceset_path: Ruta de salida para el archivo .dfs.
    """
    # Verificar extensión del archivo de salida
    if faceset_path.suffix != '.dfs':
        raise ValueError('faceset_path debe tener extensión .dfs.')

    # Obtener lista de archivos en el directorio de entrada
    filepaths = lib_path.get_files_paths(inputdir_path)

    # Crear el faceset para escritura
    fs = lib_face.Faceset(faceset_path, write_access=True, recreate=True)

    # Procesar cada archivo
    for filepath in lib_con.progress_bar_iterator(filepaths, desc='Procesando'):
        if filepath.suffix == '.txt':
            # Construir ruta de la imagen correspondiente
            image_filepath = filepath.parent / f'{filepath.name.split("_")[0]}.png'
            if not image_filepath.exists():
                print(f'{image_filepath} no existe, omitiendo')
                continue

            # Leer imagen
            img = lib_cv.imread(image_filepath)
            H, W, C = img.shape

            # Extraer landmarks del archivo de texto
            lmrks = []
            for lmrk_line in filepath.read_text().split('\n'):
                if len(lmrk_line) == 0:
                    continue

                x, y = lmrk_line.split(' ')
                x, y = float(x), float(y)
                lmrks.append((x, y))

            # Convertir landmarks a formato normalizado y crear objeto FLandmarks2D
            lmrks = np.array(lmrks[:68], np.float32) / (H, W)
            flmrks = lib_face.FLandmarks2D.create(lib_face.ELandmarks2D.L68, lmrks)

            # Crear objeto UImage con la imagen
            uimg = lib_face.UImage()
            uimg.assign_image(img)
            uimg.set_name(image_filepath.stem)

            # Crear marcador de cara
            ufm = lib_face.UFaceMark()
            ufm.set_UImage_uuid(uimg.get_uuid())
            ufm.set_FRect(flmrks.get_FRect())
            ufm.add_FLandmarks2D(flmrks)

            # Agregar a la base de datos del faceset
            fs.add_UFaceMark(ufm)
            fs.add_UImage(uimg, format='png')

    # Optimizar y cerrar el faceset
    fs.optimize()
    fs.close()
