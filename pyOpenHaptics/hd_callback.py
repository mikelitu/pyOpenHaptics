from ctypes import *
from .hd_define import *
import functools
from .hd import *

_lib_hd = CDLL("libHD.so")

def hd_callback(input_function):
    @functools.wraps(input_function)
    @CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
    def _callback(pUserData):
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