#!/usr/bin/python
from HelperPython import *
# to parse xml files
import xml.etree.ElementTree as ET
# to arrange visually better the output of nested dictionaries
import pprint 
# time
import time
# numpy
import numpy as np

# re-implement on 19 June 2019 the example from https://github.com/tsoding/kdtree-in-python/blob/master/main.py
# to add here the aspects of the brute force with tolerances, as this file compares brute force with KDTree
# later to update the KDTree method to also take into account the tolerances
# first on x,y, then on x,y,i, and after that also build the kdtree from x,y,i
# then added three things: 
# 1. attributes, in addition to the coordinates
# 2. tolerances for each of the coordinates and attributes - can be none and then come back to standard case
# 3. any number of dimensions for both coordinates and attributes

total = len(sys.argv)
# number of arguments plus 1
if total!=1:
    print "You need some arguments, will ABORT!"
    print "Ex: ",sys.argv[0]," "
    assert(False)
# done if

#################################################################
################### Configurations ##############################
#################################################################

debug=False
verbose=True

list_option="brute_force,kdtree_naive,kdtree_advanced".split(",")
#list_option="kdtree_advanced".split(",")

#svg_file_name="./points.svg"
#svg_file_name="./points2.svg"
svg_file_name="./pointsTutorial.svg"

TAG_NAME_CIRCLE='{http://www.w3.org/2000/svg}circle'
TAG_NAME_GROUP='{http://www.w3.org/2000/svg}g'

#list_tolerance=[50.0,50.0,0.20]
list_tolerance=[50.0,50.0]
#list_tolerance=None

infinity=float("inf")

dimensionCoordinates=2
dimensionAttributes=0
dimensionPoint=dimensionCoordinates+dimensionAttributes
k=dimensionPoint # the number of demensions for the k-d tree

if dimensionAttributes==1 and "/points2Tutorial.svg" in svg_file_name:
    print "You are running on svg file",svg_file_name,"that does not have any attributes besides coordinates. Will ABORT!!!"
    assert(False)
# 

# to visualise better nested dictionaries
# https://docs.python.org/2/library/pprint.html
pp=pprint.PrettyPrinter(indent=0)

#################################################################
################### Functions ###################################
#################################################################

####  read the list of points from the svg file ###

def get_point_from_circle(circle):
    if dimensionCoordinates==2:
        if dimensionAttributes==0:
            point=(float(circle.attrib['cx']),float(circle.attrib['cy']))
        elif dimensionAttributes==1:
            point=(float(circle.attrib['cx']),float(circle.attrib['cy']),float(circle.attrib['i']))
        else:
            print "dimensionCoordinates",dimensionCoordinates,"dimensionAttributes",dimensionAttributes,"not known. Will ABORT!!!"
            assert(False)
        # done if
    else:
        print "dimensionCoordinates",dimensionCoordinates,"dimensionAttributes",dimensionAttributes,"not known. Will ABORT!!!"
        assert(False)
    # done if
    if debug:
        print "point",point
    return point 
# done function

def get_tree(svg_file_name):
    return ET.parse(svg_file_name)
# done function

def get_list_point(tree):
    # using list comprehension to be more concise
    list_point=[
        get_point_from_circle(circle)
        for circle in tree.iter(TAG_NAME_CIRCLE)
        ]
    if debug:
        print "list_point",list_point
    return list_point
# done function

def get_list_point_with_the_same_point_id(tree, point_id):
    # using list comprehension to be more concise
    list_point=[
        get_point_from_circle(circle)
        for circle in tree.iter(TAG_NAME_CIRCLE)
        if 'id' in circle.attrib
        if circle.attrib['id']==point_id
        ]
    if debug:
        print "list_point with same point_id",list_point
    return list_point
# done function

def get_list_point_with_the_same_group_id(tree, group_id):
    # using list comprehension to be more concise
    list_point=[
        point
        for group in tree.iter(TAG_NAME_GROUP)
        if 'id' in group.attrib
        if group.attrib['id']==group_id
        for point in get_list_point(group)
        ]
    if debug:
        print "list_point with same group_id",list_point
    return list_point
# done function

### find the distance between two points with tolerances ###

