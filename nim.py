'''
Author: Ian Gibson
Last Change: 3/12/2015
Description: The game of Nim with both single and two player modes.
    This will be expanded in the future to include a GUI and other
    interesting features (possibly a 2D mode).

    How to play: The game is initialized with a number of stacks (usually 3)
    containing values. Players take turns subtracting some value from any
    non-empty stack. The player who is forced to make the last move is the loser.

'''
from graphics import *
from functools import reduce
import sys

stacks = list()

def main():
    print("NIM! Take turns removing numbers from the stacks.\nDon't be the last one to make a move!")
    num_players = int(input("One or two players? "))
    stacks.extend(list(map(int, input("Enter the initial values for the stacks: ").split())))

    if num_players == 1:
        single_player()
    if num_players == 2:
        two_player()

        
def single_player():
    print(stacks)
    
    while (True):
        print('Your turn!')
        make_move(*get_move_user())
        print(stacks)
        if end_condition():
            print('You win!')
            break
        make_move(*get_move_computer())
        print('Computer moves...')
        print(stacks)
        if end_condition():
            print('You lose!')
            break

def two_player():
    x, y = 2, 1
    print(stacks)
    
    while (not end_condition()):
        x, y = y, x
        print('Player ' + repr(x) + '\'s turn!')
        make_move(*get_move_user())
        print(stacks)

    print('Player ' + repr(x) + ' wins!')


def get_move_user():
    stack_num, num_taken = map(int, input("Which stack and how much? ").split())
    stack_num -= 1
    return stack_num, num_taken
    
def get_move_computer():
    x = nim_sum()
    if x == 0:
        #the player has put themselves in a winning position
        #pick a stack and empty it, maybe they'll mess up? :)
        for i, stack in enumerate(stacks):
            if stack > 0:
                stack_num, num_taken = i, stack
                break
    else:
        #find a winning position
        #choose an initial stack
        sums = [s^x < s for s in stacks]
        stack_num = sums.index(True)
        num_taken = stacks[stack_num] - (stacks[stack_num]^x)

        #check for stacks that will value greater than 1 after the move
        stack_greater_than_one = 0
        for i, stack in enumerate(stacks):
            if stack_num == i:
                n = stack - num_taken
            else:
                n = stack
            if n > 1:
                stack_greater_than_one += 1
                
        #if no stack greater than one will remain,
        #change move to one that leaves an odd number of 1-stacks
        if stack_greater_than_one == 0:
            stack_num = stacks.index(max(stacks))
            one_stacks = sum(t==1 for t in stacks)
            if one_stacks % 2 == 0:
                num_taken = stacks[stack_num] - 1
            else:
                num_taken = stacks[stack_num]
                
    return stack_num, num_taken

def make_move(stack_num, num_taken):
    try:
        if stacks[stack_num] - num_taken < 0:
            raise ValueError
        else:
            stacks[stack_num] -= num_taken
    except ValueError as e:
        print("That value is too high")
        make_move(*get_move_user())
    
def nim_sum():
    return reduce(lambda x, y: x^y, stacks)

def end_condition():
    if sum(stacks) == 1:
        return True
    else:
        return False


main()

