#importing requiered libraries
import cv2 as cv
import numpy as np
import pygame
import random

from pygame.display import set_caption

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
font = cv.FONT_HERSHEY_SIMPLEX


# Code for Snake
width = 600
height = 680
pygame.init()
set_caption("Stylus Snake")
clock = pygame.time.Clock()
start_pos_x = 300
start_pos_y = 390
screen = pygame.display.set_mode((width,height))
head = pygame.image.load('3.jpg').convert_alpha()
head_rect = head.get_rect(center = (start_pos_x,start_pos_y))
body = pygame.image.load('2.jpg').convert_alpha()
body_rect = body.get_rect(center = (335,240))
food = pygame.image.load('11.jpg').convert_alpha()
food_rect = food.get_rect(center = (300,300))
position = [(start_pos_x,start_pos_y)]
rectangles = [head_rect]
movement = previous_movement = 33
counter = 0
condition = random.randint(50,80)
display_condition = False
exit_condition = True
grab_time = random.randint(150, 555)
rect_screen = pygame.Rect(0, 0, 600, 80)
text_font = pygame.font.Font('comic.ttf',50)
text_rect = text_font.render('Snake Game',True,'Green')
text_font = pygame.font.Font('comic.ttf',25)
after_text = pygame.font.Font('comic.ttf',25)
score = 0
score_rect = text_font.render(f'Score = {score}',True,'Green')
after_text_rect = after_text.render('Press SpaceBar to start or ESC to exit',True,'Blue')
game_status = False
blocks = pygame.image.load('1.jpg').convert_alpha()
def create_blocks(count,intial_x,intial_y,x_in,y_in):
    tempblock_rect = blocks.get_rect(center = (intial_x,intial_y))
    tempblock_rectangles = [tempblock_rect]
    for i in range(count):
        tempblock_rectangles.append(blocks.get_rect(center = (tempblock_rect.x + 7 + (x_in * (i + 1)),tempblock_rect.y + 7 + (y_in * (i + 1)))))
        print(tempblock_rect.x + 7 + (x_in * (i + 1)),tempblock_rect.y + 7 + (y_in * (i + 1)))
    return tempblock_rectangles
block_rectangles = [create_blocks(29,107,87,14,0)]
block_rectangles.append(create_blocks(29,107,673,14,0))
block_rectangles.append(create_blocks(29,593,187,0,14))
block_rectangles.append(create_blocks(29,7,187,0,14))
block_rectangles.append(create_blocks(7,402,207,14,0))
block_rectangles.append(create_blocks(7,100,573,14,0))
block_rectangles.append(create_blocks(6,500,221,0,14))
block_rectangles.append(create_blocks(6,100,559,0,-14))


