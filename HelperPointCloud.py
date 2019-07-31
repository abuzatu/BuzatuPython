#!/usr/bin/python

from HelperStatistics import *
from plyfile import PlyData, PlyElement
import numpy as np
from sklearn.neighbors import NearestNeighbors

def get_plyData_from_ply_ascii_file(inputFileName,debug=False):
    if debug:
        print "Reading plyData from ply ascii file",inputFileName
    plyData=PlyData.read(inputFileName)
    return plyData
# done function

# get a point cloud of N points, each with M properties (x,y,z, etc)
# as a list of points (with N elements)
# where each point is a numpy array of dimension M
def get_list_point(plyData,expected_M=0,debug=False,verbose=False):
    list_pointTuple=plyData.elements[0].data
    N=len(list_pointTuple)
    M=len(list_pointTuple[0])
    if verbose or debug:
        print "N",N,"M",M
    if debug:
        print "plyData",type(plyData),plyData
        print "plyData.elements[0]",type(plyData.elements[0]),plyData.elements[0]
        print "plyData.elements[0].data",type(list_pointTuple),list_pointTuple.shape,list_pointTuple.dtype
        print list_pointTuple
        print len(list_pointTuple)
        print list_pointTuple[0]
    # done if
    # convert point from tuple to numpy array, () -> []
    list_point=[]
    for i,pointTuple in enumerate(list_pointTuple):
        if debug:
            print "i",i,"pointTuple",type(pointTuple),pointTuple
        if i==0:
            M=len(pointTuple)
            if expected_M!=0:
                if M!=expected_M:
                    print "For this first pointTuple",pointTuple,"its dimension M",M,"is different than the expected_M",expected_M,"so we will ABORT!!!!"
                    assert(False)
                # done if
            # done if
        else:
            if len(pointTuple)!=M:
                print "This pointTuple",pointTuple,"does not have dimension M",M,"as the previous. So we will ABORT!!!"
                assert(False)
            # done if
        # done if
        point=np.asarray([value for value in pointTuple])
        list_point.append(point)
    # done for loop over points in list
    return list_point
# done function

def get_list_point_from_ply_ascii_file(inputFileName,expected_M=0,debug=False,verbose=False):
    if debug:
        print "Reading numpy from ply ascii file",inputFileName
    return get_list_point(PlyData.read(inputFileName),expected_M=0,debug=debug,verbose=debug)
# done function

# get a point cloud of N points, each with M properties (x,y,z, etc)
# as a numpy array of shape N*M
# each row is a new point of dimension M; so there are M columns
# there are N points, so N rows
def get_nparray(plyData,expected_M=0,debug=False,verbose=False):
    list_pointTuple=plyData.elements[0].data
    N=len(list_pointTuple)
    M=len(list_pointTuple[0])
    if debug:
        print "N",N,"M",M
    if debug:
        print "plyData",type(plyData),plyData
        print "plyData.elements[0]",type(plyData.elements[0]),plyData.elements[0]
        print "plyData.elements[0].data",type(list_pointTuple),list_pointTuple.shape,list_pointTuple.dtype
        print list_pointTuple
        print len(list_pointTuple)
        print list_pointTuple[0]
    # done if
    # convert point from tuple to numpy array, () -> []
    nparray_shape=(N,M)
    nparray=np.zeros(nparray_shape,dtype=np.float32)
    if debug:
        print "nparray"
        print nparray
    for i in xrange(0,N):
        nparray[i,:]=np.array([value for value in list_pointTuple[i]])
    if debug:
        print "nparray after filling"
        print nparray  
    # calculate the min and max for each dimension
    if debug:
        print "Calculate min and max on each axis:"
    for i in xrange(M):
        nparrayD=nparray[:,i]
        minValue=np.min(nparrayD)
        maxValue=np.max(nparrayD)
        if debug:
            print "axis %i: (min,max)=(%.3f, %.3f);" % (i,minValue,maxValue)
    if debug:
        print ""
    # done
    return nparray
