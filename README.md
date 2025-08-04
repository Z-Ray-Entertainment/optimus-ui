# OptimusUI

![OptimusUI Icon](https://codeberg.org/ZRayEntertainment/optimus-ui/raw/branch/main/optimusui/data/screenshots/icon_small.png)

OptimusUI is a graphical user interface for prime-select.  
It allows a Laptop or Desktop system with an integrated GPU and a dedicated GPU to switch between these two. By either
running entirely on the dGPU, the iGPU or using nVidia's Offloading technology.

![OptimusUI](https://codeberg.org/ZRayEntertainment/optimus-ui/raw/branch/main/optimusui/data/screenshots/optimus_ui.png)

## Requirements

This application aims to be as simple as possible. this also includes it's dependencies.  
But there are still various things which can not be distributed by this application.
The following needs to be present on the target system:

- proprietary nvidia driver version >= 390
- suse-prime or nvidia-prime
- bbswitch (Recommended but not required)

## Supported Prime Tools

- [SUSEPrime](https://github.com/openSUSE/SUSEPrime) (Tumbleweed, Leap, Aeon, Kalpa, Gecko Linux, Gecko Linux
  Rolling)
- [nvidia-prime](https://wiki.ubuntuusers.de/Hybrid-Grafikkarten/PRIME/) (Ubuntu, Xubuntu, Lubuntu, Linux Mint,
  Kubuntu, ZorinOS, VanillaOS ...)
- [fedora-prime-select](https://github.com/bosim/FedoraPrime/blob/master/fedora-prime-select) (Fedora, Nobara)
- [nvidia-prime-select](https://github.com/wildtruc/nvidia-prime-select) (Fedora, Arch Linux, ChimeraOS, CatchyOS,
  EndeavourOS ...)

# Installation
[![Get it on Flathub](https://flathub.org/api/badge?svg&locale=en)](https://flathub.org/apps/de.z_ray.OptimusUI)

# Tested configurations:

## openSUSE Aeon (aka. Aeon Desktop or just Aeon)

Note: This means any openSUSE based distribution should work as well

- SUSEPrime
  - 0.8.17
  - 0.8.18
- nVidia driver
  - 470.256.02
  - 470.239.06
- Intel i5-3230M
- nVidia GeForce GT 730M
