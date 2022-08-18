#importing packages
import pygame
import time
import math
#importing resizing image funciton from utils file
from utils import scale_image



#create variable and load in images
#GRASS = constant(not going to change)
#loading grass image from the images folder
# scale_image 2.5 = resizing image by factor of 2.5
GRASS = scale_image(pygame.image.load('images/grass.jpg'), 2.5)

#loading track image from image folder
TRACK = scale_image(pygame.image.load('images/track.png'), 0.9)

#loading track border image
TRACK_BORDER = scale_image(pygame.image.load('images/track-border.png'), 0.9)

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

#setting frames per second
FPS = 60

#EVENT LOOPS
# Creating an event loop - event loop is a constant loop that handles all movement, events, etc.
#Set up main event loop to keep game 'alive' and running on screen adn then once game ends or user quits
# the screen, the loop is broken

run = True
# CLOCK - set up clock so that window is run at same speed on every computer
# pygames run automatically depending on processor of computer, creating a clock lets playeres play at same speed
#regardless of how slow/fast their processor is
clock = pygame.time.Clock()
while run:
    #setting max FPS that the while loop can run 
    clock.tick(FPS)

    #blit- used to draw image on screen
    #drawing image on window display screen
    # 0,0 = top left corner, as you go down screen Y increases, X increases as you go right
   #order of images drawn matter = GRASS then TRACK = track drawn over grass
    WIN.blit(GRASS, (0,0))
    WIN.blit(TRACK, (0,0))
    WIN.blit(FINISH, (0,0))

    #pygame allows items to be drawn onto screen and when this is run
    # what was drawn on screen will then be displayed 
    pygame.display.update()

    #get list of all events to loop through
    for event in pygame.event.get():
        #check to see if user closed window
        # if window has been closed, the loop is broken, the game is no longer running and so youd quit game
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit()