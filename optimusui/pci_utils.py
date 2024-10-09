import os
import subprocess

from optimusui import const
from optimusui.const import PCI_DEVICE_PATH, DEVICE_CLASS_GPU, NVIDIA_VENDOR_ID


def has_nvidia_gpu():
    return len(find_nvidia_gpu()) > 0


def find_nvidia_gpu():
    nvidia_gpus = []
    for subdir, dirs, files in os.walk(PCI_DEVICE_PATH):
        for device in dirs:
            device_properties = _build_device_properties(_get_device_info(device))
            if device_properties.is_nvidia_device() and device_properties.is_gpu():
                nvidia_gpus.append(device_properties)
    return nvidia_gpus


def find_all_gpus():
    all_gpus = []
    for subdir, dirs, files in os.walk(PCI_DEVICE_PATH):
        for device in dirs:
            device_properties = _build_device_properties(_get_device_info(device))
            if device_properties.is_gpu():
                all_gpus.append(device_properties)
    return all_gpus


def _get_device_info(device):
    device_uevent_result = subprocess.run(["cat", PCI_DEVICE_PATH + device + "/uevent"], stdout=subprocess.PIPE)
    return device_uevent_result.stdout.decode("utf-8").rstrip().split("\n")


def _build_device_properties(device_info):
    pci_class: str
    device_id: str
    vendor_id: str
    pci_slot: str
    for properties in device_info:
        prop = properties.split("=")
        match prop[0]:
            case "PCI_CLASS":
                pci_class = prop[1]
            case "PCI_ID":
                pci_id = prop[1].split(":")
                vendor_id = pci_id[0]
                device_id = pci_id[1]
            case "PCI_SLOT_NAME":
                pci_slot = prop[1]
    return DeviceProperties(pci_class, device_id, vendor_id, pci_slot)


class DeviceProperties:
    def __init__(self, pci_class, device_id, vendor_id, pci_slot):
        self.pci_class = pci_class
        self.device_id = device_id
        self.vendor_id = vendor_id
        self.pci_slot = pci_slot

    def is_nvidia_device(self):
        return self.vendor_id == const.NVIDIA_VENDOR_ID

    def is_gpu(self):
        return self.pci_class in const.DEVICE_CLASS_GPU

    def resolve_device_name(self):
        pci_look_up = self.vendor_id + ":" + self.device_id
        device_lspci_result = subprocess.run(["lspci", "-d", pci_look_up], stdout=subprocess.PIPE)
        lspci = device_lspci_result.stdout.decode("utf-8").rstrip().split(":")
        return lspci[len(lspci) - 1].strip()

    def resolve_device_architecture(self):
        pass
