#!/usr/bin/env python3

import numpy as np
import math
from HelperNumpy import print_numpy
from HelperMatplotlib import *

def get_nparray_from_structured_array_from_binary_file(inputFileName,expected_M=0,debug=False,verbose=False):
    if debug:
        print("Reading numpy from structured array from a binary file",inputFileName)
    # start2=timer()
    # read structured array
    structured_array=np.load(inputFileName)
    if debug:
        print("structured_array:")
        print("type",type(structured_array),"size",structured_array.size,"shape",structured_array.shape)
        print(structured_array)
        # [('x', '<f4'), ('y', '<f4'), ('z', '<f4'), ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'), ('index', '<f4')]
        print("type",structured_array.dtype,"its type",type(structured_array.dtype))
        print("descr",structured_array.dtype.descr,type(structured_array.dtype.descr))
        print("names",structured_array.dtype.names,type(structured_array.dtype.names))
    # done if 
    temp_data = []
    for i,axisName in enumerate(structured_array.dtype.names):
        if debug:
            print("i",i,"axisName",axisName)
            print(axisName,structured_array[axisName],type(structured_array[axisName]),structured_array[axisName].dtype)
            print(axisName,structured_array[axisName].astype('f8'),type(structured_array[axisName].astype('f8')),structured_array[axisName].astype('f8').dtype)
        # done if
        temp_data.append(structured_array[axisName].astype('f8')) # need f8 to allow for indices large, as for number of points per cloud large as 130M or nore
    # done for loop
    if debug:
        print("temp_data")
        print(temp_data,type(temp_data))
    nparray_vstack=np.vstack(temp_data)
    if debug:
        print("nparray_vstack",nparray_vstack.dtype,nparray_vstack.shape)
        print(nparray_vstack)
    nparray=nparray_vstack.T
    if debug:
        print("nparray",nparray.dtype,nparray.shape)
        print(nparray)
    # check that it has the same number of axes (M) as expected
    if expected_M!=nparray.shape[1]:
        print("ERROR!!! Expected number of axes=M_expecte=",expected_M,"but obtained",nparray.shape[1],". Will ABORT!!!")
        assert(False)
    # done all
    # end2=timer()
    # print(end2-start2,"seconds to Reading numpy from structured array from a binary file",inputFileName)
    # note, all of the file could be done in these two lines, but no gain in speed is observed
    # structured_array=np.load(inputFileName)
    # return np.vstack([structured_array[axisName].astype('f4') for i,axisName in enumerate(structured_array.dtype.names)]).T
    return nparray
# done function

# applicable for the particular case of S=1, M=2 with a spatial value and an attribute which is an id as integer
# we compress with a tolerance on the integer < 0.49 so the id remains the same in the compression
# so we sort by simply matching the id
def reorder_one_point_cloud_to_match_a_reference_with_last_element_an_id_new_way(pc_reference,pc_current,S,M,debug=False,verbose=False):
    if debug or verbose:
        print("")
        print("Start reorder_one_point_cloud_to_match_a_reference_with_last_element_an_id()")
    pc_current_reordered=np.copy(pc_current)
    if debug:
        print("pc_current",type(pc_current))
        print(pc_current)
        a=pc_current[:,-1]
        print("type",a.dtype,type(a))
        print_nparray("a",a)
        print("pc_current[:,-1]",type(pc_current[:,-1]))
        print(pc_current[:,-1])
        b=np.round(pc_current[:,-1]).astype(np.uint32)
        print("[np.round(pc_current[:,-1]).astype(np.uint32)","len",len(b),"type",type(b),"min",np.min(b),"max",np.max(b))
        print(b)
        unique, counts = np.unique(b, return_counts=True)
        d=dict(zip(unique, counts))
        print("d")
        for e in d:
            if d[e]==0:
                print("e",e,"d[e]",d[e])
        b=np.where(a==35255288)
        print("index of 35255288",b)
    # done if
    # do the reordering
    pc_current_reordered[np.round(pc_current[:,-1]).astype(np.uint32),:]=1*pc_current
    if debug:
        print("before reshape pc_current_reordered")
        print(pc_current_reordered,type(pc_current_reordered))
    # create a new array without the last column
    pc_current_reordered=pc_current_reordered[:,:M] # to skip the last element the index
    if debug:
        print("after reshape pc_current_reordered")
        print(pc_current_reordered,type(pc_current_reordered))
    # calculate distance for the spatial dimensions S
    distances_current_to_reference_reshaped=np.sqrt(np.sum(np.square(pc_current_reordered-pc_reference)[:,:S],axis=-1))
    if debug:
        pc_diff=(pc_current_reordered-pc_reference)**2
        print("pc_diff",pc_diff,type(pc_diff),pc_diff.shape)
        pc_a=pc_diff[:,:S]
        print("pc_a",pc_a,type(pc_a),pc_a.shape)
        pc_s2=np.sum(pc_a,axis=-1)
        print("pc_s2",pc_s2,type(pc_s2),pc_s2.shape)
        pc_s=np.sqrt(pc_s2)
        print("pc_s",pc_s,type(pc_s),pc_s.shape)
    # done all
    return pc_current_reordered,distances_current_to_reference_reshaped              