# done function

def get_nparray_from_ply_ascii_file(inputFileName,expected_M=0,debug=False,verbose=False):
    if debug:
        print "Reading numpy from ply ascii file",inputFileName
    return get_nparray(PlyData.read(inputFileName),expected_M=0,debug=debug,verbose=verbose)
# done function

# write a point cloud represented as a nparray to an ASCII .ply file
# so that we can visualize in CloudCompare smaller point clouds we create
# based on cleaning of our own, and selecting only subsets
def write_point_cloud_to_ascii_ply(nparray, outputFileName,debug=False,verbose=False):
    if debug:
        print "Start write_point_cloud_to_ascii_ply"
        print "nparray"
        print nparray
    N=nparray.shape[0]
    M=nparray.shape[1]
    if debug:
        print "N",N,"M",M
    if M!=3:
        print "WARNING!!! The header for M",M,"may not be right. Check the header writes all the variables you want!!!"
    if debug:
        for i in xrange(N):
            print i,nparray[i]
    # write the file
    f=open(outputFileName,"w+")
    # write the ascii ply header
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write("comment PCL generated\n")
    f.write("element vertex %i\n" % N)
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("property float intensity\n")
    f.write("element camera 1\n")
    f.write("property float view_px\n")
    f.write("property float view_py\n")
    f.write("property float view_pz\n")
    f.write("property float x_axisx\n")
    f.write("property float x_axisy\n")
    f.write("property float x_axisz\n")
    f.write("property float y_axisx\n")
    f.write("property float y_axisy\n")
    f.write("property float y_axisz\n")
    f.write("property float z_axisx\n")
    f.write("property float z_axisy\n")
    f.write("property float z_axisz\n")
    f.write("property float focal\n")
    f.write("property float scalex\n")
    f.write("property float scaley\n")
    f.write("property float centerx\n")
    f.write("property float centery\n")
    f.write("property int viewportx\n")
    f.write("property int viewporty\n")
    f.write("property float k1\n")
    f.write("property float k2\n")
    f.write("end_header\n")
    # write the values of the point cloud, in our new coordinate system
    for i in xrange(N):
        text=""
        for dimensionIndex in xrange(0,M):
            if dimensionIndex==0:
                pad=""
            else:
                pad=" "
            value=nparray[i,dimensionIndex]
            text+=pad+str(value)
        # done loop over all dimensions
        f.write(text+"\n")
    # done loop over all points
    # write the ascii ply last line, that is: 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 121130 1 0 0
    f.write(" 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 %i 1 0 0\n" % N)
# done function

def test_one_point_cloud(inputFileName,debug=False,verbose=False):
    plyData=get_plyData_from_ply_ascii_file(inputFileName,debug)
    if debug or verbose:
        print "list_point:"
    list_point=get_list_point(plyData,expected_M=0,debug=debug,verbose=verbose)
    N=len(list_point)
    if debug or verbose:
        print "N",N,"[0]",type(list_point[0]),list_point[0]
        print "numpy NxM:"
    nparray=get_nparray(plyData,expected_M=0,debug=debug,verbose=verbose)
    testFileName=inputFileName.replace(".ply","_rewrite.ply")
    write_point_cloud_to_ascii_ply(nparray,testFileName,debug=debug,verbose=verbose)
    # to add: function that re-orders the axis to be in a particular order to be plotted easily:
    # left to right; bottom to up; backwards to forwards; the attributes remain as they are
    # create histograms for all the axes
# done function

def distance(nparray1,nparray2,debug=False):
    M1=len(nparray1)
    M2=len(nparray2)
    if debug:
        print "M1",M1,"M2",M2
    assert(M1==M2)
    M=M2
    distance_squared=0
    for i in xrange(M):
        distance_squared+=(nparray1[i]-nparray2[i])**2
    distance=math.sqrt(distance_squared)
    if debug:
        print "distance",distance
    return distance
