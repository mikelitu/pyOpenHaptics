class DeviceInitException(Exception):
    "Raised when the device is not initialized properly"
    pass

class InvalidEnumException(Exception):
    "Raised when there is a problem with the enum"
    pass

class InvalidValueException(Exception):
    "Raised when there is an invalid value on a function"
    pass

class InvalidOperationException(Exception):
    "Raised when you perform an invalid operation"
    pass

class InvalidInputTypeException(Exception):
    "Raised when the input of a function is invalid"
    pass

class ForceTypeExceptions(Exception):
    "Raised when there is a problem with the force"
    pass