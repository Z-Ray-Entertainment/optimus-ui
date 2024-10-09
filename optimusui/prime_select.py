import subprocess
from enum import Enum

from optimusui import const
from optimusui.const import PRIME_PATHS


class PrimeMode(Enum):
    NVIDIA = 0
    OFFLOAD = 1
    INTEGRATED = 2
    NO_DRIVER = 3


def prime_select(mode: PrimeMode):
    pass


def prime_boot(mode: PrimeMode):
    pass


def get_current():
    get_currend_cmd = ["pkexec", "prime-select", "get-current"]
    if const.is_flatpak():
        get_currend_cmd = ["flatpak-spawn", "--host"] + get_currend_cmd
    device_uevent_result = subprocess.run(get_currend_cmd, stdout=subprocess.PIPE)
    return device_uevent_result.stdout.decode("utf-8").rstrip().split("\n")


def has_prime_select():
    for cur_path in PRIME_PATHS:
        which_cmd = ["test", "-f", cur_path]
        if const.is_flatpak():
            which_cmd = ["flatpak-spawn", "--host"] + which_cmd
        which_result = subprocess.run(which_cmd, stdout=subprocess.PIPE)
        if which_result.returncode == 0:
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
