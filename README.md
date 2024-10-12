# OptimusUI

![OptimusUI Icon](https://raw.githubusercontent.com/Z-Ray-Entertainment/optimus-ui/refs/heads/main/optimusui/data/screenshots/icon_small.png)

OptimusUI is a graphical user interface for prime-select.  
It allows a Laptop or Desktop system with an integrated GPU and a dedicated GPU to switch between these two. By either
running entirely on the dGPU, the iGPU or using nVidia's Offloading technology.

![OptimusUI](https://raw.githubusercontent.com/Z-Ray-Entertainment/optimus-ui/refs/heads/main/optimusui/data/screenshots/optimus_ui.png)

## Requirements

This application aims to be as simple as possible. this also includes it's dependencies.  
But there are still various things which can not be distributed by this application.
The following needs to be present on the target system:

- proprietary nvidia driver version >= 390
- suse-prime or nvidia-prime
- bbswitch (Recommended but not required)

## Supported Distributions

### openSUSE

This includes openSUSE Leap, Tumbleweed, MicroOS, Aeon, Kalpa, Gecko Linux and Gecko Linux Rolling.  
For openSUSE based distributions please install [SUSEPrime](https://github.com/openSUSE/SUSEPrime)

### Ubuntu

This includes Ubuntu, Kubuntu, Lubuntu, Xubuntu, Linux Mint (Ubuntu Edition), Pop_OS and many more.
For Ubuntu based distributions please install [nvidia-prime](https://wiki.ubuntuusers.de/Hybrid-Grafikkarten/PRIME/)

**Note:** While Ubuntu is supported the prime tool does lack some features and therefore some options are not available.

## WIP Distributions

- Fedora via fedora-prime-select
- Arch Linux via nvidia-prime-select

## Unsupported distributions

### Debian

Debian has no nvidia-prime, suse-prime or prime-select like package which can be supported by this application
Source: https://debianforum.de/forum/viewtopic.php?t=188303#p1344248

# Tested configurations:

## openSUSE Aeon (aka. Aeon Desktop or just Aeon)

Note: This means any openSUSE based distribution should work as well

- SUSEPrime 0.8.17
- nVidia driver 470.256.02
- Intel i5-3230M
- nVidia GeForce GT 730M
