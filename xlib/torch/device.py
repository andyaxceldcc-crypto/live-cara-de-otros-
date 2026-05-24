"""
Módulo de dispositivo para PyTorch.
Proporciona información sobre dispositivos GPU/CPU disponibles para entrenamiento.
"""

from typing import List, Union

import torch


class TorchDeviceInfo:
    """
    Representa información serializable del dispositivo PyTorch.
    Contiene datos como índice, nombre y memoria total de la GPU.
    """

    def __init__(self, index=None, name=None, total_memory=None):
        self._index: int = index
        self._name: str = name
        self._total_memory: int = total_memory

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

    def get_name(self) -> str:
        """Obtiene el nombre del dispositivo."""
        if self.is_cpu():
            return 'CPU'
        return self._name

    def get_total_memory(self) -> int:
        """Obtiene la memoria total del dispositivo en bytes."""
        if self.is_cpu():
            return 0
        return self._total_memory

    def __eq__(self, other):
        """Compara dispositivos por índice."""
        if self is not None and other is not None and isinstance(self, TorchDeviceInfo) and isinstance(other, TorchDeviceInfo):
            return self._index == other._index
        return False

    def __hash__(self):
        """Genera hash basado en el índice del dispositivo."""
        return self._index

    def __str__(self):
        """Representación en string del dispositivo."""
        if self.is_cpu():
            return "CPU"
        else:
            return f"[{self._index}] {self._name} [{(self._total_memory / 1024**3):.3}Gb]"

    def __repr__(self):
        return f'{self.__class__.__name__} object: ' + self.__str__()


_torch_devices = None


def get_cpu_device_info() -> TorchDeviceInfo:
    """Obtiene información del dispositivo CPU."""
    return TorchDeviceInfo(index=-1)


def get_device_info_by_index(index: int) -> Union[TorchDeviceInfo, None]:
    """
    Obtiene información del dispositivo por su índice.

    Args:
        index: Índice del dispositivo (-1 para CPU).

    Returns:
        TorchDeviceInfo o None si no se encuentra.
    """
    if index == -1:
        return get_cpu_device_info()
    for device in get_available_devices_info(include_cpu=False):
        if device.get_index() == index:
            return device
    return None


def get_device(device_info: TorchDeviceInfo) -> torch.device:
    """
    Obtiene el dispositivo físico torch desde TorchDeviceInfo.

    Args:
        device_info: Información del dispositivo.

    Returns:
        Dispositivo torch (cpu o cuda).
    """
    if device_info.is_cpu():
        return torch.device('cpu')
    return torch.device(f'cuda:{device_info.get_index()}')


def get_available_devices_info(include_cpu=True, cpu_only=False) -> List[TorchDeviceInfo]:
    """
    Retorna una lista de información de dispositivos PyTorch disponibles.

    Args:
        include_cpu: Incluir CPU en la lista de dispositivos.
        cpu_only: Retornar solo CPU.

    Returns:
        Lista de TorchDeviceInfo disponibles.
    """
    devices = []
    if not cpu_only:
        global _torch_devices
        if _torch_devices is None:
            _torch_devices = []
            for i in range(torch.cuda.device_count()):
                device_props = torch.cuda.get_device_properties(i)
                _torch_devices.append(
                    TorchDeviceInfo(
                        index=i,
                        name=device_props.name,
                        total_memory=device_props.total_memory
                    )
                )
        devices += _torch_devices

    if include_cpu:
        devices.append(get_cpu_device_info())

    return devices

