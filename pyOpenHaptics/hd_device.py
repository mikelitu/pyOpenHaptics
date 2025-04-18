from .hd import *
from.hd_callback import *
from .hd_define import *

class HapticDevice(object):
    def __init__(self, callback: hd_callback, device_name: str = "Default Device", scheduler_type: str = "async"):

        print("Initializing haptic device with name {}".format(device_name))
        current_id = get_current_device()
        
        self.id = init_device(device_name)
        if self.id == HD_BAD_HANDLE:
            print("Unable to initialize the device. Check the connection!")
            return
        
        if current_id != self.id:
            make_current_device(self.id)
            print("Device {} is already initialized.".format(device_name))
            return
        
        print("Intialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        enable_force()
        start_scheduler()
        if get_error():
            SystemError()
        self.scheduler(callback, scheduler_type)

    def close(self):
        stop_scheduler()
        close_device(self.id)
    
    def scheduler(self, callback, scheduler_type):
        if scheduler_type == "async":
            hdAsyncSheduler(callback)
        else:
            hdSyncSheduler(callback)


    @staticmethod
    def __vendor__() -> str:
        return get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return get_model()