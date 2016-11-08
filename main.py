__author__ = 'starlord'
import pygame
from pygame.locals import *
import numpy as np
import math
import model

#state variables
epochs = 1000
gamma = 0.9
epsilon = 1
angle = 0.005
width, height = (30, 30)
SCREEN_SIZE = (900, 600)
location = np.array((200.0, 50.0))
velocity = np.array((0.2, 0.0))
RADIUS_CAR = 15
RADIUS_OBSTACLES = 35
obstacles = [[50, 50], [450, 300], [700, 300], [100, 400]]
width, height = (30, 30)
SCREEN_SIZE = (900, 600)
model = model.create_model()

#updates the velocity to turn towards an angle
def vel_update(angle, vel):
	rot = np.array(([math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]))
	rot = np.matrix(rot)
	vel = np.matrix(vel)
	return np.transpose(rot*np.transpose(vel)).tolist()

#detects collision b/w the agent and all the obstacles
def detect_collision(obstacles, r1, r2):
	if location[0] <= 0 or location[0] >= SCREEN_SIZE[0] or location[1] <= 0 or location[1] >= SCREEN_SIZE[1]:
		return True 
	for i in obstacles:
		dist = math.sqrt((location[0]-i[0])**2 + (location[1]-i[1])**2)
		if dist <= r1+r2 :
			return True
	return False

#returns the distances from all the obstacles as a list
def get_distances(location, obstacles):
	distances = []
	for i in obstacles:
		dist = math.sqrt((location[0]-i[0])**2 + (location[1]-i[1])**2)
		distances.append(dist)
	return distances

#this returns the state ot any particular instant
def get_state(velocity, location, obstacles):
	thres = 200
	try:
		vx = velocity[0]
		vy = velocity[1]
	except Exception as e:
		vx = velocity[0][0]
		vy = velocity[0][1]
	distances = get_distances(location, obstacles)
	d0 = distances[0]
	d1 = distances[1]
	d2 = distances[2]
	d3 = distances[3]
	i0x = (obstacles[0][0]-location[0])/d0
	i0y = (obstacles[0][1]-location[1])/d0
	i1x = (obstacles[1][0]-location[0])/d1
	i1y = (obstacles[1][1]-location[1])/d1
	i2x = (obstacles[2][0]-location[0])/d2
	i2y = (obstacles[2][1]-location[1])/d2
	i3x = (obstacles[3][0]-location[0])/d3
	i3y = (obstacles[3][1]-location[1])/d3
	return [vx, vy, d0/1000, d1/1000, d2/1000, d3/1000, i0x, i0y, i1x, i1y, i2x, i2y, i3x, i3y]

#reward system for our agent
def get_reward(obstacles, RADIUS_CAR, RADIUS_OBSTACLES):
	if detect_collision(obstacles, RADIUS_CAR, RADIUS_OBSTACLES):
		location = np.array((200.0, 50.0))
		return -100
	return -1

#action to be taken for any given NN output
def get_action(action, velocity):
	if action == 0:
		return vel_update(angle, velocity)
	elif action == 1:
		return vel_update(-1*angle, velocity)
	else: 
		return velocity

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))

while True:
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
  
    if key_pressed[K_LEFT]:
        velocity = vel_update(angle, velocity)
        
    elif key_pressed[K_RIGHT]:
        velocity = vel_update(-1*angle, velocity)

    #print get_state(velocity, location, obstacles)

    location += velocity[0]
    screen.blit(background, (0,0))
    pygame.draw.circle(screen, (255,55,10),(int(location[0]),int(location[1])), RADIUS_CAR)

    for i in obstacles:
    	pygame.draw.circle(screen, (25,55,100), i, RADIUS_OBSTACLES)
    pygame.display.update()

