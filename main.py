#importing packages
import pygame
import time
import math
#importing resizing image funciton from utils file
from utils import scale_image,blit_rotate_center

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
PURPLE_CAR = scale_image(pygame.image.load('images/purple-car.png'), 0.55 )
WHITE_CAR = scale_image(pygame.image.load('images/white-car.png'), 0.55)

#set up display screen to be same size as width and height as track
# get the width and height from track image
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
#creating window to view game - making window widht, height from track image
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#naming window
pygame.display.set_caption("Racing Game!")

#setting frames per second
FPS = 60

# Setting up CLASS
# Abstract class - there will be a player car and a computer car, similiarities between the two will go in an abstract class
#Abstract class = meant to act as base class for other classes
class AbstractCar:
   
    # wanting to know max velocity and how quickly car can rotate
    def __init__(self, max_vel, rotation_vel) :
        self.img = self.IMG
        self.max_vel = max_vel
        #starting velocity = 0 because car is not moving 
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        # X and Y position of car
        self.x, self.y = self.START_POS
        # acceleration to move car
        # increase acceleration 0.1 pixels by second when pressing button
        self.acceleration = 0.1
#creating funciton to rotate car based on direction turning
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    #increase velocity of car based on acceleration 
    #when at max veloctiy car will move forward
    def move_forward(self):
        #if veloctiy is less than max_vel, increase velocity and acceleration
        #if max_vel is already met then move car forward
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    #function to move car
    def move(self): 
        #move in one direction
        #move to the right based on velocity
        self.x += self.vel



#Creating new class for PlayerCar, refering and using code from AbstractCar, setting player image 
class PlayerCar(AbstractCar):
    #setting class image
    IMG = PURPLE_CAR
    START_POS = (180, 200)


#draw funciton takes window to draw on and images you want to draw
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

#EVENT LOOPS
# Creating an event loop - event loop is a constant loop that handles all movement, events, etc.
#Set up main event loop to keep game 'alive' and running on screen adn then once game ends or user quits
# the screen, the loop is broken

run = True
# CLOCK - set up clock so that window is run at same speed on every computer
# pygames run automatically depending on processor of computer, creating a clock lets playeres play at same speed
#regardless of how slow/fast their processor is
clock = pygame.time.Clock()
#Creating list of images and what coordinates to draw them
images = [(GRASS, (0,0)), (TRACK, (0,0))]
#set player car as playercar class, pass max veolcity and rotation velocity
player_car = PlayerCar(4, 4)
while run:
    #setting max FPS that the while loop can run 
    clock.tick(FPS)

    #draw in images
    draw(WIN, images, player_car)


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

    #ROTATE the car while pressing keys
    keys = pygame.key.get_pressed()
        #if moving car left (pressing A key)
        # using WASD to move car
        # K_SPACE, K-SHIFT = move with space or shift key
    if keys[pygame.K_a]:
            player_car.rotate(left=True)
        #pressing D to move car to the right
    if keys[pygame.K_d]:
            player_car.rotate(right=True)
        #w key increase speed and moves car forward
    if keys[pygame.K_w]:
            player_car.move_forward()
    

pygame.quit()