# done function

def compare_two_point_clouds_with_same_order(pc_current,pc_reference,debug=False,verbose=False):
    if True:
        print("pc_current")
        print(pc_current)
        print("pc_reference")
        print(pc_reference)
    # calculate the max and avg deviation for each axis
    pc_current_deviation=np.absolute(pc_current-pc_reference)
    if debug:
        print("pc_current_deviation")
        print(pc_current_deviation)
    N,M=pc_current.shape
    if debug:
        print("N",N,"M",M)
    # get numpy arrays of dimension M with the maximum and averages values of each column
    columns_max=np.max(pc_current_deviation,0)
    columns_avg=np.mean(pc_current_deviation,0)
    if True or debug:
        print("columns_max",columns_max)
        print("columns_avg",columns_avg)
    # assert(False)
    # and here have access at the values of each column
    # such as to store in a histogram and then plot them
    if False:
        for i in range(M):
            if debug:
                print("axis i",i)
            # the column along the i-th axis
            # 1 is the second dimension, hence the one with axis
            # then from the axes we take the one with number i
            nparray_column=np.take(pc_current_deviation,i,1)
            column_max=np.max(nparray_column)
            column_avg=np.mean(nparray_column)
            if True or debug:
                print("max",column_max,"avg",column_avg)
            # create a histogram from the full distribution of the column
            # and save it in a plot
        # done loop over dimensions
    # done if
    return pc_current_deviation,columns_max,columns_avg
# done function