screen_color = (255,255,255)
blue = (0,0,255)
while exit_condition:                        #comes out of the program when escape is pressed
    
    if game_status == True:
        
        
        screen.fill(screen_color)
        pygame.draw.rect(screen, blue, rect_screen)
        screen.blit(text_rect,(30,0))
        screen.blit(score_rect,(400,45))
               
        
        # Updating the postion array of the body
        length = len(position)
        limit = length - 1
        if(limit > 0):
            for i in range(limit):
                position[limit - i] = position[limit - i - 1]
        # Updating the postion of the head
        
        if movement == 0:
            position[0] = (position[0][0] + 14 , position[0][1])
            if( position[0][0] > width):
                position[0] = (14 , position[0][1])
        elif movement == 1:
            position[0] = (position[0][0], position[0][1] + 14)
            if position[0][1] > height:
                position[0] = (position[0][0] , 94)
        elif movement == 2:
            position[0] = (position[0][0] - 14 , position[0][1])
            if position[0][0] < 0:
                position[0] = (width - 14 , position[0][1])
        elif movement == 3:
            position[0] = (position[0][0], position[0][1] - 14)
            if position[0][1] < 80:
                position[0] = (position[0][0] , height-14)
        
        
        for i in range(length):
            rectangles[i].x = position[i][0]
            rectangles[i].y = position[i][1]
        
        
        
        for rect in rectangles:
            if(rect == head_rect):
                screen.blit(head,rect)
            else:
                screen.blit(body,rect)

        # Walll
        for B in block_rectangles:
            for x in B:
                screen.blit(blocks,x)
                if head_rect.colliderect(x):
                    game_status = False
                    display_condition = False
                    condition = random.randint(50,80)
                elif food_rect.colliderect(x):
                    display_condition = False
                    condition = counter
        # displaying food until its either eaten or the allowed time is finished
        if display_condition and counter < grab_time:
            screen.blit(food, food_rect)
            
        if display_condition and counter < grab_time and head_rect.colliderect(food_rect):
            position.append(position[length-1])
            rectangles.append(body.get_rect(center = position[length - 1]))
            display_condition = False
            condition = condition + random.randint(10,25)
            score = score + 1
            score_rect = text_font.render(f'Score = {score}',True,'Green')
            pygame.draw.rect(screen, blue, rect_screen)
            screen.blit(text_rect,(30,0))
            screen.blit(score_rect,(400,45))
            
        # Food Generation
        if counter == condition:
            food_rect.x = random.randint(15,width)
            food_rect.y = random.randint(115, height)
            condition = random.randint(50,80)
            counter = 0
            grab_time = random.randint(150, 185)
            display_condition = True
        for i in range (3,length):
            if head_rect.colliderect(rectangles[i]):
                game_status = False
                
        pygame.display.flip()
        pygame.display.update()
        counter = counter + 1
        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1)            #flipping the camera along the vertical axis
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #converting frame from bgr to hsv
        mask = cv.inRange(hsv, lower_red, upper_red)    #hsv thresholding
        #applying closing operation on mask to remove noise from the image
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) 
        #dilation is done to remove some of the dark spot inside the mask
        dilation_after_closing = cv.dilate(closing,kernel,iterations = 3)
        if (dilation_after_closing[:] == 255).any():                  #if there is object in the mask at least 1 white spot will be there only then proceed to find contours
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
        
        cv.line(frame,(80,0),(560,480),(0,0,0),5)
        cv.line(frame,(80,480),(560,0),(0,0,0),5)
        cv.putText(frame,'UP',(280,50), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'DOWN',(280,400), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'RIGHT',(420,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'LEFT',(100,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.imshow("Wireless Joystick!",frame)
        if game_status == False:
            position = [(start_pos_x,start_pos_y)]
            rectangles = [head_rect]
        for events in pygame.event.get():
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    key = 27
        if(key == 27):
            exit_condition = False
        clock.tick(100)
    else:
        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1) 
        cv.imshow("Wireless Joystick!",frame)
        screen.fill(screen_color)
        pygame.draw.rect(screen, blue, rect_screen)
        score_rect = text_font.render(f'Score = {score}',True,'Green') 
        screen.blit(text_rect,(30,0))
        screen.blit(score_rect,(400,45))
        screen.blit(after_text_rect,(50,300))
        pygame.display.flip()
        pygame.display.update()
        key = cv.waitKey(1)
        for events in pygame.event.get():
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    key = 27
                elif(events.key == pygame.K_SPACE):
                    game_status = True
                    score = 0
                    score_rect = text_font.render(f'Score = {score}',True,'Green')
                    after_text_rect = after_text.render('Press SpaceBar to Restart or ESC to exit',True,'Blue')

        if(key == 27):
            exit_condition = False
        elif key == 32:
            game_status = True
            score = 0
            score_rect = text_font.render(f'Score = {score}',True,'Green')
            after_text_rect = after_text.render('Press SpaceBar to Restart or ESC to exit',True,'Blue')

        
#releasing the capture and destroying all the windows
cap.release()
cv.destroyAllWindows()