def get_distance_squared(pointA,pointB,list_tolerance=None,metric="euclidean"):
    # if any of points is none, return an infinite distance
    if pointA==None or pointB==None:
        return infinity
    text_error="does not have the dimension of "+str(dimensionPoint)+", made of "+str(dimensionCoordinates)+" coordinates plus "+str(dimensionAttributes)+" attributes. Will ABORT!!!"
    # these steps are called destructurize the ntuples in X,Y,I
    if len(pointA)!=dimensionPoint:
        print "pointA",pointA,text_error
        assert(False)
    # done if
    if len(pointB)!=dimensionPoint:
        print "pointB",pointB,text_error
        assert(False)
    # done if
    # convert to numpy arrays so that we can make the differences one by one
    nparray_A=np.asarray(pointA) # A
    nparray_B=np.asarray(pointB) # B
    nparray_adAB=np.absolute(nparray_A-nparray_B) # element-wise absolute difference of A-B

    # the squared distance in the space of N dimensions, find out what N is as a function of the metric
    if metric=="euclidean":
        N=dimensionCoordinates # N=1,2,3, ignore the attributes
    elif metric=="all":
        N=dimensionPoint # N uses also the attributes, may be tried out in the future
    else:
        print "metric",metric,"not known. Choose euclidean, all. Will ABORT!!!"
        assert(False)
    # done if

    # compare the differences between the two points with the given tolerances
    nparray_adAB_coordinates=nparray_adAB[0:N] # keep only the N first elements
    nparray_adAB_coordinates_squared=np.power(nparray_adAB_coordinates,2) # square the array
    distance_squared=np.sum(nparray_adAB_coordinates_squared) # sum the array
    if debug:
        print "distance_squared",distance_squared
    
    # if not list of tolerance given, return the distance squared
    if list_tolerance==None:
        return distance_squared

    # if here it means the tolerance checked was asked for, so check the list of tolerance has the right number of dimensions
    if len(list_tolerance)!=dimensionPoint:
        print "list_tolerance",list_tolerance,text_error
        assert(False)

    # if here it means that the tolerance has the same number of dimensions as points A and B and same as to what was asked for
    nparray_T=np.asarray(list_tolerance) # element-wise expected tolerance
    nparray_adAB_minus_T=nparray_adAB-nparray_T # element wise expected absolut differences minus the tolerances
    failed_tolerance=(nparray_adAB_minus_T>0).any() # if any of these elements is larger than zero, we have broken the tolerance
    if failed_tolerance:
        if debug:
            print "Tolerance failed A",nparray_A,"B",nparray_B,"adAB_minus_T",nparray_adAB_minus_T,"adAB",nparray_adAB,"T",nparray_T
        return infinity
    else:
        return distance_squared
    # done if
# done function

### find the closest point with the brute force method ###

def get_closest_point_brute_force(pivot,list_point,list_tolerance):
    closest_index=None
    closest_point=None
    closest_distance_squared=infinity
    for current_index,current_point in enumerate(list_point):
        if debug:
            print "current_index",current_index,"current_point",current_point
        current_distance_squared=get_distance_squared(pivot,current_point,list_tolerance)
        if debug:
            print "current_distance_squared",current_distance_squared
        if current_distance_squared<closest_distance_squared:
            closest_index=current_index
            closest_point=current_point
            closest_distance_squared=current_distance_squared
        if debug:
            print "closest_index",closest_index,"closest_point",closest_point,"closest_distance_squared",closest_distance_squared
        # done if
    # done for loop
    if debug or verbose:
        print "Studied in the euclidian space in "+str(dimensionPoint)+" total dimenensions, made of "+str(dimensionCoordinates)+" coordinates plus "+str(dimensionAttributes)+" attributes. Searched the closest point for the",pivot," with list_tolerances",list_tolerance," The result is the point",closest_point,"with the closest_index",closest_index,"got closest_distance_squared",closest_distance_squared
    return closest_index,closest_point,closest_distance_squared
# done function

### find the closest point via a k-d tree (common to the naive and avanced methods) ###

