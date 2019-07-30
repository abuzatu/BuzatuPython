#!/usr/bin/python

from plyfile import PlyData, PlyElement
import numpy as np

def get_plyData_from_ply_ascii_file(inputFileName,debug):
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

# get a point cloud of N points, each with M properties (x,y,z, etc)
# as a numpy array of shape N*M
# each row is a new point of dimension M; so there are M columns
# there are N points, so N rows
def get_nparray(plyData,expected_M=0,debug=False,verbose=False):
    list_pointTuple=plyData.elements[0].data
    N=len(list_pointTuple)
    M=len(list_pointTuple[0])
    if debug or verbose:
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
    if debug or verbose:
        print "Calculate min and max on each axis:"
    for i in xrange(M):
        nparrayD=nparray[:,i]
        minValue=np.min(nparrayD)
        maxValue=np.max(nparrayD)
        if debug or verbose:
            print "axis %i: (min,max)=(%.3f, %.3f);" % (i,minValue,maxValue)
    print ""
    # below example how to sort the numpy array 
    return nparray
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
    list_point=get_list_point(plyData,expected_M=0,debug=False,verbose=verbose)
    N=len(list_point)
    if debug or verbose:
        print "N",N,"[0]",type(list_point[0]),list_point[0]
        print "numpy NxM:"
    nparray=get_nparray(plyData,expected_M=0,debug=False,verbose=verbose)
    testFileName=inputFileName.replace(".ply","_rewrite.ply")
    write_point_cloud_to_ascii_ply(nparray,testFileName,debug=False,verbose=verbose)
# done function
