from ctypes import *
from .hd_define import *
import functools
from .hd import *
from sys import platform

if platform == "linux" or platform == "linux2":
    _lib_hd = CDLL("libHD.so")
elif platform == "win32":
    _lib_hd = CDLL("HD.dll")

def hd_callback(input_function):
    @functools.wraps(input_function)
    @CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
    def _callback(pUserData):
        """Callback function for the haptic device.
        This function is called by the haptic device when it is ready to process input.
        It calls the input_function passed as an argument and checks for errors.
        """
        begin_frame(get_current_device())
        input_function()
        end_frame(get_current_device())
        if(get_error()):
            return HD_CALLBACK_DONE
        return HD_CALLBACK_CONTINUE
    
    return _callback

def hdAsyncSheduler(callback):
    pUserData = c_void_p()
    _lib_hd.hdScheduleAsynchronous(callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)

def hdSyncSheduler(callback):
    pUserData = c_void_p()
    _lib_hd.hdScheduleSynchronous(callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)