def calculate_euclidean_distance_deviation_from_point_clouds_with_same_order(pc_current,pc_reference,S,coordinateSystemType,debug=False,verbose=False):
    N,M=pc_current.shape
    pc_current=pc_current.astype(np.float64)
    pc_reference=pc_reference.astype(np.float64)
    if True or debug:
        print("N",N,"M",M,"S",S)
        print("pc_current","dtype",pc_current.dtype)
        print(pc_current)
        print("pc_reference","dtype",pc_reference.dtype)
        print(pc_reference)
        columns_max=np.max(pc_current,0)
        print("columns_max",columns_max)
        columns_max=np.max(pc_reference,0)
        print("columns_max",columns_max)
    #assert(False)
    list_deviation=[]
    # loop over all points and for each calculate the euclidean distance
    # support both cartesian and spherical, and S=0, 1, or 2.
    list_d_cartesian=[]
    list_d_spherical=[]
    list_r2=[]
    list_t2=[]
    list_p2=[]
    list_r1=[]
    list_t1=[]
    list_p1=[]
    for i in range(N):
        #if i>10:
        #    continue
        point_current=pc_current[i]
        point_reference=pc_reference[i]
        if debug:
            print("i",i,"point_current",point_current,"dtype",point_current.dtype,"point_reference",point_reference,"dtype",point_reference.dtype)
        if coordinateSystemType=="Cartesian":
            if S==1:
                # read variables from point_current, assume order x
                x2=point_current[0]
                # read variables from point_reference, assume order x
                x1=point_reference[0]
                # calculate deviation
                x2_x1=x2-x1
                deviation=math.sqrt(x2_x1*x2_x1)
            elif S==2:
                # read variables from point_current, assume order x, y
                x2=point_current[0]
                y2=point_current[1]
                # read variables from point_reference, assume order x, y
                x1=point_reference[0]
                y1=point_reference[1]
                # calculate deviation
                x2_x1=x2-x1
                y2_y1=y2-y1
                deviation=math.sqrt(x2_x1*x2_x1+y2_y1*y2_y1)
            elif S==3:
                # read variables from point_current, assume order x, y, z
                x2=point_current[0]
                y2=point_current[1]
                z2=point_current[2]
                # read variables from point_reference, assume order x, y, z
                x1=point_reference[0]
                y1=point_reference[1]
                z1=point_reference[2]
                # calculate deviation
                x2_x1=x2-x1
                y2_y1=y2-y1
                z2_z1=z2-z1
                deviation=math.sqrt(x2_x1*x2_x1+y2_y1*y2_y1+z2_z1*z2_z1)
            else:
                print("S",S,"not known. Choose 1, 2, 3. Will ABORT!!!")
            # done if
        elif coordinateSystemType=="Spherical":
            if S==1:
                pass
            elif S==2:
                pass
            elif S==3:
                # read variables from point_current, assume order radius, theta, phi
                r2=point_current[0]
                t2=point_current[1]
                p2=point_current[2]
                #t2=0
                #p2=0
                # read variables from point_reference, assume order radius, theta, phi
                r1=point_reference[0]
                t1=point_reference[1]
                p1=point_reference[2]
                #t1=0
                #p1=0
                if r2==0 or r1==0:
                    continue
                # calculate euclidean distance
                cos_t2_t1=np.cos(t2-t1)
                cos_p2_p1=np.cos(p2-p1)
                sin_t2=np.sin(t2)
                sin_t1=np.sin(t1)
                cos_t2=np.cos(t2)
                cos_t1=np.cos(t1)
                if debug:
                    print("r2",r2,"type",r2.dtype)
                    print("r1",r1,"type",r1.dtype)
                    print("t2",t2)
                    print("t1",t1)
                    print("t2_t1",t2-t1)
                    print("cos_t2",cos_t2)
                    print("cos_t1",cos_t1)
                    print("cos_t2_t1",cos_t2_t1)
                    print("sin_t2",sin_t2,"type",type(sin_t2),math.sin(t2),type(math.sin(t2)))
                    print("sin_t1",sin_t1)
                    print("p2",p2,"p1",p1)
                    print("r2*r2",r2*r2)
                    print("r1*r1",r1*r1)
                # d*d=r2*r2+r1*r2-2*r2*r1*[cos(t2-t1)*cos(p2-p1)+sin(t1)*sin(t2)*[1-cos(p2-p1]]
                Parantheses_max_allowed=(r2*r2+r1*r1)/(2*r2*r1)
                if debug:
                    print("Parantheses_max_allowed",Parantheses_max_allowed)
                Parantheses_1=(cos_t2_t1*cos_p2_p1+sin_t2*sin_t1*(1.0-cos_p2_p1))
                if debug:
                    print("Parantheses_1",Parantheses_1)
                d2_spherical=r2*r2+r1*r1-2*r2*r1*Parantheses_1
                d_spherical=np.sqrt(d2_spherical)
                if debug:
                    print("d2_spherical",d2_spherical,"d_spherical",d_spherical)
                # calculate also cartesian coordinates and then the euclidean distance to validate the spherical coordinates formula
                #
                x2=r2*cos_t2*cos_t2
                y2=r2*cos_t2*sin_t2
                z2=r2*sin_t2
                #
                x1=r1*cos_t1*cos_t1
                y1=r1*cos_t1*sin_t1
                z1=r1*sin_t1
                #
                x2_x1=x2-x1
                y2_y1=y2-y1
                z2_z1=z2-z1
                #
                d2_cartesian=x2_x1*x2_x1+y2_y1*y2_y1+z2_z1*z2_z1
                d_cartesian=np.sqrt(d2_cartesian)
                if debug:
                    print("d2_cartesian",d2_cartesian,"d_cartesian",d_cartesian)
         
                #Peak=2
                #if (d_cartesian>Peak-0.1 and d_cartesian<Peak+0.1)==False:
                #    continue
                #
                list_d_cartesian.append(d_cartesian)
                list_d_spherical.append(d_spherical)
                list_r1.append(r1)
                list_t1.append(t1)
                list_p1.append(p1)
                list_r2.append(r2)
                list_t2.append(t2)
                list_p2.append(p2)

                #
                deviation=d_spherical
            else:
                print("S",S,"not known. Choose 1, 2, 3. Will ABORT!!!")
            # done if
        else:
            print("coordinateSystemType",coordinateSystemType,"not known. Choose Cartesian or Spherical. Will ABORT!!!")
            assert(False)
        # done if
        # add deviation to list
        list_deviation.append(deviation)
    # done loop over all points
    #
    numpy_deviation=np.array(list_deviation)
    # do some more plots for spherical coordinates in 3D
    if S==3 and coordinateSystemType=="Spherical":
        numpy_d_cartesian=np.array(list_d_cartesian)
        numpy_d_spherical=np.array(list_d_spherical)
        numpy_r1=np.array(list_r1)*0.01
        numpy_t1=np.array(list_t1)#*180/np.pi
        numpy_p1=np.array(list_p1)#*180/np.pi
        numpy_r2=np.array(list_r2)*0.01
        numpy_t2=np.array(list_t2)#*180/np.pi
        numpy_p2=np.array(list_p2)#*180/np.pi
        if debug:
            print_numpy("numpy_d_cartesian",numpy_d_cartesian)
            print_numpy("numpy_d_spherical",numpy_d_spherical)
            print_numpy("numpy_r1",numpy_r1)
            print_numpy("numpy_t1",numpy_t1)
            print_numpy("numpy_p1",numpy_p1)
            print_numpy("numpy_r2",numpy_r2)
            print_numpy("numpy_t2",numpy_t2)
            print_numpy("numpy_p2",numpy_p2)
            # make plots
            # binning_deviation=Peak-0.05+np.array(range(0,20))*(0.1/20.0)
            binning_deviation=0.0+15.0*np.array(range(0,100))/100.0
            draw_histogram_2d(numpy_d_cartesian,numpy_d_spherical,outputFileName="./output_histo_2D",extensions="png,pdf",nrBins=binning_deviation,info_x=["cartesian"],info_y=["spherical"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_d_cartesian,numpy_r1,outputFileName="./output_histo_2D_cartesian_radius",extensions="png,pdf",nrBins=[binning_deviation,100],info_x=["cartesian"],info_y=["radius"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_d_cartesian,numpy_t1,outputFileName="./output_histo_2D_cartesian_theta",extensions="png,pdf",nrBins=[binning_deviation,100],info_x=["cartesian"],info_y=["theta"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_d_cartesian,numpy_p1,outputFileName="./output_histo_2D_cartesian_phi",extensions="png,pdf",nrBins=[binning_deviation,100],info_x=["cartesian"],info_y=["phi"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_d_cartesian,np.cos(numpy_t1-numpy_t2),outputFileName="./output_histo_2D_cartesian_cos_theta",extensions="png,pdf",nrBins=[binning_deviation,100],info_x=["cartesian"],info_y=["cos theta"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_d_cartesian,np.cos(numpy_p1-numpy_p2),outputFileName="./output_histo_2D_cartesian_cos_phi",extensions="png,pdf",nrBins=[binning_deviation,100],info_x=["cartesian"],info_y=["cos phi"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_r1,numpy_r2,outputFileName="./output_histo_2D_r",extensions="png,pdf",nrBins=100,info_x=["r1"],info_y=["r2"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_t1,numpy_t2,outputFileName="./output_histo_2D_t",extensions="png,pdf",nrBins=100,info_x=["t1"],info_y=["t2"],title="Title",plotColorBar=True,debug=False,verbose=False)
            draw_histogram_2d(numpy_p1,numpy_p2,outputFileName="./output_histo_2D_p",extensions="png,pdf",nrBins=100,info_x=["p1"],info_y=["p2"],title="Title",plotColorBar=True,debug=False,verbose=False)
            #
            list_tupleArray=[]
            list_tupleArray.append((numpy_d_cartesian,"Carthesian"))
            list_tupleArray.append((numpy_d_spherical,"Spherical"))
            overlay_histogram_from_nparray_with_ratio(list_tupleArray,outputFileName="./output_histo_from_nparray",extensions="png,pdf",nrBins=binning_deviation,histtype="step",info_x=["deviation"],info_y=["Number of points"],title="Title",text=None,info_legend=["best"],list_color="r,g,b,k,y".split(","),doAddRatioPad=False,debug=False,verbose=False)
        # done if
    # done if coordinateSystemType
    # ready to return
    return numpy_deviation
# done function
