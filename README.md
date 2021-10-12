# Stylus_Snake

Play the traditional Stylus Snake game with the help of any object as the stylus

## Methods

* Using sprite class
* Without using sprite class

### Basic to Both the methods

* Use hsv backprojection to detect the object using numpy method
* Finding contour from the obtained mask
* Get the centoid value
* the camera is divided into four triangles
* if the triangle is in upper, lower, right, left triangle then snake moves upwards, downwards, rightwards, leftwards.


### Without using sprite class

* initalize and load requiered for the game to run
* creating walls
* reading the centroid
* Filling the screen with white color
* Adding title and score-board
* position is an array that stores positions of every part of the snake. If the snake has a body then it every part gets the position of its leading the element
* depending in the direction the snake goes the program checks if it crosses the maze boundaries and brings it back to the start point of the other side
* display the snake and check if the food generate collides with the snake body
* displaying the walls, also checking if food isn't on the walls
* displaying food until either snake eats or the chasing time is over
* cheking if the snake eat the food 
    * increasing the body length by 1
    * setting the display condition for food as False
    * increasing the time it will spawn the next food
    * increasing the score
    * updating the score
* generate food it counter = condition for generation
* checking if the head collided with any body part after the third part
* if the game_status turns False due to:
    * the collision of snake's head with the walls
    * the collision of snake's head with the body
this resets all the values to initial values
* If the game_status is False
    * the score gained is displayed with instruction
        * if the user pressed Esc the program exits
        * if the user pressed spacebar then the game restarts

### Using sprite class

* Creating Classes
    * snake head
        * includes the image rectangle
        * position
        * direction in which the snake moves. Initially set to 10 so that no movement takes place until stylus is detected
        * array with functions needed to change position and check if it the head crosses the boundaries
        * get_direction : a method to get the direction and change the position of the snake
        * zero, one, two, three are methods that change move the snake to new position
    * Body
        * includes the image rectangle
        * position of individual part initially set to 13, 13(just randomly)
    * Food
        * image rectangle
        * display condition
        * method generate: generates random position, sets display_condition to True
        * the generate function is called again if food lands on walls or body of the snake
    * walls
        * includes the image rectangle
        * position for individual walls

* function update_body : used to update position of every part to its leading part and first body part to the snakes position
* function collision food: used to increase length of body after it eats the food
* function create_walls create a line of walls given input as the number of walls in row, first block position (initial_x,initial_y) and the increament to this position for next block

* initialising all the varialbles requiered
* creating walls
* initializing time
* while game_stauts is true
    * fill screen, diplay game name, score and the walls 
    * finding the collision between the snake head and food
    * updating the body
    * getting snake direction and new position
    * showing snake body and head
    * finding collision between the snake and walls and snake and its body
    * using hsv backprojection to find the centroid of the stylus
    * drawing reference on the live video
    * game_status turns False when snake head collides with the body or when it collides with the wall
    * when pressed Esc the game is exited
* while game_status is False
    * frame window shows the live video
    * score gained is displayed
    * instrustion to restart the game or to exit is shown
    * press spacebar to restart and Esc to exit
    * all the values are reset when spacebar is pressed
    * it works for both when the current working window is the live feed or the game

## Notes

* first method does not have as many function as the second which makes the first code run faster.
* second method is structured and any changes can be made in the classes whereas the first method changes have to made in several places.
* The hsv projection doesn't give well results as compared to alloting proper hsv values with hsv calculator and using hsv thresholding.
* the previous versions use hsv thresholding if needed for reference
* for using a manual hsv calculator click [here](https://github.com/adityajivoji/manual_hsv_calc.git)
* The program uses opencv library for the input part. the capturing of the input takes a lot of time that is why the code may not work faster even if the f.p.s. is increased.
* The current f.p.s. is 8.3 when game_status is False and
