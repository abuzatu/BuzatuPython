#!/usr/bin/python
from HelperPython import *

def example_format_string():
    list_values=[
        ["bla", 1, 0.0, 30.0, 0.0, 0.0],
        ["bla22",5, 170.0, 190.0, 559.06, 30.65],
        ["bla333",16, 500.0, 1300.0, 7.22, 2.38],
        ]
    for text,i,binLowEdge,binHighEdge,binContent,binError in list_values:
        line="%8s bin %4.0f range [%4.0f,%4.0f] value %8.2f error %8.2f" % (text,i,binLowEdge,binHighEdge,binContent,binError)
        print line
    #     bla bin    1 range [   0,  30] value     0.00 error     0.00
    #   bla22 bin    5 range [ 170, 190] value   559.06 error    30.65
    #  bla333 bin   16 range [ 500,1300] value     7.22 error     2.38
    for text,i,binLowEdge,binHighEdge,binContent,binError in list_values:
        line="%-8s bin %-4.0f range [%-4.0f,%4.0f] value %-8.2f error %-8.2f" % (text,i,binLowEdge,binHighEdge,binContent,binError)
        print line
    # bla      bin 1    range [0   ,  30] value 0.00     error 0.00    
    # bla22    bin 5    range [170 , 190] value 559.06   error 30.65   
    # bla333   bin 16   range [500 ,1300] value 7.22     error 2.38 
    # Notice how - arranges to the left and lack of - arranges to the righ!
# done function

def getFileNameStem(fileName,debug=False):
  if debug:
    print "fileName",fileName
  fileNameSplitBySlash=fileName.split("/")
  # now pick the last element, which means with path removed
  # find out how many elements are in the list
  nrElements=len(fileNameSplitBySlash)
  fileNameWithoutPath=fileNameSplitBySlash[nrElements-1]
  if debug:
    print "fileNameWithoutPath",fileNameWithoutPath
  fileNameStem=fileNameWithoutPath.split(".")[0]
  if debug:
    print "fileNameStem",fileNameStem
  # a bit hard coded, but we know the name of the root files start with
  # train_tree_ and we want to remove that, it has 11 characters
  fileNameStem=fileNameStem[12:]
  if debug:
    print "fileNameStem",fileNameStem
  return fileNameStem
# done function

