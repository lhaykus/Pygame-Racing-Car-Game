import pygame
#Utils file to have funtcions in 

#RESIZING images funciton
#factor-scale in which image is increased/decreased
def scale_image(img, factor):
    #creating new size of image to be width, height * factor
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    #returning the img as the new size
    return pygame.transform.scale(img, size)