#!/usr/bin/python

import sys
from decorators import *
import numpy as np

total = len(sys.argv)
# number of arguments plus 1
if total!=1:
    print "You need some arguments, will ABORT!"
    print "Ex: ",sys.argv[0]," "
    assert(False)
# done if

#################################################################
################### Question ####################################
#################################################################

# On a chessboard 8x8 some of the squares are marked as available and some
# as unavailable. This information is given to you in a form of a numpy array
# which contains 1 in unavailable cells and 0 everywhere else.  Both upper
# left corner and bottom right corner are available.  You need to find the
# length of the shortest path from one corner to another which only passes
# through available cells or return -1 if such path does not exist.  Explain
# the idea of the algorithm or write the code in your favourite language.

# Diagonal moves are not allowed: 
# from the current cell one can move to one of the cells above, below, to the right, or the left, i.e.
# (x, y) -> (x+1, y)
# (x, y) -> (x-1, y)
# (x, y) -> (x, y+1)
# (x, y) -> (x, y-1)
# The length of the path is defined simply as the total number of moves.

#################################################################
################### My additions#################################
#################################################################

# My additions: 
# define the value of 2 the square with the current position
# and with the value of 3 the square with the past positions
# The solutions are equivalent if we go from one corner to the other or vice versa
# So let's choose a convention from top left (0,0) -> bottom right (7,7)

#################################################################
################### My strategy #################################
#################################################################

# Let's imagine the destinations is surrounded by forbidden squares (1).
# If we start from the first position we can compute a lot of paths
# But all of them are blocked in the end and we will have to return -1
# But we should also return -1 as fast as possible, with minimum CPU calculations
# This suggests it makes sense to start from the destination
# Now let's imagine the starting point is surrounded by forbidden squares (1)
# Then to find the result fast we should start from the first position.
# So maybe it does not matter where we start from

# No need to store the entire history of the travel in the form
# of a list of boards, since we choose to update 
# the previous position from 2 to 3
# following by eye the 3 values shows us the path so far
# one path would be final either when it can not proceed further
# so a value of 2 surrounded by either values of 1 or 3
# but allowing for some squares to still have a value of 0
# or when the value of 2 is at position of bottom right (N-1,N-1).

# Brute force would be to calculate all the possible paths
# and if any compare them by length and pick the shortest

# But we want to find the result in the shortest amount of operations
# so we should not use brute force, but find a smarter shortcut

#################################################################
################### Configurations ##############################
#################################################################

debug=True
verbose=False

N=3
NN=N*N
list_state=[0,1,2,3]

list_boardName=[
    "1",
]

dict_boardName_boardInitialState={
    "1":np.array([
            [ 2, 0, 0],
            [ 0, 1, 1],    
            [ 0, 0, 0],
            ]),
    }

#################################################################
################### Regular Functions ###########################
#################################################################

# @debugging
def getBoardImage(board):
    result=""
    for i in xrange(N):
        for j in xrange(N):
            if j!=0:
                result+=" "
            result+=str(board[i][j])
        result+="\n"
    return result
# done function

def drawBoard(board):
    print "board"
    print getBoardImage(board)
# done function

@debugging
def checkCorrectnessBoard(board,S):
    '''Check that:
    Board is the current state of the board at the current step S
    Initially S=0, and we must check the rules of the problem
    o top left corner is available (0) and piece is on the bottom right square (2)
    o bottom right corner is available (0) and the piece is on the top left quare (2)
    o all other squares are either available (0) or unvailable (1)
    For all other Steps S>0, past steps are marked as 3.
    '''
    if S<0:
        print "The number of steps S",S,"can no be negative. We will ABORT!!!"
        assert(False)
    elif S==0:
        if board[(0,0)]!=2:
            print "You did not place the piece at first in the top left corner at (0,0), with value 2. So board not correct."
            return False
    else:
        if board[(0,0)]!=3:
            print "The top left corner at (0,0), is a past position, so it should have a value of 3. So board not correct."
            return False
    if board[(N-1,N-1)]!=0:
        print "The destination corner of bottom right (N-1,N-1), should be available with a value of 0. So board not correct."
        return False
    # done if
    dict_state_count={state: 0 for state in list_state}
    for i in xrange(N):
        for j in xrange(N):
            position=(i,j)
            state=board[position]
            if debug:
                print "position","state",position,state
            if not (state==0 or state==1 or state==2 or state==3):
                if debug:
                    print "i={} j={} state={} not good, as it must be 0, 1, 2, 3. So board not correct.".format(position[0],position[1],state)
                return False
            # done if
            if state not in dict_state_count:
                dict_state_count[state]=1
            else:
                dict_state_count[state]+=1
            # done if
        # done loop over j
    # done loop over i
    # the piece should be in exactly one place
    if dict_state_count[2]>1:
        print "The piece is is more than one place, count of state 2 is more than 1. So board not correct."
        return False
    if dict_state_count[3]!=S:
        print "The count of past positions is different than the number of steps. So board not correct."
        return False
    # we could check that the forbidden places are same as before, but since we insure that in our update move we leave it out for now
    # as that would involve a lot of checks that would consume CPU
    if sum(dict_state_count.values())!=NN:
        print "The total count of values should be constant with the number of squares, i.e. N*N"
        return False
    # done if
    # if here, it means the board is initialized correctly, so return True
    return True
# done function

@debugging
def findAllowedMovesForOneSquare(i,j,board):
    list_tuple=[]
    # in principal the potential moves are done
    # horizontally and vertically by one unit
    # skip the potential new position if 
    # - it is the same position we started from
    # - it is not on the board
    # - it is in a forbidden square
    for i_current in i-1,0,i+1:
        if i_current<0 or i_current>N-1:
            # the horizontal (i) coordinate is outside of the board
            continue
        for j_current in j-1,0,j+1:
            if j_current<0 or j_current>N-1:
                # the vertical (j) coordinate is outside of the board
                continue
            if i_current==i and j_current==i:
                # is the same position we started from
                continue
            if board[i_current][j_current]==1:
                # it is a position not allowed on the board
                continue
            if board[i_current][j_current]==3:
                # it is a position where the piece was already
                # we want the shortest path
                # if going somewhere only to return
                # it means the path would not be the shortest possible
                # so declare that move not allowed
                continue
            if debug:
                print "These are selected as good potential moves: i_current","j_current",i_current,j_current
            list_tuple.append((i_current,j_current))
        # done for loop over j_current
    # done for loop over i_current
    return list_tuple
# done function

@debugging
def solve(boardName):
    boardInitialState=dict_boardName_boardInitialState[boardName]
    if debug:
        print "boardInitialState"
    drawBoard(boardInitialState)
    correct=checkCorrectnessBoard(boardInitialState,0)
    if correct==False:
        print "boardName",boardName,"with state",boardInitialState,"is not correct, please ammend it by reading the rules at the top of this file. Skipping this board."
        return None
    # done if
    drawBoard(boardInitialState)
    findAllowedMovesForOneSquare(0,0,boardInitialState)
# done function

#################################################################
################### Run #########################################
#################################################################

for boardName in list_boardName:
    solve(boardName)
# done loop over boardName

#################################################################
################### Finished ####################################
#################################################################

print ""
print ""
print "Finished all in",sys.argv[0]
