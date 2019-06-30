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

svg_file_name="./points.svg"

TAG_NAME_CIRCLE='{http://www.w3.org/2000/svg}circle'
TAG_NAME_GROUP='{http://www.w3.org/2000/svg}g'

list_tolerance=[50.0,50.0,0.40]

# assume a point is an ntuple with its positions


#################################################################
################### Functions ###################################
#################################################################

####  read the list of points from the svg file ###

def get_point_from_circle(circle):
    point=(float(circle.attrib['cx']),float(circle.attrib['cy']),float(circle.attrib['i']))
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

def get_distance_squared(pointA,pointB,list_tolerance):
    # these steps are called destructurize the ntuples in X,Y,I
    A0,A1,A2,=pointA
    B0,B1,B2=pointB
    d0=abs(A0-B0)
    d1=abs(A1-B1)
    d2=abs(A2-B2)
    euclidean_distance_squared=d0*d0+d1*d1
    if list_tolerance==None:
        distance_squared=euclidean_distance_squared
    else:
        if len(list_tolerance)!=3:
            print "list_tolerance",list_tolerance,"does not have 3 elements for XYI, so we ABORT!!!"
            assert(False)
        else:
            if d0>list_tolerance[0] or d1>list_tolerance[1] or d2>list_tolerance[2]:
                distance_squared=None
            else:
                distance_squared=euclidean_distance_squared
            # done if
        # done if
    # done if
    if debug:
        print "A0",A0,"B0",B0,"A1",A1,"B1",B1,"A2",A2,"B2",B2,"distance_squared",distance_squared
    return distance_squared
# done function

def get_closest_point(pivot,list_point,list_tolerance):
    closest_distance_squared=None
    closest_point=None
    for current_point in list_point:
        if debug:
            print "current_point",current_point
        current_distance_squared=get_distance_squared(pivot,current_point,list_tolerance)
        if current_distance_squared=="None": # it did not pass tolerances, so we ignore it
            new_closest_distance=False
        else:
            if current_distance_squared<closest_distance_squared:
                new_closest_distance=True
            else:
                new_closest_distance=False
            # done if
        # done if 
        if debug:
            print "current_distance_squared",current_distance_squared,"new_closest_distance",new_closest_distance
        if closest_distance_squared==None or current_distance_squared<closest_distance_squared:
            closest_distance_squared=current_distance_squared
            if closest_distance_squared!=None:
                closest_point=current_point
        if debug:
            print "closest_point",closest_point,"closest_distance_squared",closest_distance_squared
        # done if
    # done for loop
    if debug or verbose:
        print "Evaluated the closest point in euclidian space in 2D but with the constraints of being within the tolerances for the x, y and i.\nThe closest point to the pivot",pivot,"is the point",closest_point
    return closest_point, closest_distance_squared
# done function

### putting it all together to prepare to run ###

def doItOne(option):
    if debug:
        print "doItOne() with option",option
    tree=get_tree(svg_file_name)
    list_point=get_list_point_with_the_same_group_id(tree, "points")
    print "list_point",list_point
    [pivot]=get_list_point_with_the_same_point_id(tree, "pivot")
    print "pivot",pivot
    closest_point,closest_distance_squared=get_closest_point(pivot,list_point,list_tolerance)
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
