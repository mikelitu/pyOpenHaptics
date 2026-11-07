from .hd import *
from .hd_callback import *
from .hd_define import *

class HapticDevice(object):
    _active_devices = 0

    def __init__(self, callback: hd_callback, device_name: str = "Default Device", scheduler_type: str = "async"):

        self._closed = True
        self._scheduler_handle = None
        print("Initializing haptic device with name {}".format(device_name))

        # The scheduler snapshots initialized devices when it starts. Stop it
        # before adding a device, including all device-specific setup calls.
        had_devices = HapticDevice._active_devices > 0
        if had_devices:
            stop_scheduler()
        self.id = None
        try:
            self.id = init_device(device_name)
            make_current_device(self.id)
            # Keep callback data alive for as long as the scheduler uses it.
            self._device_id = HHD(self.id)
            self._callback = callback
            print("Initialized device! {}/{}".format(self.__vendor__(), self.__model__()))
            enable_force()
            if get_error():
                raise DeviceInitException(f"Unable to configure {device_name!r}")
            if scheduler_type == "async":
                self.scheduler(callback, scheduler_type)
                if get_error():
                    raise DeviceInitException(f"Unable to schedule {device_name!r}")
            start_scheduler()
            if get_error():
                raise DeviceInitException(f"Unable to start {device_name!r}")
            # A synchronous call needs a running scheduler to complete.
            if scheduler_type != "async":
                self.scheduler(callback, scheduler_type)
        except Exception:
            stop_scheduler()
            if self._scheduler_handle is not None:
                hdUnschedule(self._scheduler_handle)
            if self.id is not None:
                close_device(self.id)
            if had_devices:
                start_scheduler()
            raise
        HapticDevice._active_devices += 1
        self._closed = False

    def close(self):
        if self._closed:
            return
        stop_scheduler()
        if self._scheduler_handle is not None:
            hdUnschedule(self._scheduler_handle)
        close_device(self.id)
        self._closed = True
        HapticDevice._active_devices -= 1
        if HapticDevice._active_devices:
            start_scheduler()
    
    def scheduler(self, callback, scheduler_type):
        if scheduler_type == "async":
            self._scheduler_handle = hdAsyncSheduler(callback, byref(self._device_id))
        else:
            hdSyncSheduler(callback, byref(self._device_id))


    @staticmethod
    def __vendor__() -> str:
        return get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return get_model()
