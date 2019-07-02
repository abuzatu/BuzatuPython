#!/usr/bin/python
from HelperPython import *
import xml.etree.ElementTree as ET

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

list_option="A".split(",")

#svg_file_name="./points.svg"
#svg_file_name="./points2.svg"
svg_file_name="./pointsTutorial.svg"

TAG_NAME_CIRCLE='{http://www.w3.org/2000/svg}circle'
TAG_NAME_GROUP='{http://www.w3.org/2000/svg}g'

# assume a point is an ntuple with its positions

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

def get_closest_point(list_point, pivot):
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
    if debug or verbose:
        print "Closest point to the pivot",pivot,"is the point",closest_point
    return closest_point, closest_distance_squared
# done function

### putting it all together to prepare to run ###

def doItOne(option):
    if debug:
        print "doItOne() with option",option
    tree=get_tree(svg_file_name)
    [pivot]=get_list_point_with_the_same_point_id(tree, "pivot")
    print "pivot",pivot
    list_point=get_list_point_with_the_same_group_id(tree, "points")
    print "list_point",list_point
    closest_point,closest_distance_squared=get_closest_point(list_point,pivot)
    None
# done function

def doItAll():
    for option in list_option:
        if debug:
            print "option",option
        doItOne(option)
    None  
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
