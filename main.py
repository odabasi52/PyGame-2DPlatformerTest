# import game library
import pygame, sys
# import your own files
from settings import *
from level import Level

# pygame setup
pygame.init()
# set the dimensions of the window
screen = pygame.display.set_mode((screen_width, screen_height))
# set the title of the window
pygame.display.set_caption("Talha")
# create a clock object to control the frame rate later in the code
clock = pygame.time.Clock()
level = Level(level_map, screen)

# runs until the game is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # uninitialize all Pygame modules
            pygame.quit()    
            # exit the Python script
            sys.exit()
    # background color    
    screen.fill('light blue')
    level.run()
    pygame.display.update()
    # control frame rate to maintaine a consistent speed across different devices (60fps)
    clock.tick(60)