# done function

def reorder_one_point_cloud_to_match_a_reference(pc_reference,pc_current,debug=False,verbose=False):
    # for each get a subset representing only the coordinates
    # update_dictionary_plyData_retrieve_dictionary_distance
    # get_dict_stage_name_values(dict_stage_plyData,dataFormat)
    #
    # use all coordinates in the point cloud (this is just an approximation)
    if debug:
        print "Built NearestNeigbourghs object for the pc_current"
    nn_current=NearestNeighbors(n_neighbors=1,algorithm='auto',metric='euclidean').fit(pc_current)
    if debug:
        print "Match the pc_reference to the pc_current"
    distances_current_to_reference,indices_current_to_reference=nn_current.kneighbors(pc_reference)
    if debug:
        print "distances_current_to_reference",type(distances_current_to_reference),len(distances_current_to_reference),distances_current_to_reference
        print "indices_current_to_reference",type(indices_current_to_reference),len(indices_current_to_reference),indices_current_to_reference
    if False:
        for i in xrange(len(distances_current_to_reference)):
            print "i",i,"reference",pc_reference[i],"current_ordered",pc_current[indices_current_to_reference[i]][0],"current_original",pc_current[i]
            print pc_reference[i].shape
            print pc_current[indices_current_to_reference[i]][0].shape
    if debug:
        print "indices_current_to_reference",indices_current_to_reference.shape
        print "Reshape the distances and indices to be from (N,1) to (N,)"
    indices_current_to_reference_reshaped=indices_current_to_reference.T[0]
    distances_current_to_reference_reshaped=distances_current_to_reference.T[0]
    if debug:
        print "indices_current_to_reference_reshaped",indices_current_to_reference_reshaped
    if debug:
        print "Reorder the pc_current to match the order in pc_reference"
    pc_current_reordered=pc_current[indices_current_to_reference_reshaped]
    if debug:
        print "pc_current",pc_current.shape,pc_current[0]
        print pc_current
        print "pc_reference",pc_reference.shape,pc_reference[0]
        print pc_reference
        print "pc_current_reordered",pc_current_reordered.shape,pc_current_reordered[0]
        print pc_current_reordered
        print "distances_current_to_reference_reshaped"
        print distances_current_to_reference_reshaped
    print ""
    N=pc_current.shape[0]
    if debug:
        for i in xrange(N):
            if i>10:
                continue
            dist_us=distance(pc_reference[i],pc_current_reordered[i],debug)
            dist_them_1=distances_current_to_reference_reshaped[i]
            print i,"cur",pc_current[i],"ref",pc_reference[i],"cur_ordered",pc_current_reordered[i],"dist_us",dist_us,"dist_them",dist_them_1
    # done
    return pc_current_reordered,distances_current_to_reference_reshaped
# done function

def compare_two_point_clouds_with_same_order(pc_current,pc_reference,debug=False,verbose=False):
    pc_current_deviation=np.absolute(pc_current-pc_reference)
    if debug:
        print "pc_current_deviation"
        print pc_current_deviation
    N,M=pc_current.shape
    if debug:
        print "N",N,"M",M
    # get numpy arrays of dimension M with the maximum and averages values of each column
    columns_max=np.max(pc_current_deviation,0)
    columns_avg=np.mean(pc_current_deviation,0)
    # and here have access at the values of each column
    # such as to store in a histogram and then plot them
    if False:
        for i in xrange(M):
            if debug:
                print "axis i",i
            # the column along the i-th axis
            # 1 is the second dimension, hence the one with axis
            # then from the axes we take the one with number i
            nparray_column=np.take(pc_current_deviation,i,1)
            column_max=np.max(nparray_column)
            column_avg=np.mean(nparray_column)
            if debug:
                print "max",column_max,"avg",column_avg
            # create a histogram from the full distribution of the column
            # and save it in a plot
        # done loop over dimensions
    # done if
    return columns_max,columns_avg
# done function
