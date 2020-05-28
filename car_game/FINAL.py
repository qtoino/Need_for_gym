# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:19:31 2019

@author: frs98
"""

import pygame
import sys
import time
import random
import os

import argparse
from math import sin, cos, radians, sqrt
import threading
import collections
import time

from pythonosc import dispatcher
from pythonosc import osc_server

pygame.init()

#color
gray=(119,118,110)
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
green=(0,200,0)
blue=(0,0,255)
bright_red=(255,0,0)
bright_green=(0,255,0)
window_width=800
window_hight=600

#display surface
gd=pygame.display.set_mode((window_width,window_hight))
carimg=pygame.image.load('car-clipart-sprite-sheet-14.jpg')
car1=pygame.transform.scale(carimg,(100,100))
enmy1=pygame.image.load('carroamarelo.jpg')
enmy=pygame.transform.scale(enmy1,(100,100))
tree1=pygame.image.load('tree.jpg')
tree=pygame.transform.scale(tree1,(50,50))
clock=pygame.time.Clock()

#movement variables
accelerations = collections.deque(maxlen=100)
current_acceleration = 0
current_force = 0
max_force = 0
best_force = 0
counter = 0
cancel = False
alfa = 0.01
beta = 0.1
enemy_velocity = 0.005
time_exe = 15000

#game functions
def back():
    blue_strip=pygame.image.load('background.jpg')
    img=pygame.transform.scale(blue_strip,(800,600))
    gd.blit(img,(0,0))
    blue_strip=pygame.image.load('download12.jpg')
    img=pygame.transform.scale(blue_strip,(100,600))
    gd.blit(img,(0,0))
    gd.blit(img,(350,0))
    gd.blit(img,(700,0))

def back2():
    blue_strip=pygame.image.load('screen.jpg')
    img=pygame.transform.scale(blue_strip,(800,600))
    gd.blit(img,(0,0))

def car(x, y):
	gd.blit(car1,(x,y))
	#pygame.display.update()

def get_velocity(velocity):
	return current_acceleration * (1/60) * alfa + (1 - beta)*velocity - enemy_velocity

def trees(aux):
	a = aux-180
	if(a > 650):
		a -= 700
	gd.blit(tree,(20,a))
	a = aux-155
	if(a > 650):
		a -= 700
	gd.blit(tree,(50,a))
	a = aux+240
	if(a > 650):
		a -= 700
	gd.blit(tree,(380,a))
	a = aux-30
	if(a > 650):
		a -= 700
	gd.blit(tree,(760,a))
	a = aux+200
	if(a > 650):
		a -= 700
	gd.blit(tree,(740,a))

def other_car(x, y):
	gd.blit(enmy,(x,y))
	#pygame.display.update()
    
def message(mess,colour,size,x,y):
	font=pygame.font.SysFont(None,size)
	screen_text=font.render(mess,True,colour)
	gd.blit(screen_text,(x,y))
	pygame.display.update()

def load(name,x_pos,y_pos):
	v = pygame.image.load(name)
	gd.blit(v, (x_pos, y_pos))
	pygame.display.update()

def quit1():
	pygame.quit()
	quit()
	
def button(x,y,w,h,mess,mess_color,actc,noc,size,tx,ty):
	mouse = pygame.mouse.get_pos()
	click=  pygame.mouse.get_pressed()
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gd, actc, [x, y, w, h])
		message(mess, mess_color, size, tx, ty)
		pygame.display.update()
		if click==(1,0,0):
			return True
			
	else:
		pygame.draw.rect(gd, noc, [x, y, w, h])
		message(mess, mess_color, size, tx, ty)
		pygame.display.update()
	pygame.display.update()

def game_intro():
	global time_exe
	global enemy_velocity

	load('screen.jpg', 0, 0)
	gameintro=False

	window_width = 800
	
	message('MAIN MENU',green,100,(window_width/2 - 220),100)
	while gameintro==False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					return 0
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					gameintro = True
		if button(100, 300, 125, 30, 'Jogo1 - Fácil', white, bright_red, red,25,106,306):
			time_exe = 10000
			enemy_velocity = 0.002
			return 1
		if button(100, 350, 125, 30, 'Jogo1 - Médio', white, bright_red, red,25,106,356):
			time_exe = 20000
			enemy_velocity = 0.005
			return 1
		if button(100, 400, 125, 30, 'Jogo1 - Difícil', white, bright_red, red,25,106,406):
			time_exe = 30000
			enemy_velocity = 0.008
			return 1
		if button(600, 400, 70, 30, 'Força', white, bright_green, green,25,606,406):
			return 2
	
	pygame.display.update()

	
def gameloop1():

	global cancel

	y = 300
	velocity = 0
	y_tree = y

	while not cancel:

		back()
		velocity = get_velocity(velocity)
		y += velocity * clock.get_time()
		y_tree += 10
		if velocity > 0:
			y_tree += 10*velocity * clock.get_time()

		car(525, 300)
		other_car(175, y)

		aux = y_tree
		if(aux > 890):
			aux -= 700
			y_tree -= 700
		trees(aux)
		
		if(y > 600):
			distance = str(int(y)-600)
			if(len(distance) >= 4):
				message(distance,black,50,187,560)
			if(len(distance) == 3):
				message(distance,black,50,197,560)
			if(len(distance) == 2):
				message(distance,black,50,209,560)
			if(len(distance) == 1):
				message(distance,black,50,219,560)
		
		if(y < -100):
			distance1 = (abs(int(y))-100)
			distance = str(distance1)
			if(len(distance) >= 4):
				message(distance,black,50,187,10)
			if(len(distance) == 3):
				message(distance,black,50,197,10)
			if(len(distance) == 2):
				message(distance,black,50,209,10)
			if(len(distance) == 1):
				message(distance,black,50,219,10)

		clock.tick(60)

		pygame.display.update()

def gameloop2():
	
	global current_force
	global cancel

	while not cancel:
		time.sleep(0.1)
		back2()

		get_muscle()
		if current_force < 0:
			current_force = 0

		message(str(abs(current_force - 2500)),red,480,10,20)
		message("Best:",bright_red,200,10,400)
		message(str(max_force - 2500),bright_red,200,350,400)
		
		pygame.display.update()


def get_muscle():
	global max_force
	
	if current_force > max_force:
		max_force = current_force

#server functions
def receive_values(unused_addr, *args):
	global accelerations
	global current_force
	global best_force
	global counter
	global cancel
	x, y, z = gravity_compensate(args[14:18], args[0:3])
	#print(x, y, z)
	accelerations.append({x, y, z})
	current_force = args[12]

	if current_force>best_force:
		best_force=current_force

	if int(pygame.time.get_ticks()) > time_exe:
		cancel = 1
		time.sleep(2)
		pygame.quit()
		os._exit(1)

def gravity_compensate(q, acc):
	g = [0.0, 0.0, 0.0]

	# get expected direction of gravity
	g[0] = 2 * (q[1] * q[3] - q[0] * q[2])
	g[1] = 2 * (q[0] * q[1] + q[2] * q[3])
	g[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]

	# compensate accelerometer readings with the expected direction of gravity
	return (acc[0] - g[0])*9.8, (acc[1] - g[1])*9.8, (acc[2] - g[2])*9.8

def filter_acceleration():
	global cancel
	global current_acceleration
	global accelerations
	f1 = open("log1.txt", "a")
	f2 = open("log2.txt", "a")
	while(not cancel):
		current_acceleration_aux = 0
		for acc in list(accelerations):
			aux_acc = 0
			for acc_coord in acc:
				aux_acc += acc_coord**2
			current_acceleration_aux += sqrt(aux_acc) / 100
		current_acceleration = current_acceleration_aux
		print('Acc: ', current_acceleration)
		profiler(f1, current_acceleration)
		profiler(f2, current_force)
	f1.close()
	f2.close()

def profiler(f, current):
	f.write(str(current) + '\n')

if __name__ == "__main__":
	f = open("log1.txt", "w")
	f.close()
	f = open("log2.txt", "w")
	f.close()
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", default="192.168.1.100", help="The ip to listen on")
	parser.add_argument("--port", type=int, default=8888, help="The port to listen on")
	args = parser.parse_args()

	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/*/raw", receive_values)

	current_acceleration = 0

	flag = game_intro()

	if flag == 1:
		x = threading.Thread(target=filter_acceleration)
		x.start()
		y = threading.Thread(target=gameloop1)
		y.start()
	elif flag == 2:
		w = threading.Thread(target=filter_acceleration)
		w.start()
		z = threading.Thread(target=gameloop2)
		z.start()
	elif flag == 0:
		print('Exit')
		quit()
	server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
	print("Serving on {}".format(server.server_address))
	server.serve_forever()
