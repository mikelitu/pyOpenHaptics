from ctypes import *


HDint = c_int
HDuint = c_uint
HDboolean = c_bool
HDulong = c_ulong
HDfloat = c_float
HDdouble = c_double
HDlong = c_long
HDchar = c_char
HDerror = c_uint
HDenum = c_uint
HDstring = c_char_p
HHD = c_uint
HDCallback = CFUNCTYPE(None, c_void_p)

# Boolean
HD_TRUE = 1
HD_FALSE = 0

# Version information
HD_VERSION_MAJOR_NUMBER = 3
HD_VERSION_MINOR_NUMBER = 30
HD_VERSION_BUILD_NUMBER = 0

HD_DEVICE_MODEL_TYPE = 0x2501
HD_DEVICE_VENDOR = 0x2503

HD_CURRENT_POSITION = 0x2050
HD_DEFAULT_DEVICE = None
HD_VERSION = 0x2500
HD_CURRENT_BUTTONS = 0x2000

