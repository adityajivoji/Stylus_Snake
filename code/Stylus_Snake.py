#importing requiered libraries
import cv2 as cv
import numpy as np
import pygame
import random

img = np.zeros((480, 640, 3), np.uint8) #creating an image which is the drawing space
cv.bitwise_not(img,img)                 #turning all the zeros to 1s so that drawing pad is white(optional)
cp = np.copy(img)                       #copying this image to clear the drawing canvas(optional)
cap = cv.VideoCapture(0 + cv.CAP_DSHOW) #capturing video (+ cv.CAP_DSHOW is only used if using only 0 doesn't work)
#these are the lower and upper limits of hsv values identified create a mask of stylus
lh = 158
ls = 101
lv = 90
uh = 179
us = 255
uv = 255
lower_red = np.array([lh, ls, lv])      #creating the array for hsv thresholding
upper_red = np.array([uh, us, uv])
kernel = np.ones((3, 3), np.uint8)      #this is the kernel for passing while "closing" and dilation
ncx = ncy=  2300000                     #assigning these value so that there is no condition check everytime for 1st and2nd iteration
key = 0                                 #condition for entering into the loop

# Code for Snake
pygame.init()
clock = pygame.time.Clock()
start_pos_x = 330
start_pos_y = 240
screen = pygame.display.set_mode((600,700))
head = pygame.image.load('3.jpg').convert_alpha()
head_rect = head.get_rect(center = (320,240))
body = pygame.image.load('2.jpg').convert_alpha()
body_rect = body.get_rect(center = (335,240))
food = pygame.image.load('1.jpg').convert_alpha()
food_rect = food.get_rect(center = (300,300))
position = [(start_pos_x,start_pos_y)]
rectangles = [head_rect]
movement = previous_movement = 33
counter = 0
condition = random.randint(1,50)
display_condition = False
exit_condition = True
grab_time = random.randint(150, 555)
rect_screen = pygame.Rect(0, 0, 600, 100)
text_font = pygame.font.Font('comic.ttf',50)
text_rect = text_font.render('Snake Game',False,'Green')
text_font = pygame.font.Font('comic.ttf',25)
score = 0
score_rect = text_font.render(f'Score = {score}',False,'Green')
game_status = False
while exit_condition:                        #comes out of the program when escape is pressed
    if game_status == True:
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0,0,255), rect_screen)
        screen.blit(text_rect,(30,0))
        screen.blit(score_rect,(400,50))
        pygame.display.flip()
        # displaying food until its either eaten or the allowed time is finished
        if display_condition and counter < grab_time:
            screen.blit(food, food_rect)
        # Updating the postion array of the body
        length = len(position)
        limit = length - 1
        if(limit >= 1):
            for i in range(limit):
                position[limit - i] = position[limit - i - 1]
        # Updating the postion of the head
        
        if movement == 0:
            position[0] = (position[0][0] + 15 , position[0][1])
        elif movement == 1:
            position[0] = (position[0][0], position[0][1] + 15)
        elif movement == 2:
            position[0] = (position[0][0] - 15 , position[0][1])
        elif movement == 3:
            position[0] = (position[0][0], position[0][1] - 15)
        
        if( position[0][0] > 600):
            position[0] = (7 , position[0][1])
        elif position[0][0] < 0:
            position[0] = (593 , position[0][1])
        elif position[0][1] > 700:
            position[0] = (position[0][0] , 107)
        elif position[0][1] < 100:
            position[0] = (position[0][0] , 693)
        else:
            pass
        for i in range(length):
            rectangles[i].x = position[i][0]
            rectangles[i].y = position[i][1]
        
        
        
        for rect in rectangles:
            if(rect == head_rect):
                screen.blit(head,rect)
            else:
                screen.blit(body,rect)
        
            
        if display_condition and counter < grab_time and head_rect.colliderect(food_rect):
            position.append(position[length-1])
            rectangles.append(body.get_rect(center = position[length - 1]))
            display_condition = False
            condition = condition + random.randint(1,25)
            score = score + 1
            score_rect = text_font.render(f'Score = {score}',False,'Green')
            pygame.draw.rect(screen, (0,0,255), rect_screen)
            screen.blit(text_rect,(30,0))
            screen.blit(score_rect,(400,50))
            
        # Food Generation
        if counter == condition:
            food_rect.x = random.randint(1,600)
            food_rect.y = random.randint(100,700)
            condition = random.randint(50,80)
            counter = 0
            grab_time = random.randint(150, 185)
            display_condition = True
        for i in range (3,length):
            if head_rect.colliderect(rectangles[i]):
                game_status = False
        
        pygame.display.update()
        counter = counter + 1
        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1)            #flipping the camera along the vertical axis
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #converting frame from bgr to hsv
        mask = cv.inRange(hsv, lower_red, upper_red)    #hsv thresholding
        if (mask[:] == 255).any():                  #if there is object in the mask at least 1 white spot will be there only then proceed to find contours
            #applying closing operation on mask to remove noise from the image
            closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) 
            #dilation is done to remove some of the dark spot inside the mask
            dilation_after_closing = cv.dilate(closing,kernel,iterations = 3)
            contours, _ = cv.findContours(dilation_after_closing, 1, 2) #detecting contours
            areas = [cv.contourArea(c) for c in contours]   #finding areas of all the contourand putting them in a list
            #finding the index of the largest contour in the above list
            cnt=contours[np.argmax(areas)]
            #using the contour with larget area to draw it on the original frame
            M = cv.moments(cnt)                             #finding moments and centroid of the largest contour
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #copying the values of the old coordinated for the end points of next line
            diffx = cx - 320
            diffy = cy - 240
            absx = abs(diffx)
            absy = abs(diffy)
            if(absx > 30 or absy > 30):
                previous_movement = movement
                if absx > absy:
                    if diffx > 0:
                        movement = 0
                    else:
                        movement = 2
                else:
                    if diffy < 0:
                        movement = 3
                    else:
                        movement = 1
                if(abs(previous_movement - movement) == 2):
                    movement = previous_movement
        key = cv.waitKey(1)             #waiting for one millisecond for some input from the user
        if key == 97:                   #if the user gave 'a' as the input the the canvas is cleared(optional)
            img = np.copy(cp)
        for events in pygame.event.get():
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    key = 27
        if(key == 27):
            exit_condition = False
        cv.line(frame,(80,0),(560,480),(0,0,0),5)
        cv.line(frame,(80,480),(560,0),(0,0,0),5)


        cv.imshow("Frame",frame)
    else:
        pass
        


#releasing the capture and destroying all the windows
cap.release()
cv.destroyAllWindows()
