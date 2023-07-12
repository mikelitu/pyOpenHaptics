from ctypes import *
from hd_define import *
from typing import List
from hdu_matrix import hduMatrix, hduVector3Dd
from sys import platform
from exceptions import *

exception_dict = {
    HD_BAD_HANDLE: DeviceInitException,
    HD_INVALID_ENUM: InvalidEnumException,
    HD_INVALID_OPERATION: InvalidOperationException,
    HD_INVALID_HANDLE: DeviceInitException,
    HD_FORCE_ERROR: ForceTypeExceptions,
}

if platform == "linux" or platform == "linux2":
    _lib_hd = CDLL("libHD.so")
elif platform == "win32":
    _lib_hd = CDLL("HD.dll")

def _get_doublev(code: int, dtype):
    data = dtype()
    _lib_hd.hdGetDoublev.argtypes = [HDenum, POINTER(dtype)]
    _lib_hd.hdGetDoublev.restype = None
    _lib_hd.hdGetDoublev(code, data)
    return data

def _get_integerv(code: int, dtype):
    data = dtype()
    _lib_hd.hdGetIntegerv.argtypes = [HDenum, POINTER(dtype)]
    _lib_hd.hdGetIntegerv.restype = None
    _lib_hd.hdGetIntegerv(code, data)
    return data

def _set_doublev(code: int, value, dtype):
    data = dtype(*value)
    _lib_hd.hdSetDoublev.argtypes = [HDenum, POINTER(dtype)]
    _lib_hd.hdSetDoublev.restype = None
    _lib_hd.hdSetDoublev(code, data)

def _get_error() -> HDErrorInfo:
    _lib_hd.hdGetError.restype = HDErrorInfo
    return _lib_hd.hdGetError()


def init_device(name: str = None) -> int:
    _lib_hd.hdInitDevice.argtypes = [c_char_p]
    _lib_hd.hdInitDevice.restype = HHD
    try:
        id = _lib_hd.hdInitDevice(HD_DEFAULT_DEVICE)
        if id == HD_BAD_HANDLE:
            raise DeviceInitException
        else:
            return id
    except DeviceInitException:
        print("Unable to initialize the device. Check the connection!")

def get_buttons() -> int:
    return _get_integerv(HD_CURRENT_BUTTONS, HDint).value

def get_transform() -> hduMatrix:
    return _get_doublev(HD_CURRENT_TRANSFORM, hduMatrix)

def get_joints() -> hduVector3Dd:
    return _get_doublev(HD_CURRENT_JOINT_ANGLES, hduVector3Dd)

def get_gimbals() -> hduVector3Dd:
    return _get_doublev(HD_CURRENT_GIMBAL_ANGLES, hduVector3Dd)

def get_error() -> bool:
    error = _get_error().errorCode
    try:
        if error == HD_SUCCESS:
            return False
        else:
            raise exception_dict[error]
    except exception_dict[error] as e:
        print("{}: Error during the main scheduler.".format(type(e).__name__))
        return True

def set_force(feedback: List[float]) -> None:
    _set_doublev(HD_CURRENT_FORCE, feedback, hduVector3Dd)
    

def close_device(id: int):
    _lib_hd.hdDisableDevice.argtypes = [HHD]
    _lib_hd.hdDisableDevice(id)

def get_current_device() -> HHD:
    _lib_hd.hdGetCurrentDevice.restype = HHD
    return _lib_hd.hdGetCurrentDevice()

def start_scheduler() -> None:
    _lib_hd.hdStartScheduler()

def stop_scheduler() -> None:
    _lib_hd.hdStopScheduler()

def enable_force() -> None:
    _lib_hd.hdEnable.argtypes = [HDenum]
    _lib_hd.hdEnable.restype = None
    _lib_hd.hdEnable(HD_FORCE_OUTPUT)
    print("Force feedback enabled!")

def begin_frame(id: int) -> None:
    _lib_hd.hdBeginFrame.argtypes = [HHD]
    _lib_hd.hdBeginFrame.restype = None
    _lib_hd.hdBeginFrame(id)

def end_frame(id: int) -> None:
    _lib_hd.hdEndFrame.argtypes = [HHD]
    _lib_hd.hdEndFrame.restype = None
    _lib_hd.hdEndFrame(id)

def get_model() -> str:
    _lib_hd.hdGetString.argtypes = [HDenum]
    _lib_hd.hdGetString.restype = HDstring
    return  _lib_hd.hdGetString(HD_DEVICE_MODEL_TYPE).decode()

def get_vendor() -> str:
    _lib_hd.hdGetString.argtypes = [HDenum]
    _lib_hd.hdGetString.restype = HDstring
    return _lib_hd.hdGetString(HD_DEVICE_VENDOR).decode()



