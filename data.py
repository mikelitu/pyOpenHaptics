from ctypes import *



class DeviceDisplayState(Structure):
    __fields__=[
        ('Position', c_double),
        ('Force', c_double)
    ]

if __name__ == "__main__":
    DeviceDisplayState()