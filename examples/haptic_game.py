#!/usr/bin/env python
""" pyOpenHaptics.example.haptic_game.py

This example contains a small demo of a haptic game of a rectangle trapped in a confined space.
The closer the red rectangle gets to the ends the more force will you feel in the device.
This example is to show the capabilities of developing such applications in pure Python language
using the pyOpenHaptics library.

"""

import pygame
from pyOpenHaptics.hd_device import HapticDevice
import pyOpenHaptics.hd as hd
import time
from dataclasses import dataclass, field
from pyOpenHaptics.hd_callback import hd_callback

@dataclass
class DeviceState:
    button: bool = False
    position: list = field(default_factory=list)
    joints: list = field(default_factory=list)
    gimbals: list = field(default_factory=list)
    force: list = field(default_factory=list)

@hd_callback
def state_callback():
    global device_state
    transform = hd.get_transform()
    joints = hd.get_joints()
    gimbals = hd.get_gimbals()
    device_state.position = [transform[3][0], -transform[3][1], transform[3][2]]
    device_state.joints = [joints[0], joints[1], joints[2]]
    device_state.gimbals = [gimbals[0], gimbals[1], gimbals[2]]
    hd.set_force(device_state.force)
    button = hd.get_buttons()
    device_state.button = True if button==1 else False

def wall_feedback(big: pygame.Rect, small: pygame.Rect):
    device_state.force = [0, 0, 0]

    if small.y <= 80:
        device_state.force[1] = -0.05 * (80 - small.y)
    elif small.y + 60 >= 1000:
        device_state.force[1] = 0.05 * (small.y + 60 - 1000)
    
    if small.x <= 80:
        device_state.force[0] = 0.05 * (80 - small.x)
    elif small.x + 60 >= 1800:
        device_state.force[0] = -0.0275 * (small.x + 60 - 1800)
        

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
    device_state = DeviceState()
    device = HapticDevice(callback=state_callback)
    time.sleep(0.2)
    main()
    device.close()