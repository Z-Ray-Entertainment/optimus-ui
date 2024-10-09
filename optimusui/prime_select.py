from enum import Enum

from optimusui import const, os_utils

prime_path = ""


class PrimeMode(Enum):
    NVIDIA = 0
    OFFLOAD = 1
    INTEGRATED = 2
    NO_DRIVER = 3


def get_boot():
    prime_command = [prime_path, "get-boot"]
    prime_result = os_utils.run_command(prime_command)
    prime_time = prime_result.stdout.decode("utf-8").rstrip()
    driver = prime_time.split(":")
    return _text_to_prime_mode(driver[1].strip())


def get_current():
    prime_time = _get_current().split("\n")
    driver = prime_time[0].split(":")
    if len(driver) < 2:
        return PrimeMode.NO_DRIVER
    return _text_to_prime_mode(driver[1].strip())


def is_device_on(bus_id):
    power_command = ["cat", const.PCI_DEVICE_PATH + bus_id + "/power_state"]
    power_result = os_utils.run_command(power_command)
    d3_state = power_result.stdout.decode("utf-8").rstrip()
    print(d3_state)
    return d3_state != "D3cold"


def has_prime_select():
    global prime_path
    for cur_path in const.PRIME_PATHS:
        which_cmd = ["test", "-f", cur_path]
        which_result = os_utils.run_command(which_cmd)
        if which_result.returncode == 0:
            prime_path = cur_path
            return True
    return False


def has_bbswitch():
    lsmod_cmd = ["lsmod"]
    bbswtich_result = os_utils.run_command(lsmod_cmd)
    all_mods = bbswtich_result.stdout.decode("utf-8").rstrip().split("\n")
    for mod in all_mods:
        clean_mod = " ".join(mod.split()).split(" ")
        if clean_mod[0] == "bbswitch":
            return True
    return False


def prime_select(mode: PrimeMode, boot: bool):
    prime_command = ["pkexec", prime_path]
    if boot:
        prime_command += ["boot"]

    # TODO: Add handling for "amd" and "intel2"
    match mode:
        case PrimeMode.NVIDIA:
            prime_command += ["nvidia"]
        case PrimeMode.OFFLOAD:
            prime_command += ["offload"]
        case PrimeMode.INTEGRATED:
            prime_command += ["intel"]
    prime_result = os_utils.run_command(prime_command)
    return prime_result.returncode == 0


def _get_current():
    prime_command = [prime_path, "get-current"]
    prime_result = os_utils.run_command(prime_command)
    return prime_result.stdout.decode("utf-8").rstrip()


def _text_to_prime_mode(text: str) -> PrimeMode:
    match text:
        case "intel" | "intel2" | "amd":
            return PrimeMode.INTEGRATED
        case "nvidia":
            return PrimeMode.NVIDIA
        case "offload":
            return PrimeMode.OFFLOAD
        case _:
            return PrimeMode.NO_DRIVER
