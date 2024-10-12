import subprocess
from os import environ

'''
Various OS and flatpak related utilities
'''

FLATPAK_SPAWN = ["flatpak-spawn", "--host"]

'''
Test if the app is running as  flatpak
'''
def is_flatpak() -> bool:
    return environ.get("FLATPAK_ID") is not None

'''
Runs a command as a subprocess but does not return the result and does not
wait for the command to finish. Useful for running binaries which do not terminate
'''
def run_command_no_pipe(base_command: []):
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command)
    return subprocess.run(base_command)

'''
Runs a given array as a subprocess and returns the result.
If the app is running inside flatpak it will use flatpak-spawn
'''
def run_command(base_command: []):
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command, stdout=subprocess.PIPE)
    return subprocess.run(base_command, stdout=subprocess.PIPE)
