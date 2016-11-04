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

def detect_collision(obstacles, r1, r2):
	if location[0] <= 0 or location[0] >= SCREEN_SIZE[0] or location[1] <= 0 or location[1] >= SCREEN_SIZE[1]:
		return True 
	for i in obstacles:
		dist = math.sqrt((location[0]-i[0])**2 + (location[1]-i[1])**2)
		if dist <= r1+r2 :
			return True
	return False

pygame.init()
width, height = (30, 30)
SCREEN_SIZE = (900, 600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
location = np.array((200.0, 50.0))
velocity = np.array((0.2, 0.0))
background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))
obstacles = [[50, 50], [450, 300], [700, 300], [100, 400]]

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
    pygame.draw.circle(screen, (255,55,10),(int(location[0]),int(location[1])), 15)

    if detect_collision(obstacles, 15, 35):
		location = np.array((200.0, 50.0))
    for i in obstacles:
    	pygame.draw.circle(screen, (25,55,100), i, 35)
    pygame.display.update()

