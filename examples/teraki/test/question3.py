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
################### My additions ################################
#################################################################

# My additions: 
# Fill with with 2 the good (shortest) path.
# Fill with 9 the squares from the path explored to not be good.
# The solutions are equivalent if we go from one corner to the other or vice versa
# So let's choose a convention from top left (0,0) -> bottom right (7,7)
# When board given, first check it obbeys the rules of the program

#################################################################
################### My strategy #################################
#################################################################

# Brute force would be to calculate all the possible paths
# and if any compare them by length and pick the shortest

# But we want to find the result in the shortest amount of operations
# so we should not use brute force, but find a smarter shortcut
# We use a recursive function with a backtracking option.
# From every square, explore the four possible moves in a pre-defined order
# check for each if it is allowed (not forbidden, not out of the box, 
# and not one where we were there already and it was not good)
# if it is good, keep going and explore in the same order the possiblities
# hence recursiveness
# if road gets blocked, backtrack once, if all options blocked, backtrack again

#################################################################
################### Configurations ##############################
#################################################################

debug=False
verbose=False

N=8
NN=N*N

list_boardName=[
    "boardA",
    "boardB",
    "boardC",
    "boardD",
    "boardE",
]

dict_boardName_board={
    "boardA":np.array([
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ]),
    "boardB":np.array([
            [0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ]),
    "boardC":np.array([
            [0,0,1,0,1,0,0,0],
            [0,0,1,0,1,0,0,0],
            [0,0,0,0,1,0,0,0],
            [1,1,1,0,1,0,0,0],
            [0,0,0,0,1,0,0,0],
            [1,0,1,1,1,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,1,0,0,0,0,0],
            ]),
    "boardD":np.array([
            [0,0,1,0,0,0,1,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,1],
            [1,1,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0],
            ]),
    "boardE":np.array([
            [0,0,1,0,0,0,1,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,1],
            [1,1,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1],
            [0,0,0,0,0,1,0,0],
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
        if i!=N-1:
            result+="\n"
    return result
# done function

def drawBoard(title,board):
    print title
    print getBoardImage(board)
# done function

# @debugging
def checkCorrectnessBoard(board):
    '''Check that:
    o top left corner and bottom right corners are available (0)
    o all other squares are either available (0) or unvailable (1)
    '''
    if board[(0,0)]!=0:
        print "The starting point corner of top left (0,0), should be available with a value of 0. So board not correct."
        return False
    if board[(N-1,N-1)]!=0:
        print "The destination corner of bottom right (N-1,N-1), should be available with a value of 0. So board not correct."
        return False
    # done if
    for i in xrange(N):
        for j in xrange(N):
            position=(i,j)
            state=board[position]
            if debug:
                print "position","state",position,state
            if not (state==0 or state==1):
                if debug:
                    print "i={} j={} state={} not good, as it must be 0, or 1. So board not correct.".format(position[0],position[1],state)
                return False
            # done if
        # done loop over j
    # done loop over i
    return True
# done function

# @debugging
def isSquareAllowed(board,i,j):
    # skip the potential new position if 
    # - it is not on the board
    # - it is in a forbidden square
    if i<0 or i>N-1:
        # the horizontal (i) coordinate is outside of the board
        return False
    if j<0 or j>N-1:
        # the vertical (j) coordinate is outside of the board
        return False
    if board[i][j]==1:
        # it is a position not allowed on the board
        return False
    if board[i][j]>=2:
        # we already went here enough times, so avoid it, as you go in a loop
        return False
    # if here, the square is allowed
    return True
# done function

# @debugging
def solveRecursive(board,i,j,):
    if debug:
        drawBoard("Temp",board)
    if i==N-1 and j==N-1:
        # we reached the destination
        board[i][j]=2
        return True
    # done if
    if isSquareAllowed(board,i,j)==True:
        # go to that square
        board[i][j]=2
        # then try to go to neibourghs in all four directions
        # since in most situations a path towards right/down
        # is the most probable, with returns to left and up 
        # needed only if those paths are closed
        # we choose the order: right, down, up, left
        # if one finds the right path, then continues
        # from that square also with the same order of trials
        # hence a recursive function
        # check right
        if solveRecursive(board,i,j+1)==True:
            return True
        # check down
        if solveRecursive(board,i+1,j)==True:
            return True
        # check left
        if solveRecursive(board,i,j-1)==True:
            return True
        # check up
        if solveRecursive(board,i-1,j)==True:
            return True
        # if none of these (but one should work, so we should choose three that are not from the direction we come from)
        # then we need to come back, to back track, so it is a backtracking algorithm
        # so consider we did not come here
        board[i][j]=9
        return False
    # done if square is allowed
    return False
    # done if square is allowed
# done function

# @debugging
def solve(boardName):
    board=dict_boardName_board[boardName]
    correct=checkCorrectnessBoard(board)
    if correct==False:
        print "boardName",boardName,"is not correct, please amend it by reading the rules at the top of this file. Skipping this board."
        return None
    # done if
    print ""
    print "boardName="+boardName
    drawBoard("Initial board, with 1 for forbidden and 0 where we never went.",board)
    if solveRecursive(board,0,0)==False:
        # path does not exist, return False, or -1 as we are asked
        print "No solution exists, so return -1."
        return -1 
    # print solution
    drawBoard("Solution board with path shown in 2, and 9 where we went and was not good.",board)
    # it worked fine return 0
    return 0
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
