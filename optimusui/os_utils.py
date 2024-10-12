import subprocess
from os import environ

'''
Various OS and flatpak related utilities
'''

FLATPAK_SPAWN = ["flatpak-spawn", "--host"]

def is_flatpak() -> bool:
    """
    Test if the app is running as  flatpak
    """
    return environ.get("FLATPAK_ID") is not None


def run_command_no_pipe(base_command: []):
    """
    Runs a command as a subprocess but does not return the result and does not
    wait for the command to finish. Useful for running binaries which do not terminate
    """
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command)
    return subprocess.run(base_command)


def run_command(base_command: []):
    """
    Runs a given array as a subprocess and returns the result.
    If the app is running inside flatpak it will use flatpak-spawn
    """
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command, stdout=subprocess.PIPE)
    return subprocess.run(base_command, stdout=subprocess.PIPE)
