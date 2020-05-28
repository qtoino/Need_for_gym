# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:19:31 2019

@author: frs98
"""

import pygame
import sys
import time
import random
pygame.init()

#color
gray=(119,118,110)
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
redi=(220,150,50)
green=(0,200,0)
blue=(0,0,255)
bright_red=(255,0,0)
bright_green=(0,255,0)
window_width=800
window_hight=600

#display surface
gd=pygame.display.set_mode((window_width,window_hight))
clock=pygame.time.Clock()

def back():
    blue_strip=pygame.image.load('screen.jpg')
    img=pygame.transform.scale(blue_strip,(800,600))
    gd.blit(img,(0,0))

def message(mess,colour,size,x,y):
	font=pygame.font.SysFont(None,size)
	screen_text=font.render(mess,True,colour)
	gd.blit(screen_text,(x,y))
	#pygame.display.update()

#def find_biggest(file):
	

def gameloop():
	
	game_over=False

	while game_over==False:
		back()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_over=True

		message("0546",red,480,10,20)
		message("Best:",redi,200,10,400)
		message("1120",redi,200,350,400)
		
		
		pygame.display.update()


gameloop()
pygame.quit()
quit()