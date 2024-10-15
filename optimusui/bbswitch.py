"""
Helper file to work with bbswitch
"""
from optimusui import os_utils


def has_bbswitch():
    loaded_mods = ["cat", "/proc/modules"]
    loaded_mods_result = os_utils.run_command(loaded_mods)
    all_mods = loaded_mods_result.stdout.decode("utf-8").rstrip().split("\n")
    for mod in all_mods:
        clean_mod = mod.split(" ")
        if clean_mod[0] == "bbswitch":
            return True
    return False
