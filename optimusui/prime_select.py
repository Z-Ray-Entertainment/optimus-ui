import subprocess
from enum import Enum

from optimusui import const
from optimusui.const import PRIME_PATHS, is_flatpak

prime_path = ""


class PrimeMode(Enum):
    NVIDIA = 0
    OFFLOAD = 1
    INTEGRATED = 2
    NO_DRIVER = 3


def prime_select(mode: PrimeMode):
    _prime_select(mode, False)


def prime_boot(mode: PrimeMode):
    _prime_select(mode, True)


def get_current():
    prime_command = [prime_path, "get-current"]
    if is_flatpak():
        prime_command = ["flatpak-spawn", "--host"] + prime_command
    prime_result = subprocess.run(prime_command, stdout=subprocess.PIPE)
    prime_time = prime_result.stdout.decode("utf-8").rstrip().split("\n")
    driver = prime_time[0].split(":")
    print(driver)
    return _text_to_prime_mode(driver[1].strip())


def has_prime_select():
    global prime_path
    for cur_path in PRIME_PATHS:
        which_cmd = ["test", "-f", cur_path]
        if const.is_flatpak():
            which_cmd = ["flatpak-spawn", "--host"] + which_cmd
        which_result = subprocess.run(which_cmd, stdout=subprocess.PIPE)
        if which_result.returncode == 0:
            prime_path = cur_path
            print("Which found at: " + cur_path)
            return True
    print("prime-select not found. Searched at: " + str(PRIME_PATHS))
    return False


def has_bbswitch():
    lsmod_cmd = ["lsmod"]
    if const.is_flatpak():
        lsmod_cmd = ["flatpak-spawn", "--host"] + lsmod_cmd
    bbswtich_result = subprocess.run(lsmod_cmd, stdout=subprocess.PIPE)
    all_mods = bbswtich_result.stdout.decode("utf-8").rstrip().split("\n")
    for mod in all_mods:
        clean_mod = " ".join(mod.split()).split(" ")
        if clean_mod[0] == "bbswitch":
            return True
    return False


def _prime_select(mode: PrimeMode, boot: bool):
    prime_command = ["pkexec", prime_path]
    if boot:
        prime_command += ["boot"]
    if is_flatpak():
        prime_command = ["flatpak-spawn", "--host"] + prime_command

    # TODO: Add handling for "amd" and "intel2"
    match mode:
        case PrimeMode.NVIDIA:
            prime_command += ["nvidia"]
        case PrimeMode.OFFLOAD:
            prime_command += ["offload"]
        case PrimeMode.INTEGRATED:
            prime_command += ["intel"]
    prime_result = subprocess.run(prime_command, stdout=subprocess.PIPE)
    if prime_result.returncode == 0:
        pass
    else:
        pass


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
