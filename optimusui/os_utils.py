import subprocess
from os import environ

'''
Various OS and flatpak related utilities
'''

FLATPAK_SPAWN = ["flatpak-spawn", "--host"]


def is_flatpak() -> bool:
    return environ.get("FLATPAK_ID") is not None


def run_command(base_command: []):
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command, stdout=subprocess.PIPE)
    return subprocess.run(base_command, stdout=subprocess.PIPE)
