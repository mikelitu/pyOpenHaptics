from ctypes import *
from hd_define import *
import hd
import time

_lib_hd = CDLL("libHD.so")

@CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
def callback(pUserData):
    # device_state = pUserData(DeviceDisplayState)
    hd.begin_frame(hd.get_current_device())
    button = hd.get_integerv(HD_CURRENT_BUTTONS)
    if button == 1:
        print("Apply force!")
        feedback = [5, 0, 0]    
    else:
        print("Remove force!")
        feedback = [0, 0, 0]
    hd.set_doublev(HD_CURRENT_FORCE, feedback)        
    hd.end_frame(hd.get_current_device())
    return HD_CALLBACK_CONTINUE


class HapticDevice(object):
    def __init__(self, device_name: str = "Default Device"):

        print("Initializing haptic device with name {}".format(device_name))
        self.id = hd.init_device(None)
        print("Intialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        hd.enable_force()
        hd.start_scheduler()

    def close(self):
        hd.stop_scheduler()
        hd.close_device(self.id)

    def enable_force(self):
        _lib_hd.hdEnable.argtypes = [HDenum]
        _lib_hd.hdEnable.restype = None
        _lib_hd.hdEnable(HD_FORCE_OUTPUT)
    
    def callback(self):
        pUserData = c_void_p()
        _lib_hd.hdScheduleSynchronous(callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)

    @staticmethod
    def __vendor__() -> str:
        return hd.get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return hd.get_model()
        

if __name__ == "__main__":
    device = HapticDevice()
    device.callback()
    device.close()