#importing packages
import pygame
import time
import math

#create variable and load in images
#GRASS = constant(not going to change)
#loading grass image from the images folder
GRASS = pygame.image.load('images/grass.jpg')

#loading track image from image folder
TRACK = pygame.image.load('images/track.png')

#loading track border image
TRACK_BORDER = pygame.image.load('images/track-border.png')

#load finish line image
FINISH = pygame.image.load('images/finish.png')

#load car images
PURPLE_CAR = pygame.image.load('images/purple-car.png')
WHITE_CAR = pygame.image.load('images/white-car.png')

#set up display screen to be same size as width and height as track
# get the width and height from track image
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
#creating window to view game - making window widht, height from track image
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#naming window
pygame.display.set_caption("Racing Game!")