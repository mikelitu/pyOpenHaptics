"""pyOpenHaptics.examples.haptic_device.py
Simple example on how to write your custom haptic device class and callback function for any type.
In this case we are just getting the value of the button on the Touch X to change an ASCII drawing.
It only updates the drawing if the state of the button changes.
"""

from pyOpenHaptics.hd_device import HapticDevice
import pyOpenHaptics.hd as hd
import time
from dataclasses import dataclass
from pyOpenHaptics.hd_callback import hd_callback

@dataclass
class DeviceState:
    """Class to store the state of the device"""
    # Device ID
    device_id: int = 0
    # Button state
    button: bool = False

@hd_callback
def button_callback():
    global device_state
    # Set the device to the current device
    hd.make_current_device(device_state.device_id)
    button = hd.get_buttons()
    device_state.button = True if button==1 else False 
        

if __name__ == "__main__":
    device_state = DeviceState()
    device = HapticDevice(callback = button_callback, device_name = "Default Device", scheduler_type = "async")
    pre_button = device_state.button
    for i in range(10000):
        if pre_button != device_state.button:
            if device_state.button:
                print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠉⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⠟⠋⣠⣿⣦⣄⣀⣀⣀⡀⠀⠀⠀⠀⠙⣷⠙⠻⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⡿⠁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣴⣾⣿⣿⣦⠈⢿⣿⣿⣿⣿\n⣿⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣿⣿⣿\n⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⣿⣿⣿\n⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿\n⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿\n⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿\n⣿⣿⣿⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠥⣿⣿⣿\n⣿⣿⣿⣿⠋⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠤⠤⠤⠄⢀⠀⣿⣿\n⣿⣿⣿⠁⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣶⣶⣶⡆⠀⣿⡄⢸⣿\n⣿⣿⡇⠀⠀⠀⠀⣿⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⡿⠀⣿⠀⣼⣿\n⣿⣿⣿⣤⣀⣠⣾⣿⣿⣶⣦⣬⣉⣉⣉⣉⣉⣉⣽⣇⣈⣉⣉⣉⣁⣀⣤⣶⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
            else:
                print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣠⣴⠟⠀⠙⠻⠿⠿⠿⢿⣿⣿⣿⣿⣦⠈⣦⣄⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠋⠁⠀⠀⠙⣷⡀⠀⠀⠀⠀\n⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀\n⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⠀⠀⠀\n⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀\n⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀\n⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀\n⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣚⠀⠀⠀\n⠀⠀⠀⠀⣴⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣛⣛⣛⣻⡿⣿⠀⠀\n⠀⠀⠀⣾⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠉⠉⠉⢹⣿⠀⢻⡇⠀\n⠀⠀⢸⣿⣿⣿⣿⠀⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢀⣿⠀⣿⠃⠀\n⠀⠀⠀⠛⠿⠟⠁⠀⠀⠉⠙⠓⠶⠶⠶⠶⠶⠶⠂⠸⠷⠶⠶⠶⠾⠿⠛⠉⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        pre_button = device_state.button
        time.sleep(0.001)       
    device.close()