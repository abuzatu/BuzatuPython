#!/usr/bin/python

import sys
import time
import itertools
from collections import Counter

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
verbose=True
list_pair=[
    # ("aab","bba"),
    # ("qwerty","wqeyrt"),
    # ("camel","tiger"),
    # ("cat","lion"),
    # ("abgty","tyagb"),
    # ("aab","aba"),
    # ("abgtyqwerty","tywqeyrtagb"),
    ("abgtaabgaja","tywqeyrtagb"),
    ("abgtaabgaja","aabgajbatag"),
    
]

list_algo=[
    "1",
    "2",
]

#################################################################
################### Functions ###################################
#################################################################

def checkPermutationsAlgo1(left,right):
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

def checkPermutationsAlgo2(left,right):
    # Algo1 has the disadvantage that one needs to calculate all the permutations first
    # Especially when they have a lot of duplications, we can do better
    # by counting the number of times each letter is in each word
    # if the two counts are equal, that is what it means that they are a permutation of each other
    counter_left=Counter(left)
    counter_right=Counter(right)
    # loop over the unique elements of each counter, and check if the element exists in the other counter
    # if not, return False
    # if yes, then compare the count numbers; if not the same, return False
    # if yes, continue

    for letter in counter_left:
        count_left=counter_left[letter]
        count_right=counter_right[letter]
        if debug:
            print "letter",letter,"count_left",count_left,"count_right",count_right
        if count_left != count_right:
            return False
    # done loop over all letters
    # if still here, we got all the letters matched to the same count
    # we can return True
    return True
# done function

def checkPermutationsPair(pair):
    if verbose:
        print "Start checkPermutations with pair",pair
    (left,right)=pair
    # if the two strings do not have the same name, they can not be one permutation of the other
    # so return False
    if len(left)!=len(right):
        if verbose or debug:
            print "The two strings have different lengths,",len(left),len(right),"so they can not be permutations of the other. Return False."
        return False
    else:
        if verbose or debug:
            print "The two strings have the same length, so we can proceed."
        length=len(left)
    # done if

    for algo in list_algo:
        start_time = time.time()
        if algo=="1":
            existPermutation=checkPermutationsAlgo1(left,right)
        elif algo=="2":
            existPermutation=checkPermutationsAlgo2(left,right)
        else:
            print "algo",algo,"not found. Choose 1 or 2. Will ABORT!!!"
            assert(False)
        # done if
        duration_seconds=time.time() - start_time
        string_time="--- %s seconds ---" % (duration_seconds)
        print "existPermutation is",int(existPermutation),"duration",string_time,"for pair",pair
    # done loop over algo

# done function

#################################################################
################### Run #########################################
#################################################################

for pair in list_pair:
    checkPermutationsPair(pair)
# done loop over pair

# done for loop over pairs

#################################################################
################### Finished ####################################
#################################################################

print ""
print ""
print "Finished all in",sys.argv[0]
