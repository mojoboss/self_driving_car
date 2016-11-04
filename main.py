__author__ = 'starlord'
import pygame
from pygame.locals import *
import numpy as np
import math

angle = 0.005
def vel_update(angle, vel):
	rot = np.array(([math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]))
	rot = np.matrix(rot)
	vel = np.matrix(vel)
	return np.transpose(rot*np.transpose(vel)).tolist()

#print vel_update(0.0001, np.array([5, 5]))

pygame.init()
width, height = (30, 30)
SCREEN_SIZE = (900, 600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
location = np.array((200.0, 50.0))
velocity = np.array((0.1, 0.0))
background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))

while True:
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    if key_pressed[K_LEFT]:
        velocity = vel_update(angle, velocity)
        print location, velocity
        
    elif key_pressed[K_RIGHT]:
        velocity = vel_update(-1*angle, velocity)
        print location, velocity

    location += velocity[0]
    screen.blit(background, (0,0))
    #pygame.draw.rect(screen, (255,255,0),[location[0],location[1],width,height])
    pygame.draw.circle(screen, (255,55,10),(int(location[0]),int(location[1])), 15)
    pygame.display.update()

