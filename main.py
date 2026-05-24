"""
DeepFaceLive - Aplicación de Intercambio de Caras en Tiempo Real
Autor: iperov
Traducción: Agente AI

Este programa permite intercambiacar caras en tiempo real desde una webcam
o desde un archivo de video usando modelos de caras entrenados o fotos únicas.
"""

import argparse
import os
import platform
from pathlib import Path

from xlib import appargs as lib_appargs
from xlib import os as lib_os


def main():
    """Función principal que configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='DeepFaceLive - Intercambio de caras en tiempo real'
    )
    subparsers = parser.add_subparsers()

    # Parser para ejecutar la aplicación
    run_parser = subparsers.add_parser(
        "run",
        help="Ejecutar la aplicación."
    )
    run_subparsers = run_parser.add_subparsers()

    def run_DeepFaceLive(args):
        """Ejecuta la aplicación principal DeepFaceLive."""
        userdata_path = Path(args.userdata_dir)
        lib_appargs.set_arg_bool('NO_CUDA', args.no_cuda)

        print('Ejecutando DeepFaceLive.')
        from apps.DeepFaceLive.DeepFaceLiveApp import DeepFaceLiveApp
        DeepFaceLiveApp(userdata_path=userdata_path).run()

    p = run_subparsers.add_parser(
        'DeepFaceLive',
        help='Aplicación principal de intercambio de caras'
    )
    p.add_argument(
        '--userdata-dir',
        default=None,
        action=fixPathAction,
        help="Directorio de datos del usuario."
    )
    p.add_argument(
        '--no-cuda',
        action="store_true",
        default=False,
        help="Desactivar CUDA (usar solo CPU)."
    )
    p.set_defaults(func=run_DeepFaceLive)

    # Parser para herramientas de desarrollo
    dev_parser = subparsers.add_parser(
        "dev",
        help="Herramientas de desarrollo."
    )
    dev_subparsers = dev_parser.add_subparsers()

    def run_split_large_files(args):
        """Divide archivos grandes en partes."""
        from scripts import dev
        dev.split_large_files()

    p = dev_subparsers.add_parser(
        'split_large_files',
        help='Dividir archivos grandes en partes'
    )
    p.set_defaults(func=run_split_large_files)

    def run_merge_large_files(args):
        """Une archivos grandes desde partes."""
        from scripts import dev
        dev.merge_large_files(delete_parts=args.delete_parts)

    p = dev_subparsers.add_parser(
        'merge_large_files',
        help='Unir archivos grandes desde partes'
    )
    p.add_argument(
        '--delete-parts',
        action="store_true",
        default=False,
        help="Eliminar las partes después de unir."
    )
    p.set_defaults(func=run_merge_large_files)

    def run_extract_FaceSynthetics(args):
        """Extrae caras del dataset FaceSynthetics."""
        from scripts import dev

        inputdir_path = Path(args.input_dir)
        faceset_path = Path(args.faceset_path)

        dev.extract_FaceSynthetics(inputdir_path, faceset_path)

    p = dev_subparsers.add_parser(
        'extract_FaceSynthetics',
        help='Extraer caras del dataset FaceSynthetics'
    )
    p.add_argument(
        '--input-dir',
        default=None,
        action=fixPathAction,
        help="Directorio de FaceSynthetics."
    )
    p.add_argument(
        '--faceset-path',
        default=None,
        action=fixPathAction,
        help="Ruta de salida del archivo .dfs"
    )
    p.set_defaults(func=run_extract_FaceSynthetics)

    # Parser para entrenar modelos
    train_parser = subparsers.add_parser(
        "train",
        help="Entrenar redes neuronales."
    )
    train_parsers = train_parser.add_subparsers()

    def train_FaceAligner(args):
        """Entrena el modelo FaceAligner para alinear caras."""
        lib_os.set_process_priority(lib_os.ProcessPriority.IDLE)
        from apps.trainers.FaceAligner.FaceAlignerTrainerApp import FaceAlignerTrainerApp
        FaceAlignerTrainerApp(
            workspace_path=Path(args.workspace_dir),
            faceset_path=Path(args.faceset_path)
        )

    p = train_parsers.add_parser(
        'FaceAligner',
        help='Entrenar modelo FaceAligner'
    )
    p.add_argument(
        '--workspace-dir',
        default=None,
        action=fixPathAction,
        help="Directorio de espacio de trabajo."
    )
    p.add_argument(
        '--faceset-path',
        default=None,
        action=fixPathAction,
        help="Ruta del archivo .dfs"
    )
    p.set_defaults(func=train_FaceAligner)

    def bad_args(arguments):
        """Muestra la ayuda cuando los argumentos son incorrectos."""
        parser.print_help()
        exit(0)
    parser.set_defaults(func=bad_args)

    args = parser.parse_args()
    args.func(args)


class fixPathAction(argparse.Action):
    """Action personalizada para convertir rutas relativas a absolutas."""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


if __name__ == '__main__':
    main()
