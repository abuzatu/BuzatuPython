#!/usr/bin/python
from HelperPython import *
# to parse xml files
import xml.etree.ElementTree as ET
# to arrange visually better the output of nested dictionaries
import pprint 
# time
import time

# re-implement on 19 June 2019 the example from https://github.com/tsoding/kdtree-in-python/blob/master/main.py

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

svg_file_name="./points2.svg"

TAG_NAME_CIRCLE='{http://www.w3.org/2000/svg}circle'
TAG_NAME_GROUP='{http://www.w3.org/2000/svg}g'

# assume a point is an ntuple with its positions, and we have 2 positions x,y, so
k=2 # the number of dimension of our data, here only x,y

# to visualise better nested dictionaries
# https://docs.python.org/2/library/pprint.html
pp=pprint.PrettyPrinter(indent=0)

#################################################################
################### Functions ###################################
#################################################################

####  read the list of points from the svg file ###

def get_point_from_circle(circle):
    point=(float(circle.attrib['cx']),float(circle.attrib['cy']))
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

### find the closest point with the brute force method ###

def get_distance_squared(point1,point2):
    # these steps are called destructurize the ntuples
    x1,y1=point1
    x2,y2=point2
    dx=x2-x1
    dy=y2-y1
    distance_squared=dx*dx+dy*dy
    if debug:
        print "x1",x1,"y1",y1,"x2",x2,"y2",y2,"distance_squared",distance_squared
    return distance_squared
# done function

def get_closest_point_brute_force(pivot,list_point):
    closest_distance_squared=None
    closest_point=None
    for current_point in list_point:
        if debug:
            print "current_point",current_point
        current_distance_squared=get_distance_squared(pivot,current_point)
        if closest_distance_squared==None or current_distance_squared<closest_distance_squared:
            closest_distance_squared=current_distance_squared
            closest_point=current_point
        if debug:
            print "closest_point",closest_point,"closest_distance_squared",closest_distance_squared
        # done if
    # done for loop
    if debug:
        print "brute_force: Closest point to the pivot",pivot,"is the point",closest_point
    return closest_point, closest_distance_squared
# done function

### find the closest point via a k-d tree ###

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

# the kdtree is the root tree, the big tree of the kdtree
# need to keep track of the depth starting with the default of 0
# need to keep track of the closest point, starting with the default of None
# this is a recursive function too
def get_closest_point_kdtree_naive(pivot,kdtree,depth=0,closest_point=None):
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
    # 1) get_distance_squared(pivot,current_closest_point)
    # 2) get_distance_squared(pivot,current_point)
    # But what is the current_point? None other the splitting point of the current node of the kdtree
    # 2) get_distance_squared(pivot,kdtree['point'])
    # but remember that the current_closest_point can be None at first, and in that case we just
    # want to assign the first value
    if closest_point is None or get_distance_squared(pivot,kdtree['point']) < get_distance_squared(pivot,closest_point):
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
    return get_closest_point_kdtree_naive(pivot,next_kdtree,depth+1,next_closest_point)
# done function

# get the closest of two points to the pivot
# the pivot can not be None, but the two points can
# the distance between None and the pivot is infinite
# None is the most distance point
# if both points are None, then return None, meaning no closest point
def get_closest_of_two_points(pivot,point1,point2):
    if point1 is None:
        return point2
    if point2 is None:
        return point1
    # these two if guarantee that if both are None, then it returns None
    # once here, both of them are not none, and as pivot is not None
    # we can measure the distances
    if get_distance_squared(pivot,point1)<get_distance_squared(pivot,point2):
        return point1
    else:
        return point2
# done function


# iterative function, we maintain depth, but not closest_point
def get_closest_point_kdtree_advanced(pivot,kdtree,depth=0):
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
        get_closest_point_kdtree_advanced(pivot,next_kdtree,depth+1)
        )

    # but maybe there is something better on the other side
    # a good indicator of this is if the distance on that axis between pivot and point
    # is smaller than the euclidean distance between the pivot and the closest_point found above
    d_axis_pivot_point=pivot[axis]-kdtree['point'][axis]
    if d_axis_pivot_point*d_axis_pivot_point<get_distance_squared(pivot,closest_point):
        # same call but for the opposite branch of the tree
        # and instead of the splitting point, use the previous best
        closest_point=get_closest_of_two_points(
            pivot,
            closest_point,
            get_closest_point_kdtree_advanced(pivot,opposite_kdtree,depth+1)
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
        closest_point,closest_distance_squared=get_closest_point_brute_force(pivot,list_point)
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
        closest_point=get_closest_point_kdtree_naive(pivot,kdtree)
    elif option=="kdtree_advanced":
        # step 1: build the k-d tree
        kdtree=get_kdtree(list_point,depth=0)
        if debug:
            pp.pprint(kdtree)
        # step 2 the advanced approach
        # two recursions inside the main function, but second only inside an if, so not always
        # to check if in the opposite branch there is no closer point
        closest_point=get_closest_point_kdtree_advanced(pivot,kdtree)
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
