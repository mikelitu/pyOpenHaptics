"""pyOpenHaptics.examples.haptic_device.py
Simple example on how to write your custom haptic device class and callback function for any type.
In this case we are just getting the value of the button on the Touch X to change an ASCII drawing.
It only updates the drawing if the state of the button changes.
"""

from ctypes import *
from src.hd_define import *
import src.hd as hd
import time
from dataclasses import dataclass
from src.hd_callback import *

@dataclass
class DeviceState:
    button: bool = False

@hd_callback
def button_callback():
    global device_state
    hd.begin_frame(hd.get_current_device())
    button = hd.get_buttons()
    device_state.button = True if button==1 else False 
    hd.end_frame(hd.get_current_device())

class HapticDevice(object):
    def __init__(self, device_name: str = "Default Device", scheduler_type: str = "async"):

        print("Initializing haptic device with name {}".format(device_name))
        self.id = hd.init_device(device_name)
        print("Intialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        hd.enable_force()
        hd.start_scheduler()
        if hd.get_error():
            SystemError()
        self.scheduler(scheduler_type)

    def close(self):
        hd.stop_scheduler()
        hd.close_device(self.id)
    
    def scheduler(self, scheduler_type):
        global device_state
        device_state = DeviceState()
        if scheduler_type == "async":
            hdAsyncSheduler(button_callback)
        else:
            hdSyncSheduler(button_callback)

    @staticmethod
    def __vendor__() -> str:
        return hd.get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return hd.get_model()
        

if __name__ == "__main__":
    device = HapticDevice()
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