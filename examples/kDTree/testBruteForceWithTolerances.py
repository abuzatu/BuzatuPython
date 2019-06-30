#!/usr/bin/python
from HelperPython import *
import xml.etree.ElementTree as ET
import numpy as np

# re-implement on 19 June 2019 the example from https://github.com/tsoding/kdtree-in-python/blob/master/main.py
# then added two things: 
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

list_option="A".split(",")

svg_file_name="./points.svg"
#svg_file_name="./points2Tutorial.svg"

TAG_NAME_CIRCLE='{http://www.w3.org/2000/svg}circle'
TAG_NAME_GROUP='{http://www.w3.org/2000/svg}g'

list_tolerance=[50.0,50.0,0.20]
#list_tolerance=[10.0,10.0]
#list_tolerance=None

infinity=float("inf")

dimensionCoordinates=2
dimensionAttributes=1
dimensionPoint=dimensionCoordinates+dimensionAttributes

if dimensionAttributes==1 and "/points2Tutorial.svg" in svg_file_name:
    print "You are running on svg file",svg_file_name,"that does not have any attributes besides coordinates. Will ABORT!!!"
    assert(False)
# 

# assume a point is an ntuple with its positions


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

### find the closest point with the brute force method ###

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

def get_closest_point(pivot,list_point,list_tolerance):
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

### putting it all together to prepare to run ###

def doItOne(option):
    if debug:
        print "doItOne() with option",option
    print ""
    tree=get_tree(svg_file_name)
    list_point=get_list_point_with_the_same_group_id(tree,"points")
    if verbose:
        print "list_point",list_point
    [pivot]=get_list_point_with_the_same_point_id(tree,"pivot")
    if verbose:
        print "pivot",pivot
    if verbose:
        print ""
        print "with list_tolerance",list_tolerance
    closest_index,closest_point,closest_distance_squared=get_closest_point(pivot,list_point,list_tolerance)
    if verbose:
        print ""
        print "with list_tolerance",None
    closest_index,closest_point,closest_distance_squared=get_closest_point(pivot,list_point,None)
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
