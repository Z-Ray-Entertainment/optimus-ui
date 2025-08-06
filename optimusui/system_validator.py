from optimusui import prime_select, pci_utils, os_utils

def is_system_using_nouveau() -> bool:
    driver = os_utils.get_gpu_driver()
    match driver:
        case "nouveau":
            return True
    return False


def is_prime_supported() -> bool:
    has_prime_select = prime_select.has_prime_select()
    has_nvidia_gpu = pci_utils.has_nvidia_gpu()
    has_nvidia_driver = not is_system_using_nouveau()

    return has_prime_select and has_nvidia_gpu and has_nvidia_driver
