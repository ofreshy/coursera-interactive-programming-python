# http://www.codeskulptor.org/#user40_TFbFENC5CJ29TQ6.py

import math
import random

import simplegui
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

num_range = 100
guesses_left = 7
secret_number = None

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, number_guesses
    
    secret_number = random.randrange(num_range)
    set_range_and_guesses(num_range)
    print " \n New Game! "
    print "Play range is [0-%d) and you got %d guesses" % (num_range, guesses_left) 


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    set_range_and_guesses(100)
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    set_range_and_guesses(1000)
    new_game()

def set_range_and_guesses(r):
    global num_range, guesses_left
    num_range = r
    guesses_left = int(math.ceil(math.log(r, 2)))
    
    
def input_guess(guess):
    # main game logic goes here
    global guesses_left
    print ""
    last_guess = (guesses_left == 1)
    if last_guess:
        print "Last guess!"
    else:    
        print "You got %d guesses left" % guesses_left
    
    guess = int(guess)
    print "Player guessed %d" % guess
    if secret_number == guess:
        print "Correct!"
        new_game()
        return
    
    if last_guess:
        print "Game over. The number was %d" % secret_number
        new_game()
        return
    
    # We are still playing
    guesses_left -= 1
    if secret_number > guess:
        print "Higher!"
    else:   
        print "Lower!"
    
# create frame
frame = simplegui.create_frame("GuessTheNumber", 200, 200)


# register event handlers for control elements and start frame
frame.add_button("range100", range100, 200)
frame.add_button("range1000", range1000, 200)
frame.add_input("Enter a Guess", input_guess, 200)


# call new_game 
new_game()

frame.start()


# always remember to check your completed program against the grading rubric
