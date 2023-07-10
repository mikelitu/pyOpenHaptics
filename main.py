from ctypes import *
from hd import *

class HapticDevice(object):
    def __init__(self, device_name: str = "Default Device"):

        print("Initializing haptic device with name {}".format(device_name))
        self.lib_hd = CDLL("/usr/lib/libHD.so")
        self.lib_hd.hdInitDevice.argtypes = [c_char_p]
        self.lib_hd.hdInitDevice.restype = HHD
        self.id = self.lib_hd.hdInitDevice(HD_DEFAULT_DEVICE)
        print("Started {}/{} device".format(self.vendor(), self.model()))
    
    def get_serial_number(self):
        self.lib_hd.hdGetCurrentDevice.restype = HHD
        device = self.lib_hd.hdGetCurrentDevice()
        print(device)

    def begin_frame(self):  
        self.lib_hd.hdBeginFrame.argtypes = [HHD]
        self.lib_hd.hdBeginFrame.restype = None
        self.lib_hd.hdBeginFrame(self.id)
    
    def end_frame(self):
        self.lib_hd.hdEndFrame.argtypes = [HHD]
        self.lib_hd.hdEndFrame.restype = None
        self.lib_hd.hdEndFrame(self.id)
    
    def scheduler(self):
        self.begin_frame()

        self.end_frame()
    
    def vendor(self) -> str:
        self.lib_hd.hdGetString.argtypes = [HDenum]
        self.lib_hd.hdGetString.restype = HDstring
        return self.lib_hd.hdGetString(HD_DEVICE_VENDOR).decode()
    
    def model(self) -> str:
        self.lib_hd.hdGetString.argtypes = [HDenum]
        self.lib_hd.hdGetString.restype = HDstring
        return  self.lib_hd.hdGetString(HD_DEVICE_MODEL_TYPE).decode()
    
    def getbuttons(self):
        buttonState = HDint(1)
        # self.lib_hd.hdGetIntegerv.argtypes = [HDenum, POINTER(HDint)]
        self.lib_hd.hdGetIntegerv.restype = None
        self.begin_frame()
        self.lib_hd.hdGetIntegerv(HD_CURRENT_BUTTONS, byref(buttonState))
        self.end_frame()
        print(buttonState)

if __name__ == "__main__":
    device = HapticDevice()
    device.getbuttons()