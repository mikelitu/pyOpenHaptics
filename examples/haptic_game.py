#!/usr/bin/env python
""" pygame.examples.moveit

This is the full and final example from the Pygame Tutorial,
"How Do I Make It Move". It creates 10 objects and animates
them on the screen.

It also has a separate player character that can be controlled with arrow keys.

Note it's a bit scant on error checking, but it's easy to read. :]
Fortunately, this is python, and we needn't wrestle with a pile of
error codes.
"""
import os
import pygame
from ctypes import *
from pyHD.hd_define import *
import pyHD.hd as hd
import time
from dataclasses import dataclass, field

_lib_hd = CDLL("libHD.so")

@dataclass
class DeviceState:
    button: bool = False
    position: list = field(default_factory=list)
    joints: list = field(default_factory=list)
    gimbals: list = field(default_factory=list)
    force: list = field(default_factory=list)

@CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
def state_callback(pUserData):
    global device_state
    hd.begin_frame(hd.get_current_device())
    transform = hd.get_transform()
    joints = hd.get_joints()
    gimbals = hd.get_gimbals()
    device_state.position = [transform[3][0], -transform[3][2], transform[3][1]]
    device_state.joints = [joints[0], joints[1], joints[2]]
    device_state.gimbals = [gimbals[0], gimbals[1], gimbals[2]]
    hd.set_force(device_state.force)
    button = hd.get_buttons()
    device_state.button = True if button==1 else False 
    hd.end_frame(hd.get_current_device())
    # print(hd.get_error())
    if(hd.get_error()):
        return HD_CALLBACK_DONE
    
    return HD_CALLBACK_CONTINUE

class HapticDevice(object):
    def __init__(self, device_name: str = "Default Device"):

        print("Initializing haptic device with name {}".format(device_name))
        self.id = hd.init_device(None)
        print("Intialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        hd.enable_force()
        hd.start_scheduler()
        if hd.get_error():
            SystemError()
        self.callback()

    def close(self):
        hd.stop_scheduler()
        hd.close_device(self.id)
    
    def callback(self):
        global device_state
        pUserData = c_void_p()
        device_state = DeviceState(force=[0, 0, 0])
        _lib_hd.hdScheduleAsynchronous(state_callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)

    @staticmethod
    def __vendor__() -> str:
        return hd.get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return hd.get_model()
    

def main():
    pygame.init()

    surface = pygame.display.set_mode((680, 420))

    # Initializing color
    red = (255, 0, 0)
    green = (0, 255, 0)

    # Drawing rectangle
    small_rectangle = pygame.Rect(40, 40, 60, 60)
    big_rectangle = pygame.Rect(30, 30, 620, 360)
    pygame.draw.rect(surface, red, small_rectangle)
    pygame.draw.rect(surface, green, big_rectangle, 2)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(100)
        small_rectangle.move_ip(1, 0)
        surface.fill((1, 1, 1))
        pygame.draw.rect(surface, red, small_rectangle)
        pygame.draw.rect(surface, green, big_rectangle, 2)
        dev_x, dev_y = device_state.position[0], device_state.position[1]
        print(dev_x, dev_y)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pygame.display.flip()
        



if __name__ == "__main__":
    device = HapticDevice()
    main()
    device.close()