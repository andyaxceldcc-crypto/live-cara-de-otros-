"""
Módulo de dispositivo para ONNX Runtime.
Proporciona información sobre dispositivos GPU/CPU disponibles para inferencia.
"""

import ctypes
import itertools
import os
from typing import List

import onnxruntime as rt

from .. import appargs as lib_appargs


class ORTDeviceInfo:
    """
    Representa información serializable del dispositivo ONNX Runtime.
    Contiene datos como índice, proveedor de ejecución, nombre y memoria.
    """

    def __init__(self, index=None, execution_provider=None, name=None, total_memory=None, free_memory=None):
        self._index: int = index
        self._execution_provider: str = execution_provider
        self._name: str = name
        self._total_memory: int = total_memory
        self._free_memory: int = free_memory

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, d):
        self.__init__()
        self.__dict__.update(d)

    def is_cpu(self) -> bool:
        """Indica si el dispositivo es CPU."""
        return self._index == -1

    def get_index(self) -> int:
        """Obtiene el índice del dispositivo."""
        return self._index

    def get_execution_provider(self) -> str:
        """Obtiene el nombre del proveedor de ejecución (CUDA, CPU, etc.)."""
        return self._execution_provider

    def get_name(self) -> str:
        """Obtiene el nombre del dispositivo."""
        return self._name

    def get_total_memory(self) -> int:
        """Obtiene la memoria total del dispositivo en bytes."""
        return self._total_memory

    def get_free_memory(self) -> int:
        """Obtiene la memoria libre del dispositivo en bytes."""
        return self._free_memory

    def __eq__(self, other):
        """Compara dispositivos por índice."""
        if self is not None and other is not None and isinstance(self, ORTDeviceInfo) and isinstance(other, ORTDeviceInfo):
            return self._index == other._index
        return False

    def __hash__(self):
        """Genera hash basado en el índice del dispositivo."""
        return self._index

    def __str__(self):
        """Representación en string del dispositivo."""
        if self.is_cpu():
            return f"CPU"
        else:
            ep = self.get_execution_provider()
            if ep == 'CUDAExecutionProvider':
                return f"[{self._index}] {self._name} [{(self._total_memory / 1024**3):.3}Gb] [CUDA]"
            elif ep == 'DmlExecutionProvider':
                return f"[{self._index}] {self._name} [{(self._total_memory / 1024**3):.3}Gb] [DirectX12]"

    def __repr__(self):
        return f'{self.__class__.__name__} object: ' + self.__str__()


_ort_devices_info = None


def get_cpu_device_info() -> ORTDeviceInfo:
    """Obtiene información del dispositivo CPU."""
    return ORTDeviceInfo(
        index=-1,
        execution_provider='CPUExecutionProvider',
        name='CPU',
        total_memory=0,
        free_memory=0
    )


def get_available_devices_info(include_cpu=True, cpu_only=False) -> List[ORTDeviceInfo]:
    """
    Retorna una lista de información de dispositivos ORT disponibles.

    Args:
        include_cpu: Incluir CPU en la lista de dispositivos.
        cpu_only: Retornar solo CPU.

    Returns:
        Lista de ORTDeviceInfo disponibles.
    """
    devices = []
    if not cpu_only:
        global _ort_devices_info
        if _ort_devices_info is None:
            _initialize_ort_devices_info()
            _ort_devices_info = []
            for i in range(int(os.environ.get('ORT_DEVICES_COUNT', 0))):
                _ort_devices_info.append(
                    ORTDeviceInfo(
                        index=int(os.environ[f'ORT_DEVICE_{i}_INDEX']),
                        execution_provider=os.environ[f'ORT_DEVICE_{i}_EP'],
                        name=os.environ[f'ORT_DEVICE_{i}_NAME'],
                        total_memory=int(os.environ[f'ORT_DEVICE_{i}_TOTAL_MEM']),
                        free_memory=int(os.environ[f'ORT_DEVICE_{i}_FREE_MEM']),
                    )
                )
        devices += _ort_devices_info
    if include_cpu:
        devices.append(get_cpu_device_info())

    return devices


