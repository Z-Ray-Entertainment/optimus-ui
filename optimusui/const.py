from os import environ

if environ.get("FLATPAK_ID") is not None:
    VERSION = "@VERSION@"
    LOCALE_DIR = "@localedir@"
else:
    VERSION = "0.dev0"
    LOCALE_DIR = "optimusui/data/po"
APP_NAME = "OptimusUI"
APP_ID = "de.z_ray.OptimusUI"

NVIDIA_VENDOR_ID = "10DE"
DEVICE_CLASS_GPU = "30000" "30200"  # "desktop_gpu" "mobile_gpu"
DRIVER_ID = "nvidia"
PCI_DEVICE_PATH = "/sys/bus/pci/devices/"

PRIME_BIN = "prime-select"
PRIME_PATHS = [
    "/usr/bin/" + PRIME_BIN,
    "/usr/sbin/" + PRIME_BIN,
    "/bin/" + PRIME_BIN,
    "/sbin/" + PRIME_BIN
]

def is_flatpak() -> bool:
    return environ.get("FLATPAK_ID") is not None