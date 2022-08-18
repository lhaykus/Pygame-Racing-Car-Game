import pygame
#Utils file to have funtcions in 

#RESIZING images funciton
#factor-scale in which image is increased/decreased
def scale_image(img, factor):
    #creating new size of image to be width, height * factor
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    #returning the img as the new size
    return pygame.transform.scale(img, size)

#Function to retrun rotated image based on angles
#Pygame is a rectangle and images are essentially rectangles within
#When rotating just the rectangle shape, morphing and dissortions can occur
def blit_rotate_center(win, image, top_left, angle):
    #rotate from top left 
    rotated_image = pygame.transform.rotate(image, angle)
    #rotate image without changing X,Y position of image on screen
    #get top left positon of original image, get the center of that 
    #new rectangle is = to the center of original image, so new image is rotating from center not top left 
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    #find X,Y of new rectangle 
    win.blit(rotated_image, new_rect.topleft)

   
  
    