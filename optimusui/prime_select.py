from enum import Enum

from optimusui import const, os_utils

'''
Prime Select wrapper
'''

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
    match os_utils.get_distro():
        case os_utils.Distribution.SUSE:
            prime_time = _get_current().split("\n")
            if len(prime_time) < 2:
                return PrimeMode.NO_DRIVER
            driver = prime_time[0].split(":")
            return _text_to_prime_mode(driver[1].strip())
        case os_utils.Distribution.UBUNTU:
            prime_time = _get_current()
            return _text_to_prime_mode(prime_time)
    return PrimeMode.NO_DRIVER


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
    loaded_mods = ["cat", "/proc/modules"]
    loaded_mods_result = os_utils.run_command(loaded_mods)
    all_mods = loaded_mods_result.stdout.decode("utf-8").rstrip().split("\n")
    for mod in all_mods:
        clean_mod = mod.split(" ")
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
            match os_utils.get_distro():
                case os_utils.Distribution.SUSE:
                    prime_command += ["offload"]
                case os_utils.Distribution.UBUNTU:
                    prime_command += ["on-demand"]
                case os_utils.Distribution.UNKNOWN:
                    prime_command += ["offload"]
        case PrimeMode.INTEGRATED:
            prime_command += ["intel"]
    os_utils.run_command_no_pipe(prime_command)
    return True


def _get_current():
    prime_command = [prime_path]
    match os_utils.get_distro():
        case os_utils.Distribution.UBUNTU:
            prime_command += ["query"]
        case os_utils.Distribution.SUSE:
            prime_command += ["get-current"]
    prime_result = os_utils.run_command(prime_command)
    return prime_result.stdout.decode("utf-8").rstrip()


def _text_to_prime_mode(text: str) -> PrimeMode:
    match text:
        case "intel" | "intel2" | "amd":
            return PrimeMode.INTEGRATED
        case "nvidia":
            return PrimeMode.NVIDIA
        case "offload" | "on-demand":
            return PrimeMode.OFFLOAD
        case _:
            return PrimeMode.NO_DRIVER
