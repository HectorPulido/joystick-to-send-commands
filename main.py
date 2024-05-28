"""
Application to create hotkeys with a joystick
"""

import sys
import pygame
from pygame.locals import QUIT
from command_control import CommandControl


FPS = 24
cc = CommandControl()

# Initialization
pygame.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)


def quit_app():
    """
    Quit the application
    """
    if event.type == QUIT:
        pygame.quit()
        sys.exit()


while True:
    for event in pygame.event.get():
        quit_app()

    cc.run_commands(joystick)
    clock.tick(FPS)
