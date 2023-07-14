# pyOpenHaptics

Python wrapper for the OpenHaptics HD library to use the haptic device directly from Python. Used to control the [3dSystems](https://www.3dsystems.com/) devices (Touch/Touch X) directly from Python.

## Prerequisites

This library requires from the pre-installation of the OpenHaptics libraries and Touch X drivers. For this please follow their official installation tutorial for [Linux](https://support.3dsystems.com/s/article/OpenHaptics-for-Linux-Developer-Edition-v34?language=en_US) or [Windows](https://support.3dsystems.com/s/article/OpenHaptics-for-Windows-Developer-Edition-v35?language=en_US).

OpenHaptics in Linux requires from additional libraries. You can use the following command to install them.

```shell
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install libncurses5-dev freeglut3 build-essential
```

## Installation

Use the latest version from the [PyPi project](https://pypi.org/project/pyOpenHaptics/).

```shell
python3 -m pip install pyOpenHaptics
```

## How to use it

The library contains multiple functionalities to get and set different variables. Most of the functionalities are gathered into 3 different files *hd.py*, *hd_callback.py* and *hd_device.py*.
The first file contains a Python mimic of most of the OpenHaptics HD library main functions. The second file contains the schedulers and a python wrapper to wrap your python callback function into a C callback function to interact with the already compiled shared library. Lastly, this defines the Python class to initialize your Haptic hardware and interface.

## Haptic device template

Here is a small template on how to setup your callback loop and your haptic device to gather the desired information from the device. 

```python
import pyOpenHaptics.hd as hd
from pyOpenHaptics.hd_callback import hd_callback
from pyOpenHaptics.hd_device import HapticDevice
from dataclasses import dataclass

# Data class to keep track of the device state and use it in other parts of the code
@dataclass
class DeviceState:
    # Define the variables you want to safe here

# Callback to gather the device state
@hd_callback
def device_callback():
    # Make the device_state global to be accesed in other parts of the code
    global device_state
    # your callback function, gather the different variables on the device
    # YOUR CODE HERE

if __name__ == "__main__":
    # Initialize the data class
    device_state = DeviceState()

    # Initialize the haptic device and the callback loop
    device = HapticDevice(callback = device_callback, scheduler_type="async")
    
    # YOUR CODE HERE
    
    # Close the device to avoid segmentation faults
    device.close()
```

You can find more complex examples [here](examples)