def _initialize_ort_devices_info():
    """
    Determina los dispositivos ORT disponibles y coloca su información en os.environ,
    para que esté disponible en subprocesos generados.

    Usa solo ctypes de Python y la biblioteca predeterminada proporcionada con los drivers NVIDIA.
    """
    if int(os.environ.get('ORT_DEVICES_INITIALIZED', 0)) == 0:
        os.environ['ORT_DEVICES_INITIALIZED'] = '1'
        os.environ['ORT_DEVICES_COUNT'] = '0'

        devices = []
        prs = rt.get_available_providers()
        
        # Inicializar dispositivos CUDA si está disponible
        if not lib_appargs.get_arg_bool('NO_CUDA') and 'CUDAExecutionProvider' in prs:
            os.environ['CUDA​CACHE_​MAXSIZE'] = '2147483647'
            try:
                libnames = ('libcuda.so', 'libcuda.dylib', 'nvcuda.dll')
                for libname in libnames:
                    try:
                        cuda = ctypes.CDLL(libname)
                    except Exception:
                        continue
                    else:
                        break
                else:
                    return

                nGpus = ctypes.c_int()
                name = b' ' * 200
                cc_major = ctypes.c_int()
                cc_minor = ctypes.c_int()
                freeMem = ctypes.c_size_t()
                totalMem = ctypes.c_size_t()
                device = ctypes.c_int()
                context = ctypes.c_void_p()

                if cuda.cuInit(0) == 0 and \
                        cuda.cuDeviceGetCount(ctypes.byref(nGpus)) == 0:
                    for i in range(nGpus.value):
                        if cuda.cuDeviceGet(ctypes.byref(device), i) != 0 or \
                                cuda.cuDeviceGetName(ctypes.c_char_p(name), len(name), device) != 0 or \
                                cuda.cuDeviceComputeCapability(ctypes.byref(cc_major), ctypes.byref(cc_minor), device) != 0:
                            continue

                        if cuda.cuCtxCreate_v2(ctypes.byref(context), 0, device) == 0:
                            if cuda.cuMemGetInfo_v2(ctypes.byref(freeMem), ctypes.byref(totalMem)) == 0:
                                devices.append({
                                    'index': i,
                                    'execution_provider': 'CUDAExecutionProvider',
                                    'name': name.split(b'\0', 1)[0].decode(),
                                    'total_mem': totalMem.value,
                                    'free_mem': freeMem.value,
                                })
                            cuda.cuCtxDetach(context)
            except Exception as e:
                print(f'Error en la inicialización de dispositivos CUDA: {e}')

        # Inicializar dispositivos DirectML (Windows)
        if 'DmlExecutionProvider' in prs:
            # onnxruntime-directml no tiene API de enumeración de dispositivos para usuarios.
            # Por lo tanto, el código debe seguir la misma lógica que en el código fuente de Microsoft.
            
            from xlib.api.win32 import dxgi as lib_dxgi

            dxgi_factory = lib_dxgi.create_DXGIFactory4()
            if dxgi_factory is not None:
                for i in itertools.count():
                    adapter = dxgi_factory.enum_adapters1(i)
                    if adapter is not None:
                        desc = adapter.get_desc1()
                        if desc.Flags != lib_dxgi.DXGI_ADAPTER_FLAG.DXGI_ADAPTER_FLAG_SOFTWARE and \
                                not (desc.VendorId == 0x1414 and desc.DeviceId == 0x8c):
                            devices.append({
                                'index': i,
                                'execution_provider': 'DmlExecutionProvider',
                                'name': desc.Description,
                                'total_mem': desc.DedicatedVideoMemory,
                                'free_mem': desc.DedicatedVideoMemory,
                            })
                        adapter.Release()
                    else:
                        break
                dxgi_factory.Release()

        # Guardar información de dispositivos en el entorno
        os.environ['ORT_DEVICES_COUNT'] = str(len(devices))
        for i, device in enumerate(devices):
            os.environ[f'ORT_DEVICE_{i}_INDEX'] = str(device['index'])
            os.environ[f'ORT_DEVICE_{i}_EP'] = device['execution_provider']
            os.environ[f'ORT_DEVICE_{i}_NAME'] = device['name']
            os.environ[f'ORT_DEVICE_{i}_TOTAL_MEM'] = str(device['total_mem'])
            os.environ[f'ORT_DEVICE_{i}_FREE_MEM'] = str(device['free_mem'])


_initialize_ort_devices_info()
