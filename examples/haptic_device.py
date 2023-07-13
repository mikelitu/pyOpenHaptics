from ctypes import *
from src.hd_define import *
import src.hd as hd
import time
from dataclasses import dataclass, field

_lib_hd = CDLL("libHD.so")

@dataclass
class DeviceState:
    button: bool = False
    position: list = field(default_factory=list)
    joints: list = field(default_factory=list)
    gimbals: list = field(default_factory=list)
    force: list = field(default_factory=list)

@CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
def state_callback(pUserData):
    global device_state
    hd.begin_frame(hd.get_current_device())
    transform = hd.get_transform()
    joints = hd.get_joints()
    gimbals = hd.get_gimbals()
    device_state.position = [transform[3][0], -transform[3][2], transform[3][1]]
    device_state.joints = [joints[0], joints[1], joints[2]]
    device_state.gimbals = [gimbals[0], gimbals[1], gimbals[2]]
    # hd.set_force([1.0, 0.0, 0.0])
    button = hd.get_buttons()
    device_state.button = True if button==1 else False 
    hd.end_frame(hd.get_current_device())
    # print(hd.get_error())
    if(hd.get_error()):
        return HD_CALLBACK_DONE
    
    return HD_CALLBACK_CONTINUE

class HapticDevice(object):
    def __init__(self, device_name: str = "Default Device"):

        print("Initializing haptic device with name {}".format(device_name))
        self.id = hd.init_device("Default Device")
        print("Intialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        hd.enable_force()
        hd.start_scheduler()
        if hd.get_error():
            SystemError()
        self.callback()

    def close(self):
        hd.stop_scheduler()
        hd.close_device(self.id)
    
    def callback(self):
        global device_state
        pUserData = c_void_p()
        device_state = DeviceState()
        _lib_hd.hdScheduleAsynchronous(state_callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)

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
        # print(device_state.position)
        time.sleep(0.001)       
    device.close()