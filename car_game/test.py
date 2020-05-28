import pygame

import argparse
from math import sin, cos, radians, sqrt
import threading
import collections
import time

from pythonosc import dispatcher
from pythonosc import osc_server

pygame.init()

window_width=800
window_hight=600
gd=pygame.display.set_mode((window_width,window_hight))
carimg=pygame.image.load('car-clipart-sprite-sheet-14.jpg')
car1=pygame.transform.scale(carimg,(100,100))
enmy1=pygame.image.load('carroamarelo.jpg')
enmy=pygame.transform.scale(enmy1,(100,100))
tree1=pygame.image.load('tree.jpg')
tree=pygame.transform.scale(tree1,(50,50))
clock=pygame.time.Clock()

accelerations = collections.deque(maxlen=100)
current_acceleration = 0
cancel = False
alfa = 0.01
beta = 0.01

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

def car(x, y):
	gd.blit(car1,(x,y))
	#pygame.display.update()

def get_velocity(velocity):
	return current_acceleration * (1/60) * alfa + (1 - beta)*velocity - enemy_velocity

def other_car(x, y):
	gd.blit(enmy,(x,y))
	#pygame.display.update()
    
def message(mess,colour,size,x,y):
	font=pygame.font.SysFont(None,size)
	screen_text=font.render(mess,True,colour)
	gd.blit(screen_text,(x,y))
	pygame.display.update()

def gameloop():

	global cancel

	y = 300
	velocity = 0

	while not cancel:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				cancel = True

		back()
		message(str(clock.get_fps()),(0,0,0),50,187,560)

		y += get_velocity(velocity) * clock.get_time()
		car(525, 300)
		other_car(175, y)
		
		# if(y > 600):
		# 	distance = str(int(y)-600)
		# 	if(len(distance) >= 4):
		# 		message(distance,black,50,187,560)
		# 	if(len(distance) == 3):
		# 		message(distance,black,50,197,560)
		# 	if(len(distance) == 2):
		# 		message(distance,black,50,209,560)
		# 	if(len(distance) == 1):
		# 		message(distance,black,50,219,560)
		
		# if(y < -100):
		# 	distance1 = (abs(int(y))-100)
		# 	distance = str(distance1)
		# 	if(len(distance) >= 4):
		# 		message(distance,black,50,187,10)
		# 	if(len(distance) == 3):
		# 		message(distance,black,50,197,10)
		# 	if(len(distance) == 2):
		# 		message(distance,black,50,209,10)
		# 	if(len(distance) == 1):
		# 		message(distance,black,50,219,10)

		clock.tick(60)

		pygame.display.update()

def receive_values(unused_addr, *args):
     global accelerations
     x, y, z = gravity_compensate(args[14:18], args[0:3])
     #print(x, y, z)
     accelerations.append({x, y, z})

     if cancel:
          pygame.quit()
          quit()


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
     while(not cancel):
          current_acceleration = 0
          for acc in accelerations:
               aux_acc = 0
               for acc_coord in acc:
                    aux_acc += acc_coord**2
               current_acceleration += sqrt(aux_acc) / 100
          print('Acc: ', current_acceleration)

if __name__ == "__main__":
     try:
          parser = argparse.ArgumentParser()
          parser.add_argument("--ip", default="192.168.1.100", help="The ip to listen on")
          parser.add_argument("--port", type=int, default=8888, help="The port to listen on")
          args = parser.parse_args()

          dispatcher = dispatcher.Dispatcher()
          dispatcher.map("/*/raw", receive_values)

          current_acceleration = 0

          x = threading.Thread(target=filter_acceleration)
          x.start()

          y = threading.Thread(target=gameloop)
          y.start()

          server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
          print("Serving on {}".format(server.server_address))
          server.serve_forever()
     except KeyboardInterrupt:
          cancel = 1
          quit()