#!/usr/bin/python

import functools
import time

#################################################################
################### Decorator Functions #########################
#################################################################

def timing(f):
    """Print the timing for the function"""
    # create a decorator as a wrapper so that before the function call we get the time
    # after the function call we get the new time, so compute the elapsed time, and print it
    # also print out the result if the permutation is possible or not and the two words
    @functools.wraps(f) # preserves information about the original function
    def wrapper(*args,**kwargs):
        start=time.time()
        result=f(*args,**kwargs)
        end=time.time()
        print "Permutation possible {} for function {} in elapsed time {} for {} vs {}".format(
            int(result),f.__name__, end-start,args[0],args[1])
        return result
    # done inner function
    return wrapper
# done function

def debugging(f):
    """Print the function signature and return value"""
    # create a decorator as a wrapper so that befor teh function call prints the arguments 
    # and after the function call the returned value
    @functools.wraps(f)
    def wrapper_debug(*args, **kwargs):
        args_repr=[repr(a) for a in args]
        kwargs_repr=["{k}={v!r}" for k, v in kwargs.items()]
        signature=",".join(args_repr + kwargs_repr)
        print "Start function {}({}).".format(f.__name__,signature)
        result=f(*args, **kwargs)
        print "End   function {}({}). Returned {}.".format(f.__name__,signature,result)
        return result
    # done inner function
    return wrapper_debug
# done function
