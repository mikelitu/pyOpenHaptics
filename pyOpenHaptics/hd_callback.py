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
    @CFUNCTYPE(HDCallbackCode, c_void_p)
    def _callback(pUserData):
        """Callback function for the haptic device.
        This function is called by the haptic device when it is ready to process input.
        It calls the input_function passed as an argument and checks for errors.
        """
        device_id = cast(pUserData, POINTER(HHD)).contents.value if pUserData else get_current_device()
        make_current_device(device_id)
        begin_frame(device_id)
        try:
            input_function()
        finally:
            end_frame(device_id)
        if(get_error()):
            return HD_CALLBACK_DONE
        return HD_CALLBACK_CONTINUE
    
    return _callback

def hdAsyncSheduler(callback, user_data=None):
    _lib_hd.hdScheduleAsynchronous.restype = c_ulong
    return _lib_hd.hdScheduleAsynchronous(callback, user_data, HD_MAX_SCHEDULER_PRIORITY)

def hdSyncSheduler(callback, user_data=None):
    _lib_hd.hdScheduleSynchronous(callback, user_data, HD_MAX_SCHEDULER_PRIORITY)

def hdUnschedule(handle):
    _lib_hd.hdUnschedule.argtypes = [c_ulong]
    _lib_hd.hdUnschedule.restype = None
    _lib_hd.hdUnschedule(handle)
