#!/usr/bin/env python3
import sys
from os import environ

'''
Init wrapper to ensure this app works in and outside flatpak
'''

pkgdatadir = '@pkgdatadir@'

# Can not use is_flatpak from os_uitls as it will not be accessible without the next two lines
if environ.get("FLATPAK_ID") is not None:
    sys.path.insert(1, pkgdatadir)

from optimusui import const, system_validator
from optimusui.optimus_ui import OptimusUI

if __name__ == '__main__':
    if system_validator.is_system_using_nouveau():
        pass
    elif system_validator.is_prime_supported():
        OptimusUI(application_id=const.APP_ID).run(sys.argv)