# recursive function that builds the k-d tree a the list of points
# when it splits, it wil have as input a list which is a subset of the previous list
# and a depth increased by one
# depths starts with the default value of zero, for when we first invoke the function
def get_kdtree(list_point,depth=0):
    N=len(list_point)
    # if no points, we can not build any kdtree, so return None
    if N<=0:
        return None
    # we will alternate the axis to use indices x,y -> indices 0,1; k=2 dimensions (x,y)
    # axis:  0,1,0,1,0,1
    # depth: 0,1,2,4,5,5
    # so we can write the value of the axis as the value of the depth modulo value of k
    axis=depth%k
    # list_point is a list of tuples, each tuple with two floats for x,y or t0,t1
    # as per the k-d tree algorithm, we sort this list only by the chosen axes
    # if axis=1 (x), then we ignore the y values and the x values must be in increasing ordder
    # if axis=2 (y), then we ignore the x values and the y values must be in increasign order
    list_point_sorted=sorted(list_point,key=lambda point: point[axis])
    if debug:
        print "list_point_sorted",list_point_sorted
        for point in list_point_sorted:
            print "point",point
    # done if
    # now that the list is ordered, we will choose the point in the middle
    # if N=5, choose the third value, n=2
    # if N=4, there is no real middle, so choose the first of the second value, also n=2
    # so the general formula for the position of the median is n=N/2, where n and N are integers
    # and remember in integer algebra 5/2=2
    # this chosen median point will become a node in the tree
    # we will create two sub-lists of points to its left and right
    # and then we will call recursively the same function to split them again
    # but changing the axis, so we would increase the depth by one k+=1
    # which will define the new alternating axis by the value axis=depth%k
    # so no need to store the axis value, as it is calculated from depth inside the function
    # and we will return the k-d tree. So how does the k-d tree looks like?
    # The k-d tree has the three elements:
    # 1. one point (the node): the chosen median point in our list
    # 2. a new tree made from a new list of points, the sub-list found to the left of our median point
    # 3. a new tree made from a new list of points, the sub-list found to the right of our median point
    # What data structure is best to represent such tree?
    # A dictionary! With keys "point", "left", "right". 
    return {
        # the median point, from the list at position N/2
        'point':list_point_sorted[N/2],
        # new tree from sub-list left of N/2 and increased depth by one
        'left':get_kdtree(list_point_sorted[0:N/2],depth+1), 
        # new tree from sub-list right of N/2 and increased depth by one
        'right':get_kdtree(list_point_sorted[N/2+1:],depth+1), 
        }
# done function

### find the closest point with the k-d tree naive ###

# the kdtree is the root tree, the big tree of the kdtree
# need to keep track of the depth starting with the default of 0
# need to keep track of the closest point, starting with the default of None
# this is a recursive function too
def get_closest_point_kdtree_naive(pivot,kdtree,list_tolerance,depth,closest_point):
    # deal with edge (corner) cases first
    if kdtree is None:
        # we reached the leaf of the kdtree and we must return the best result and stop the recursion
        # the recursion stops as we do not ask to return the result of the same function, but the point
        if debug:
            print "kdtree_naive: Closest point to the pivot",pivot,"is the point",closest_point
        return closest_point
    # done if

    axis=depth%k

    # does the current comparison find a closest point?
    next_closest_point=None
    # on what branch show we go next? Left or Right?
    next_kdtree=None

    # to answer the first question, we need to compare two distances squared (squared to be faster)
    # 1) get_distance_squared(pivot,current_closest_point,list_tolerance)
    # 2) get_distance_squared(pivot,current_point_list_tolerance)
    # But what is the current_point? None other the splitting point of the current node of the kdtree
    # 2) get_distance_squared(pivot,kdtree['point'],list_tolerance)
    # but remember that the current_closest_point can be None at first, and in that case we just
    # want to assign the first value
    if closest_point is None or get_distance_squared(pivot,kdtree['point'],list_tolerance) < get_distance_squared(pivot,closest_point,list_tolerance):
        next_closest_point=kdtree['point']
    else:
        next_closest_point=closest_point
    # done if

    # to answer the second question, we see on which side of the current splitting point lies our pivot
    if pivot[axis]<kdtree['point'][axis]:
        next__kdtree=kdtree['left']
    else:
        next_kdtree=kdtree['right']
    # done if

    # with this two information we can go to the next iteration of the recursive process
    return get_closest_point_kdtree_naive(pivot,next_kdtree,list_tolerance,depth+1,next_closest_point)
# done function

### find the closest point with the k-d tree advanced ###

