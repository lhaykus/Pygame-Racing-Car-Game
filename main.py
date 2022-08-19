#importing packages
from ctypes import c_char_p
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
#Masks- used to see if pixels in the rectangles of pygame are colliding
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

#load finish line image
FINISH = pygame.image.load('images/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 230)

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
# points created for the computer car
PATH = [(166, 104), (91, 87), (69, 474), (326, 727), (410, 551), (575, 502), (612, 700), (756, 657), (730, 382), (404, 339), (484, 246), (743, 218), (707, 82), (334, 78), (274, 369), (174, 321), (164, 233)]

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

    #move backwards
    def move_backward(self):
        #subrtacting velocity when going backwards
        #want maximum negative velcoity to be 1/2 the forward velocity- making sure when going in reverse
        #there is a max speed and youre going slower than if you were going forwards like a real car
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    #function to move car
    def move(self): 
        # using radians to calculate angles (360 = 2pi, 180 = pi)
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical 
        self.x -= horizontal

    #function to tell if images are colliding
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        #calculate offset x and offset y, use interger for offset
        #offset relative to calling mask
        #using the current x and y position and subtracting the x and y from the other calling mask that gives displatment between both masks
        offset = (int(self.x - x), int(self.y - y))
        #poi = point of intersection
        poi = mask.overlap(car_mask, offset)
        #if poi returned = collison occured, otherwise there was no collusion
        return poi





#Creating new class for PlayerCar, refering and using code from AbstractCar, setting player image 
class PlayerCar(AbstractCar):
    #setting class image
    IMG = PURPLE_CAR
    START_POS = (180, 180)

    #method to reduce speed when not pressing key
    def reduce_speed(self):
        # when speed decreases, velocity is reduced by half of the acceleration and car moves
        # stop at 0 so car isnt moving backwards
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    #method for when car bounces off wall to throw car back in direction it hit from
    def bounce(self):
        #reverse the velocity so car will be thrown oppostie direction
        #if car is going backwards and vel is -, the vel now becomes + and throws car forward
        #if car is going forward and hits wall, vel is +, the vel becomes - and throws car backwards
        self.vel = -self.vel
        self.move()

    #reset cars position to prepare for next level
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

# Class for computer car
class ComputerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (150, 180)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        # path = the path the computer car will take
        self.path = path
        self.current_point = 0
        # will start at max_vel at move at that speed the entire time
        self.vel = max_vel

#allows us to click and draw points for the computer car to follow
    def draw_points(self, win):
        for point in self.path:
            # draw a cirlce, color = red, draw at point, radius of 5
            pygame.draw.circle(win, (255,0,0), point, 5)

#draw all points in the path for computer car to follow
    def draw(self, win):
        super().draw(win)
    #    self.draw_points(win)

# calculate displacement in X and Y between the target point and current position
# once displacement is found, then the angle between car and the point will be found
# car direction can then be adjusted to move towards target point
    def calculate_angle(self):
        # getting current point
        target_x, target_y = self.path[self.current_point]
        # finding the difference between target x and y and current position x and y
        x_diff = target_x - self.x
        y_diff = target_y - self.y

# if y = 0, manually set angle 
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else: 
            #give angle between car and target point
            desired_radian_angle = math.atan(x_diff/y_diff)
# if angle of target point is lower on screen that current y position, the turn needed to make is more extreme that what the angle is 
# add math.pi to make sure car is turnign into right direction
        if target_y > self.y:
            desired_radian_angle += math.pi

# convert angle from radians to degrees and take current angle and subtract desired angle, if negative turn left, if positive turn right 
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
       #if angle to turn is greater than 180, subrtract 360 from the angle to get the negative angle to move in the opposite direction at less degrees
       # example: if left = 220 degrees, but right is 140 degrees, subrtract 220 -360 = -140 to move to the right 140 degrees instead of haviong to go a full 220
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            # if difference in angle is less than rotation velocity well move by that amount
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        # creating a rectangle from left top point of car and getting width and height to see if any collisions are happeing with that rectangle
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
     # will tell if target is being collided with, takes X and Y coordinates
        if rect.collidepoint(*target):
            # if current point is hit go to next point
            self.current_point += 1


# checking to make sure car is in right directoin and facing right angle to move forward
    def move (self): 
        if self.current_point >= len(self.path):
            return
            # calculate angle for computer car to move to 
        self.calculate_angle()
        # check to see if car needs to move to next point
        self.update_path_point()
        super().move()





#draw funciton takes window to draw on and images you want to draw
def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player(player_car):
     #ROTATE the car while pressing keys
    keys = pygame.key.get_pressed()
    moved = False
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
            moved = True
            player_car.move_forward()
    if keys[pygame.K_s]:
            moved = True
            player_car.move_backward()
    # when not pressing on gas (w key) the speed is reduced
    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car):
    
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

# when computer car hits finish line 
    computer_finish_poi_collide  = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        player_car.reset()
        computer_car.reset()


    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    # split the tuple that stores position, Xand Y and stores as individual coordinates and passes this to the function as two arguments
    # be the same as saying FINISH_POSITION(180, 200)
    if player_finish_poi_collide != None:
        #if the y axis of point of intersection is 0 that means that the car hit the finish line from the back (didnt go throuhgt whole course)
        # so have car bounce off to make player go through whole course
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()

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
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
#set player car as playercar class, pass max veolcity and rotation velocity
player_car = PlayerCar(4, 4)
# passing PATH in computer car so the car will follow the created path
computer_car = ComputerCar(4, 4, PATH)

while run:
    #setting max FPS that the while loop can run 
    clock.tick(FPS)

    #draw in images
    draw(WIN, images, player_car, computer_car)


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

#method to allow us to click and create points for path of computer car
        #if event.type == pygame.MOUSEBUTTONDOWN:
          #  pos = pygame.mouse.get_pos()
          #  computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car)

#print out computer car path to have code to use later
print(computer_car.path)
pygame.quit()