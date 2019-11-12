#!/usr/bin/env python3

import numpy as np

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
            print(axisName,structured_array[axisName].astype('f4'),type(structured_array[axisName].astype('f4')),structured_array[axisName].astype('f4').dtype)
        # done if
        temp_data.append(structured_array[axisName].astype('f4'))
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
        print("pc_current[:,1]",type(pc_current[:,1]))
        print(pc_current[:,1])
        print("[np.round(pc_current[:,1]).astype(np.uint32)",type(np.round(pc_current[:,1]).astype(np.uint32)))
        print(np.round(pc_current[:,1]).astype(np.uint32))
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
    # and here have access at the values of each column
    # such as to store in a histogram and then plot them
    if False:
        for i in xrange(M):
            if debug:
                print("axis i",i)
            # the column along the i-th axis
            # 1 is the second dimension, hence the one with axis
            # then from the axes we take the one with number i
            nparray_column=np.take(pc_current_deviation,i,1)
            column_max=np.max(nparray_column)
            column_avg=np.mean(nparray_column)
            if debug:
                print("max",column_max,"avg",column_avg)
            # create a histogram from the full distribution of the column
            # and save it in a plot
        # done loop over dimensions
    # done if
    return pc_current_deviation,columns_max,columns_avg
# done function
