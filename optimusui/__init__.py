#!/usr/bin/env python3
import sys
from os import environ

pkgdatadir = '@pkgdatadir@'
if environ.get("FLATPAK_ID") is not None:
    sys.path.insert(1, pkgdatadir)
    print(pkgdatadir)

from optimusui import const
from optimusui.optimus_ui import OptimusUI

print("Booting up " + const.APP_NAME)

if __name__ == '__main__':
    OptimusUI(application_id=const.APP_ID).run(sys.argv)

print("\n")
