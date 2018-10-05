#!/usr/bin/python

import sys
import itertools
import time

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

#You are given two strings.  Write a Python function which would check
#if one of them can be obtained from the other simply by permutation of
#characters.  The function should return True if this is possible and False
#if it is not possible.  Example:  for the pair (qwerty, wqeyrt) it should
#return True and for the pair (aab, bba) it should return False.

#################################################################
################### Configurations ##############################
#################################################################

debug=False
verbose=False
list_pair=[
    # ("aab","bba"),
    # ("qwerty","wqeyrt"),
    # ("camel","tiger"),
    # ("cat","lion"),
    # ("abgty","tyagb"),
    ("abgtyqwerty","tywqeyrtagb"),
]

#################################################################
################### Functions ###################################
#################################################################

def checkPermutations(pair):
    if debug:
        print "Start checkPermutations with pair",pair
    (left,right)=pair
    # if the two strings do not have the same name, they can not be one permutation of the other
    # so return False
    if len(left)!=len(right):
        if verbose or debug:
            print "The two strings have different lengths, so they can not be permutations of the other. Return False."
        return False
    else:
        if verbose or debug:
            print "The two strings have the same length, so we can proceed."
        length=len(left)
    # done if

    # the simplest solution, brute force, the most inneficient, would be to
    # start with left and compute all the permutations possible
    # for each check if right is equal to one of the computed permutations
    # at the first match, return true, else continue to the next permutation
    #
    # we trust the permutation algorithm from Python 
    # that the permutations are computed in the most efficient way
    # in terms of memory and CPU
    iterator_permutations_left=itertools.permutations(left)
    for iterator in  iterator_permutations_left:
        if debug:
            print "iterator",iterator
        permutation_left=''.join(iterator)
        if debug:
            print "permutation_left",permutation_left
        if permutation_left==right:
            if verbose or debug:
                print "Found matching permutation, so return True."
            return True
        # done if
    # done for loop over permutations
    if verbose or debug:
        print "End of loop over permutations."
        print "if reached here, then no match was found, so return False."
    return False
# done function

#################################################################
################### Run #########################################
#################################################################

for pair in list_pair:
    start_time = time.time()
    existPermutation=checkPermutations(pair)
    duration_seconds=time.time() - start_time
    string_time="--- %s seconds ---" % (duration_seconds)
    print "existPermutation is",int(existPermutation),"duration",string_time,"for pair",pair
# done for loop over pairs

#################################################################
################### Finished ####################################
#################################################################

print ""
print ""
print "Finished all in",sys.argv[0]
