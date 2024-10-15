"""
Helper file to work with bbswitch
"""
from enum import Enum

from optimusui import os_utils


class PowerState(Enum):
    ON = "ON"
    OFF = "OFF"


def force_power_state(power_on: bool):
    power_cmd = ["echo"]
    if power_on:
        power_cmd += [PowerState.ON.value]
    else:
        power_cmd += [PowerState.OFF.value]
    power_cmd += [">", "/proc/acpi/bbswitch"]
    os_utils.run_command_as_root(power_cmd)

def has_bbswitch():
    loaded_mods = ["cat", "/proc/modules"]
    loaded_mods_result = os_utils.run_command(loaded_mods)
    all_mods = loaded_mods_result.stdout.decode("utf-8").rstrip().split("\n")
    for mod in all_mods:
        clean_mod = mod.split(" ")
        if clean_mod[0] == "bbswitch":
            return True
    return False
