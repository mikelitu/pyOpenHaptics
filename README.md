# pyOpenHaptics

Python wrapper for the OpenHaptics HD library to use the haptic device directly from Python. Used to control the [3dSystems](https://www.3dsystems.com/) devices (Touch/Touch X) directly from Python.

## Requirements
This library requires from the pre-installation of the OpenHaptics libraries and Touch X drivers. For this please follow their official installation tutorial for [Linux](https://support.3dsystems.com/s/article/OpenHaptics-for-Linux-Developer-Edition-v34?language=en_US) or [Windows](https://support.3dsystems.com/s/article/OpenHaptics-for-Windows-Developer-Edition-v35?language=en_US).

OpenHaptics in Linux requires from additional libraries. You can use the following command to install them.

```shell
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install libncurses5-dev freeglut3 build-essential
```

## How to use it

Clone the repository in *pyOpenHaptics* folder. To test that is working run any of the *examples*.

## Developing...

I am working into transforming this into a Python package to be installed via `pip`. However, this is just an alpha and I cannot secure the wheel is working.

`pip install pyOpenHaptics`

Follow the [Pypi Project](https://pypi.org/project/pyOpenHaptics/).