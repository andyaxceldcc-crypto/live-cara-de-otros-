"""
Módulo de sesión de inferencia ONNX Runtime.
Proporciona funcionalidad para cargar y ejecutar modelos ONNX en diferentes dispositivos.
"""

import onnx
import onnxruntime as rt
from io import BytesIO
from .device import ORTDeviceInfo


def InferenceSession_with_device(onnx_model_or_path, device_info: ORTDeviceInfo):
    """
    Construye una sesión de inferencia ONNX Runtime para el dispositivo especificado.

    Args:
        onnx_model_or_path: Modelo ONNX (ModelProto) o ruta al archivo del modelo.
        device_info: Información del dispositivo de ejecución.

    Returns:
        Una instancia de onnxruntime.InferenceSession configurada para el dispositivo.

    Raises:
        Exception: Si el proveedor de ejecución no está disponible.
    """

    # Si es un modelo ONNX, convertir a bytes
    if isinstance(onnx_model_or_path, onnx.ModelProto):
        buffer = BytesIO()
        onnx.save(onnx_model_or_path, buffer)
        onnx_model_or_path = buffer.getvalue()

    # Verificar que el proveedor de ejecución esté disponible
    device_ep = device_info.get_execution_provider()
    if device_ep not in rt.get_available_providers():
        raise Exception(f'{device_ep} no está disponible en onnxruntime')

    # Configurar opciones del dispositivo
    ep_flags = {}
    if device_ep in ['CUDAExecutionProvider', 'DmlExecutionProvider']:
        ep_flags['device_id'] = device_info.get_index()

    # Configurar opciones de la sesión
    sess_options = rt.SessionOptions()
    sess_options.log_severity_level = 4
    sess_options.log_verbosity_level = -1
    
    # Configuraciones específicas para DirectML
    if device_ep == 'DmlExecutionProvider':
        sess_options.enable_mem_pattern = False
    
    # Crear y devolver la sesión de inferencia
    sess = rt.InferenceSession(
        onnx_model_or_path,
        providers=[(device_ep, ep_flags)],
        sess_options=sess_options
    )
    return sess