# get the closest of two points to the pivot
# the pivot can not be None, but the two points can
# the distance between None and the pivot is infinite
# None is the most distance point
# if both points are None, then return None, meaning no closest point
def get_closest_of_two_points(pivot,point1,point2,list_tolerance):
    if point1 is None:
        return point2
    if point2 is None:
        return point1
    # these two if guarantee that if both are None, then it returns None
    # once here, both of them are not none, and as pivot is not None
    # we can measure the distances
    if get_distance_squared(pivot,point1,list_tolerance)<get_distance_squared(pivot,point2,list_tolerance):
        return point1
    else:
        return point2
# done function

# iterative function, we maintain depth, but not closest_point
# default value of depth=0
def get_closest_point_kdtree_advanced(pivot,kdtree,list_tolerance,depth):
    if debug:
        print "depth",depth,"splitting point",kdtree['point']

    # if the kdtree is none (the leaf of the tree), then it has no point inside so we return none
    if kdtree is None:
        return None

    axis=depth%k

    next_kdtree=None
    opposite_kdtree=None

    if pivot[axis]<kdtree['point'][axis]:
        next_kdtree=kdtree['left']
        opposite_kdtree=kdtree['right']
    else:
        next_kdtree=kdtree['right']
        opposite_kdtree=kdtree['left']
    # done if

    # now read to invoke the recursive call
    closest_point=get_closest_of_two_points(
        pivot,
        kdtree['point'],
        get_closest_point_kdtree_advanced(pivot,next_kdtree,list_tolerance,depth+1),
        list_tolerance
        )

    # but maybe there is something better on the other side
    # a good indicator of this is if the distance on that axis between pivot and point
    # is smaller than the euclidean distance between the pivot and the closest_point found above
    d_axis_pivot_point=pivot[axis]-kdtree['point'][axis]
    if d_axis_pivot_point*d_axis_pivot_point<get_distance_squared(pivot,closest_point,list_tolerance):
        # same call but for the opposite branch of the tree
        # and instead of the splitting point, use the previous best
        closest_point=get_closest_of_two_points(
            pivot,
            closest_point,
            get_closest_point_kdtree_advanced(pivot,opposite_kdtree,list_tolerance,depth+1),
            list_tolerance
        )
    # done if

    return closest_point
# done function

### putting it all together to prepare to run ###

def doItOne(pivot,list_point,option):
    if debug:
        print "doItOne() with option",option
    if option=="brute_force":
        # step 1: does not exist, we do not need to build something, as we will use all events
        None
        # step 2: traverse all the points, and at every step maintain the closest point
        closest_index,closest_point,closest_distance_squared=get_closest_point_brute_force(pivot,list_point,list_tolerance)
    elif option=="kdtree_naive":
        # step 1: build the k-d tree
        kdtree=get_kdtree(list_point,depth=0)
        if debug:
            pp.pprint(kdtree)
        # step 2 in naive approach approach:
        # use the k-d tree, and at every step maintain the closest point 
        # advantage in speed vs brute force is that we do not need to traverse all the tree branches
        # but rather discard those that can not meet our criteria, and thus gain time
        # one recursion inside the main function
        closest_point=get_closest_point_kdtree_naive(pivot,kdtree,list_tolerance,depth=0,closest_point=None)
    elif option=="kdtree_advanced":
        # step 1: build the k-d tree
        kdtree=get_kdtree(list_point,depth=0)
        if debug:
            pp.pprint(kdtree)
        # step 2 the advanced approach
        # two recursions inside the main function, but second only inside an if, so not always
        # to check if in the opposite branch there is no closer point
        closest_point=get_closest_point_kdtree_advanced(pivot,kdtree,list_tolerance,depth=0)
    else:
        print "option",option,"not known. Choose brute_force, kdtree_naive. Will ABORT!!!"
        assert(False)
    # done if
    return closest_point
# done function

def doItAll():
    tree=get_tree(svg_file_name)
    [pivot]=get_list_point_with_the_same_point_id(tree, "pivot")
    if debug or verbose:
        print "pivot",pivot
    list_point=get_list_point_with_the_same_group_id(tree, "points")
    if debug or verbose:
        print "list_point",list_point
    for option in list_option:
        if debug:
            print "option",option
        start = time.time()
        closest_point=doItOne(pivot,list_point,option)
        end = time.time()
        if debug or verbose:
            print "Option","%-15s" % option,", timing",end-start,"seconds, closest_point",closest_point
    # done if
# done function

#################################################################
################### Run #########################################
#################################################################

doItAll()

#################################################################
################### Finished ####################################
#################################################################

print ""
print ""
print "Finished all in",sys.argv[0]
