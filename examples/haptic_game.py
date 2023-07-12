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
from src.hd_define import *
import src.hd as hd
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
    device_state.position = [transform[3][0], -transform[3][1], transform[3][2]]
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

def wall_feedback(big: pygame.Rect, small: pygame.Rect):
    if small.y < 80:
        device_state.force[1] = -(big.y/small.y) * 2.5 + 2.5 * (big.y/80)
    elif small.y + 60 > 1000:
        device_state.force[1] = ((small.y + 60)/(big.height + 30)) * 2.5 - 2.5 * (1060/(big.height + 30))
    elif small.x < 80:
        device_state.force[0] = (big.x/small.x) * 2.5 - 2.5 * (big.x/80)
    elif small.x + small.width > 1800:
        print("Hello!")
        print(-((small.x + small.width)/(big.width)) * 2.5)
        device_state.force[0] = -((small.x + small.width)/(big.width + big.x)) * 2.5 + 2.5 * (1800/(big.width + 30))
    else:
        device_state.force = [0, 0, 0]

def main():
    pygame.init()

    surface = pygame.display.set_mode((1920, 1080))

    # Initializing color
    red = (255, 0, 0)
    green = (0, 255, 0)

    pre_dev_x, pre_dev_y = device_state.position[0], device_state.position[1]

    # Drawing rectangle
    small_rectangle = pygame.Rect(surface.get_width() // 2 - 30, surface.get_height() - 50, 60, 60)
    big_rectangle = pygame.Rect(30, 30, surface.get_width() - 60, surface.get_height() - 60)
    pygame.draw.rect(surface, red, small_rectangle)
    pygame.draw.rect(surface, green, big_rectangle, 2)
    clock = pygame.time.Clock()
    run = True
    pygame.display.flip()

    while run:
        clock.tick(100)
        dev_x, dev_y = device_state.position[0], device_state.position[1]
        small_rectangle.move_ip(10 * (dev_x - pre_dev_x), 9 * (dev_y - pre_dev_y))
        small_rectangle.move_ip(0, 0)
        small_rectangle.clamp_ip(big_rectangle)
        surface.fill((1, 1, 1))
        pygame.draw.rect(surface, red, small_rectangle)
        pygame.draw.rect(surface, green, big_rectangle, 2)
        wall_feedback(big_rectangle, small_rectangle)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pygame.display.flip()
        pre_dev_x, pre_dev_y = dev_x, dev_y

if __name__ == "__main__":
    device = HapticDevice()
    time.sleep(0.2)
    main()
    device.close()