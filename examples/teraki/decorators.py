#!/usr/bin/python

from functools import wraps
from time import time

#################################################################
################### Decorator Functions #########################
#################################################################

def timing(f):
    # create a decorator as a wrapper so that before the function call we get the time
    # after the function call we get the new time, so compute the elapsed time, and print it
    # also print out the result if the permutation is possible or not and the two words
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print 'Permutation possible {} in elapsed time: {} for {} vs {}'.format(int(result), end-start,args[0],args[1])
        return result
    # done inner function
    return wrapper
# done function
