import random
import pygame, sys
from pygame import display
from pygame.constants import K_DOWN, K_LEFT, K_UP
from direction import movement1
movement = 0
score = 0
start_pos = (300,300)
screen_width = 600
screen_height = 680
screen = pygame.display.set_mode((screen_width,screen_height))

class Snake(pygame.sprite.Sprite):
    movement = 10
    def __init__(self,Path) -> None:
        super().__init__()
        self.image = pygame.image.load(Path).convert_alpha()
        self.rect = self.image.get_rect()
        self.position = start_pos
        self.rect.center = self.position
        self.direction = 4

    def get_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
                self.movement = 0
        elif keys[pygame.K_DOWN]:
            self.movement = 1
        elif keys[pygame.K_LEFT]:
            self.movement = 2
        elif keys[pygame.K_UP]:
            self.movement = 3
        if abs(self.direction - self.movement) != 2:
            self.direction = self.movement
            

    def update_position(self):
        if self.direction == 0:
            self.position = (self.position[0] + 14 , self.position[1])
        elif self.direction == 1:
            self.position = (self.position[0], self.position[1] + 14)
        elif self.direction == 2:
            self.position = (self.position[0] - 14 , self.position[1])
        elif self.direction == 3:
            self.position = (self.position[0], self.position[1] - 14)

    def reset(self):
        if( self.position[0] > screen_width):
            self.position = (14 , self.position[1])
        elif self.position[0] < 0:
            self.position = (screen_width - 14 , self.position[1])
        elif self.position[1] > screen_height:
            self.position = (self.position[0] , 94)
        elif self.position[1] < 80:
            self.position = (self.position[0] , screen_height-14)

    def update(self):
        self.rect.center = self.position


class Body(pygame.sprite.Sprite):
    length = 0
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("2.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.position = (13,13)
        self.array = []

        

    def update_body_part(self):
        self.rect.center = self.position



class Food(pygame.sprite.Sprite):
    variable = 7
    display_condition = False
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('11.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.display_condition = False
    

    def generate(self):
        self.rect.center = (random.randint(1,600),random.randint(80,600))
        self.display_condition = True

    


    
    
    


# Updating snake body
def update_body():

    first_term = True
    for x in body_group:
        
        if first_term == True:
            variable = x.position
            first_term = False
        else:
            temp = x.position
            x.position = variable
            variable = temp
    first_body.position = snake.position
    for x in body_group:
        x.update_body_part()            
        

        
   
    



pygame.init()
clock = pygame.time.Clock()
body_group = pygame.sprite.Group()

# Collision
first_body = Body()

def collision_food():
    if Body.length == 0:
        body_group.add(first_body)
        Body.length += 1
    else:
        body_group.add(Body())
        Body.length += 1
    food.display_condition = False


# def collision_food():
#         food.collided()
#         if Body.length == 0:
#             Body.length += 1
#         else:
#             body_group.add(Body())
#             Body.length += 1
text_font = pygame.font.Font('comic.ttf',50)
display_screen = pygame.Rect(0, 0, 600, 80)
text_font_50 = pygame.font.Font('comic.ttf',50)
title = text_font_50.render('Snake Game',True,'Green')
text_font_25 = pygame.font.Font('comic.ttf',25)
score_display = text_font_25.render(f'Score = {score}',True,'Green')
restart_text = text_font_25.render('Press SpaceBar to Restart or ESC to exit',True,'Blue')

        
    

        
        

class Walls(pygame.sprite.Sprite):
    def __init__(self,position_x,position_y) -> None:
        super().__init__()
        self.image = pygame.image.load("1.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.position = (position_x,position_y)

    def set_walls(self):
        self.rect.center = self.position
walls_group = pygame.sprite.Group()


def create_blocks_position(count,initial_x,initial_y,x_increament,y_increament):
    for i in range(count):
        x = initial_x + (x_increament * i)
        y = initial_y + (y_increament * i)
        walls_group.add(Walls(x,y))

create_blocks_position(29,107,87,14,0)
create_blocks_position(29,107,673,14,0)
create_blocks_position(29,593,187,0,14)
create_blocks_position(29,7,187,0,14)
create_blocks_position(8,402,207,14,0)
create_blocks_position(8,100,573,14,0)
create_blocks_position(7,500,221,0,14)
create_blocks_position(7,100,559,0,-14)

for x in walls_group:
    x.set_walls()







game_status = True
# Initiating Screen and background
background = pygame.image.load("grass.jpg").convert()

food = Food()
food_group = pygame.sprite.GroupSingle()
food_group.add(food)


snake = Snake('3.jpg')
snake_group = pygame.sprite.GroupSingle()
snake_group.add(snake)

Blue = (0,0, 255)
white = (255,255,255)
start_time = 0
time_to_chase = random.randint(17,25)
time_not_eaten = random.randint(7,15)
time_ate = random.randint(7,15)

counter = 0
run_condition = True
while run_condition:
    if game_status == True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(white)
        
        walls_group.draw(screen)
        pygame.draw.rect(screen,Blue,display_screen)
        screen.blit(title,(30,0))
        screen.blit(score_display,(400,45))
        pygame.display.flip()
        pygame.display.update()
        
        #food_group.update()
        curr_time = int(pygame.time.get_ticks() / 1000)

        if food.display_condition == True:
            if snake.rect.colliderect(food.rect):
                start_time = curr_time
                score += 1
                Food.variable = random.randint(5,15)
                collision_food()
            elif curr_time - start_time > time_to_chase:
                food.display_condition = False
                Food.variable = random.randint(5,15)
                time_to_chase = random.randint(17,25)
                start_time  = curr_time
        else:
            if curr_time - start_time > Food.variable:
                start_time = curr_time
                food.generate()
        if Body.length > 0:
            update_body()
            body_group.draw(screen)
        if food.display_condition == True:
            food_group.draw(screen)
        
        snake.get_direction()
        snake.update_position()
        snake.reset()
        snake.update()
        
        snake_group.draw(screen)
        if pygame.sprite.spritecollide(snake, body_group, False):
            game_status = False

        pygame.display.flip()
        clock.tick(30)
    else:
        screen.fill(white)
        pygame.draw.rect(screen,Blue,display_screen)
        screen.blit(title,(30,0))
        score = text_font_25.render(f'Score = {score}',True,'Green')
        screen.blit(score,(400,45))
        screen.blit(restart_text,(50,300))
        pygame.display.flip()
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_status = True
            score = 0
        elif keys[pygame.K_ESCAPE]:
            run_condition = False

