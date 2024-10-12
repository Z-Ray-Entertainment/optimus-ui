# OptimusUI

![OptimusUI Icon](https://raw.githubusercontent.com/Z-Ray-Entertainment/optimus-ui/refs/heads/main/optimusui/data/screenshots/icon_small.png)

OptimusUI is a graphical user interface for prime-select.  
It allows a Laptop or Desktop system with an integrated GPU and a dedicated GPU to switch between these two. By either
running entirely on the dGPU, the iGPU or using nVidia's Offloading technology.

![OptimusUI](https://raw.githubusercontent.com/Z-Ray-Entertainment/optimus-ui/refs/heads/main/optimusui/data/screenshots/optimus_ui.png)

## Supported Prime Tools

- openSUSE [SUSEPrime](https://github.com/openSUSE/SUSEPrime)
- Ubuntu: [nvidia-prime](https://wiki.ubuntuusers.de/Hybrid-Grafikkarten/PRIME/) (Supported but lacks some features
  which means some option are not available)

## Work in progress Prime Tools:

- fedora-prime-select (Fedora)
- nvidia-prime-select (Arch Linux)

## Unsupported distributions

### Debian

Debian has not nvidia-prime, suse-prime or prime-select like package which can be supported by this application

## Requirements

This application aims to be as simple as possible. this also includes it's dependencies.  
But there are still various things which can not be distributed by this application.
The following needs to be present on the target system:

- proprietary nvidia driver version >= 390
- suse-prime or nvidia-prime
- bbswitch (Recommended but not required)

# Tested configurations:

## openSUSE Aeon (aka. Aeon Desktop or just Aeon)

Note: This means openSUSE Tumbleweed and Leap should work as well

- SUSEPrime 0.8.17
- nVidia driver 470.256.02
- Intel i5-3230M
- nVidia GeForce GT 730M