def get_list_fileFromFolder(inputFolderName,fileSearch="*.root",debug=False):
    result=[]
    proc = subprocess.Popen(["ls -1 "+inputFolderName+"/"+fileSearch], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if debug:
        print type(out),out
    for file in out.split():
        if debug:
            print "file",file
        result.append(file.strip('\n'))
    # the file name contains full path
    if debug:
        print "list_file:"
        for file in result:
            print file
    return result
# done function

# optionOpenFile="w" # create from scratch, "a", append to an already existing file
# in which case be sure to name the list differently
def get_python_list_filesFromFolder(inputFolderName,fileSearch="*.root",
                                    outputFileName="list.py",optionOpenFile="w",
                                    listName="list_outputFile",
                                    debug=False):
    outputFile=open(outputFileName,optionOpenFile)
    if optionOpenFile=="w":
        line="#!/usr/bin/python\n"
        outputFile.write(line)
    elif optionOpenFile=="a":
        # will append
        None
    else:
        print "optionOpenFile",optionOpenFile,"not known. Choose w (rewrite), a (append). Will ABORT!!!"
        assert(False)
    # end if
    line=" \n"
    outputFile.write(line)
    line=listName+"=[\n"
    outputFile.write(line)
    list_fileName=get_list_fileFromFolder(inputFolderName,fileSearch,debug)
    for fileName in list_fileName:
        print "fileName",fileName
        line="    \""+fileName+"\",\n"
        outputFile.write(line)
    # done loop over files
    line="]\n"
    outputFile.write(line)
    outputFile.close()
    if True:
        print "File ",outputFileName,"has been created."
# done function

def get_list_from_file(fileName,debug=False):
    # it assumes there is one element per line
    list_line=[]
    for line in open(fileName, 'r'):
        line=line.rstrip()
        if debug:
            print "line",line
        list_line.append(line)
    # done for loop over lines
    if debug:
        print "list_line",list_line
    return list_line
# done function

# read a value from a file that has only one number inside
def get_value_from_file(fileName,debug):
    # we assume there is only one line, and on that line only one value
    with open(fileName) as f:
        value=float(f.readline().rstrip())
    if debug:
        print "value from fileName",fileName,"is value",value
    return value
# done function

##########################################################################################################
################### Write values nicely in a table format later to be read as numpy ######################
##########################################################################################################

# e.g. 
# list_list_varInfo=[
#    ["option","s",18,"l",0],
#    ["value","f",9,"r",2],
#    ]
# append_performance_to_file(performanceFileName,list_list_varInfo,dict_varName_value)

def get_stringFormat(list_varInfo,option,debug=False):
    varName,varType,stringLength,side,nrDigitsAfterDot=list_varInfo
    # overwrite the float to s for the first line of header of the file
    if option=="s":
        varType="s"
    elif option=="f":
        pass
    else:
        print "option",option,"not known. Must be s or f. String or Float. Will ABORT!!!"
        assert(False)
    # done if
    if debug:
        print "option",option,"varType",varType
    # start build the stringFormat
    stringFormat="%"
    # add if arranged to the left of to the right
    # usually pure strings want to be arranged to the left
    # and numbers arranged to the right
    if side=="l":
        stringFormat+="-" # %-25s
    elif side=="r":
        pass # %25s
    else:
        print "side",side,"not known. Choose l or r. Left or Right. Will ABORT!!!"
        assert(False)
    # done if
    # add the length of the string
    stringFormat+=str(stringLength)
    # add the fact that it is a string or a float
    if varType=="s":
        stringFormat+="s"
    elif varType=="f":
        stringFormat+="."+str(nrDigitsAfterDot)+"f" # %15.4f or %-15.4f
    else:
        print "varType",varType,"not known. Choose s or f. String or Float. Will ABORT!!!"
        assert(False)
    # done if
    return stringFormat
# done function

def get_performanceText_names(list_list_varInfo,debug):
    if debug:
        print "Start get_performanceText_names()"
    performanceText=""
    for list_varInfo in list_list_varInfo:
        stringFormat=get_stringFormat(list_varInfo,"s")
        varName=list_varInfo[0]
        if debug:
            print "stringFormat",stringFormat,"varName",varName
        performanceText+=stringFormat % varName
    # done for loop
    if debug:
        print "performanceText",performanceText
    return performanceText
# done function

def get_performanceText_values(list_list_varInfo,dict_varName_value,debug):
    if debug:
        print "Start get_performanceText_values()"
    performanceText=""
    for list_varInfo in list_list_varInfo:
        stringFormat=get_stringFormat(list_varInfo,"f")
        varName=list_varInfo[0]
        if debug:
            print "stringFormat",stringFormat,"varName",varName
        performanceText+=stringFormat % dict_varName_value[varName]
    # done for loop
    if debug:
        print "performanceText",performanceText
    return performanceText        
# done function

def append_performance_to_file(performanceFileName,list_list_varInfo,dict_varName_value,debug):
    exists=os.path.isfile(performanceFileName)
    if exists==False:
        with open(performanceFileName, "w") as myFile:
            performanceText=get_performanceText_names(list_list_varInfo,debug)
            myFile.write(performanceText+"\n")
        myFile.close()
    # done if
    with open(performanceFileName, "a") as myFile:
        performanceText=get_performanceText_values(list_list_varInfo,dict_varName_value,debug)
        myFile.write(performanceText+"\n")
    myFile.close()
# done function

#################################################################
################### Finished ####################################
#################################################################
