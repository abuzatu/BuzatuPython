# !/usr/bin/python
# Adrian Buzatu (adrian.buzatu@glasgow.ac.uk)
# 20 May 2013, Python functions to manipulate and draw histograms

# functions that help ROOT in general
from HelperPyRoot import *
# ROOT imports specific for the neural network
from ROOT import TMultiLayerPerceptron,TNeuron,TMLPAnalyzer

#########################################################################################
#### create the elements of the list of NNs to train style                           ####
#########################################################################################

def get_list_NN(initial_number,random_number_variations,neuron_activation_functions,learning_methods,
                input_layers,output_layers,hidden_layers,dict_tree_epoch, use_defaults_if_wrong_values,fileName,debug):

    if debug:
        print "input_layers",input_layers
        print "output_layers",output_layers
        print "hidden_layers",hidden_layers

    # option can contain:
    # - "text" (simple text output)
    # - "graph" (evoluting graphical training curves)
    # - "update=X" (step for the text/graph output update)
    # - "+" will skip the randomisation and start from the previous values.
    # - "current" (draw in the current canvas)
    # - "minErrorTrain" (stop when NN error on the training sample gets below minE
    # - "minErrorTest" (stop when NN error on the test sample gets below minE
    # All combinations are available.
    option="text, graph, current, update=1 +"

    # initialize a list to empty values
    list_NN=[]
    # now add to the list all the NN combinations we want
    # loop over how many random numbers you want
    if debug:
        print "random_number_variations",random_number_variations
    counter_NN=initial_number-1
    if True:
        # loop over activation functions
        for neuron_activation_function in neuron_activation_functions:
            # loop over learning methods
            for learning_method in learning_methods:
                # loop over input layers
                for input_layer in input_layers:
                    # loop over output layers
                    for output_layer in output_layers:
                        # loop over all the random numbers for this configuration
                        for i in xrange(random_number_variations):
                            counter_NN+=1
                            dict_tree_NN={}
                            # loop over all the trees to train on
                            for training_tree in dict_tree_epoch:
                                if debug:
                                    print "training_tree",training_tree
                                # append the current NN to the list
                                NN=["NN","n"+str(counter_NN),fileName,training_tree,
                                    neuron_activation_function,learning_method,dict_tree_epoch[training_tree],option,
                                    updateListVariables("",input_layer,""),hidden_layers,output_layer,
                                    use_defaults_if_wrong_values,debug]
                                if debug:
                                    print NN
                                dict_tree_NN[training_tree]=NN
                            # ended loop over training_trees
                            list_NN.append(dict_tree_NN)
                        # ended looping over random numbers
                    # ended looping over output layers
                # ended looping over input layers
            # ended looping over learning methods
        # ended looping over neuron activation functions
    # ended if True
    # if desired, print the list
    if debug:
        print_list_NN(list_NN)
    # done
    return list_NN
    #return get_list_NN_partial(list_NN,1,debug)
# done definition function

#########################################################################################
#### get the sublist with only these elemens that you want to keep                   ####
#########################################################################################

def get_sublist_NN_to_keep(list_NN,list_names):
    result=[]
    for NNdict in list_NN:
        NNname=NNdict[NNdict.keys()[0]][1]
        if False:
            print "NNname",NNname
        if NNname in list_names:
            result.append(NNdict) 
    # done
    return result
# done definition function

#########################################################################################
#### get the sublist by throwing away these elements                                 ####
#########################################################################################

def get_sublist_NN_to_reject(list_NN,list_names):
    result=[]
    for NNdict in list_NN:
        NNname=NNdict[NNdict.keys()[0]][1]
        if False:
            print "NNname",NNname
        if NNname not in list_names:
            result.append(NNdict) 
    # done
    return result
# done definition function


#########################################################################################
#### get the first elements of the NN list                                           ####
#########################################################################################

def get_list_NN_partial(list_NN,number,debug):
    result=[]
    for i,dict_tree_NN in enumerate(list_NN):
        if i>number-1:
            continue
        result.append(dict_tree_NN)
    if debug:
        print_list_NN(list_NN)
    # done
    return result
# done definition function

#########################################################################################
#### get the NN dictionary for a certain type                                        ####
#########################################################################################

def get_NNdict(list_NN,type,debug):
    for NNdict in list_NN:
        NNname=NNdict[NNdict.keys()[0]][1]
        if debug:
            print "desired type",type,"current NNname",NNname
        if NNname==type:
            if debug:
                print "Match found, we will return this element and exit function"
            return NNdict  
# done definition function

#########################################################################################
#### print the the NNs in a list                                                     ####
#########################################################################################

def print_list_NN(list_NN):
    for i,dict_tree_NN in enumerate(list_NN):
        for tree in dict_tree_NN:
            NN=dict_tree_NN[tree]
            print stringNN(NN,"b")
    return None
# done definition function

#########################################################################################
#### sum two list_NNs                                                                ####
#########################################################################################

def add_list_NN(list_NN):
    for i,dict_tree_NN in enumerate(list_NN):
        for tree in dict_tree_NN:
            NN=dict_tree_NN[tree]
            print stringNN(NN,"b")
    return None
# done definition function

#########################################################################################
#### get a string of the elements of a NN                                            ####
#########################################################################################

def stringNN(NN,option):
    if option=="a":
        result="NN_folder "+NN[0]+" NN_name="+NN[1]+" fileName="+NN[2]+" treeName="+NN[3]+" NN_neuron_activation_function="+NN[4]+" NN_learning_method="+NN[5]+" NN_epochs="+str(NN[6])+" NN_train_option="+NN[7]+" NN_input_layer="+NN[8]+" NN_hidden_layers="+NN[9]+" NN_output_layer="+NN[10]+" use_defaults_if_wrong_values="+str(NN[11])+" debug="+str(NN[12])
    elif option=="b":
        result="%-4s %-25s %-7s %-7s %-4s %-10s %-3s %-6s %-90s" % (NN[1], NN[3],NN[4],NN[5],str(NN[6]),NN[10],NN[9],str(NN[11]),NN[8])    
    elif option=="c":
        result="%-7s %-7s %-4s %-100s %-10s %-10s" % (NN[4],NN[5],str(NN[6]),NN[8],NN[10],str(NN[11]))    
    elif option=="d":
        result="%-7s %-7s %-4s %-75s" % (NN[4],NN[5],str(NN[6]),NN[8])    
    else:
        print "option",option,"not known. WILL ABORT!!!"
        return None
    # now ready to return
    return result
# done function

#########################################################################################
#### import a NN from its module based on its name                                 ######
#########################################################################################

def studyFileErrors(fileName,debug):
    if debug:
        "Studying file",fileName
    bestNrEpoch=9999
    bestTestError=9999.0
    #lines = [line.strip() for line in open(fileName)]
    #for line in lines:
    with open(fileName) as file_:
        for line in file_:
            if "Epoch" not in line:
                continue
            if debug:
                print line
            elements=line.split(" ")
            if debug:
                print elements
            nrEpoch=elements[1]
            train=elements[2]
            test=elements[3]
            trainError=float(train.split("=")[1])
            testError=float(test.split("=")[1])
            if debug:
                print nrEpoch,trainError,testError
            if testError<bestTestError:
                bestTestError=testError
                bestNrEpoch=nrEpoch
    # ended loop over all the lines
    if debug:
        print "Best testError is",bestTestError,"for nrEpoch",bestNrEpoch
    # add one as we started counting from zero
    bestNrEpoch=int(bestNrEpoch)+1
    bestTestError=float(bestTestError)
    return bestNrEpoch,bestTestError
# function definition ended

#########################################################################################
#### train a NN, see examples in test.py, either on a per-jet or a per-event basis   ####
#########################################################################################

def trainNN(file_training_name,doRandomize,NN,suffix,debug):

    print "############## Start trainNN(...) ###############"
    print "NN=",NN,"suffix",suffix

    # fill the information from NN
    folder=NN[0]
    name=NN[1]
    fileName=NN[2]
    treeName=NN[3]
    neuron_activation_function=NN[4]
    learning_method=NN[5]
    epochs=NN[6]
    option=NN[7]
    input_layer=NN[8]
    hidden_layers=NN[9]
    output_layer=NN[10]
    use_defaults_if_wrong_values=NN[11]
    debug=NN[12]

    print "debug",debug

    # hard code values for trainining parameters (in the future to put as inputs)
    default=False
    if default:
        eta=0.1
        etadecay=1.0
        delta=0.0
        reset=50
    else:
        eta=0.000001
        etadecay=0.9999
        delta=0.0
        reset=50

    # open TFile
    file=TFile(fileName)
    if not not file:
        print "TFile",fileName,"opened sucessfully."
    else:
        print "TFile",fileName,"could not be opened."
    # get TTree from TFile
    tree=file.Get(treeName)
    if not not tree:
        print "TTree",treeName,"opened sucessfully."
    else:
        print "TTree",treeName,"could not be opened."
    print type(tree)
    # get number of entries in the tree
    nentries=tree.GetEntries()
    print "TTree",treeName,"has",nentries,"entries. We will use them for training."

    # create the structure of NN
    input_layer=listVariables(input_layer,"@")  # add the normalization of variables by default
    if hidden_layers=="":
        if use_defaults_if_wrong_values:
            hidden_layers=':'+str(len(input_layer.split(',')))+':'
        else:
            print "Your desired hidden_layers is empty, it should be : followed by a number followed by : followed by another number followed by :, for as many hidden layers that you want. Will ABORT!!!"
            assert(False)
        # done if
    structure = input_layer+hidden_layers+output_layer

    # check the user asked for a known neuron activation function
    list_possible_neuron_activation_functions=["Linear","Sigmoid","Tanh","Gauss"]
    if neuron_activation_function not in list_possible_neuron_activation_functions:
        if use_defaults_if_wrong_values:
            neuron_activation_function="Sigmoid"
        else:
            print "Your desired neuron_activation_function",neuron_activation_function,"not known. Need to choose from",list_possible_neuron_activation_functions,". Will ABORT!!!"
            assert(False)
        # done if

    # check the user asked for a known learning method
    list_possible_learning_methods=["Stochastic","Batch","SteepestDescent","RibierePolak","FletcherReeves","BFGS"]
    if learning_method not in list_possible_learning_methods:
        if use_defaults_if_wrong_values:
            learning_method="BFGS"
        else:
            print "Your desired learning_method",learning_method,"not known. Need to choose from",list_possible_learning_methods,". Will ABORT!!!"
            assert(False)
        # done if
    
    # add the NN_counter to the name, to distinguish them
    name_weights=name+"_"+treeName
    name=name+suffix+"_"+treeName

    # print values if debug
    if debug:
        print "folder",folder
        print "name",name
        print "file used in training",fileName
        print "tree from file used in training",treeName
        print "input_layer",input_layer
        print "hidden_layers",hidden_layers # notice plural!
        print "output_layer",output_layer
        print "structure",structure
        print "epochs",epochs
        print "option",option
        print "neuron_activation_function",neuron_activation_function
        print "learning_method",learning_method
        print "doRandomize",doRandomize
        print "eta",eta
        print "etadecay",etadecay
        print "delta",delta
        print "reset",reset

    #exit()

    # create the NN object of the type MultiLayerPerceptron
    mlp=TMultiLayerPerceptron(structure, tree,"Train==1","Train==0",getattr(TNeuron,"k"+neuron_activation_function))
    #mlp=TMultiLayerPerceptron(structure, tree,"(Entry$%2)==0","(Entry$%2)!=0",getattr(TNeuron,"k"+neuron_activation_function))
    #mlp=TMultiLayerPerceptron(structure, tree,"Entry$%2","(Entry$+1)%2",getattr(TNeuron,"k"+neuron_activation_function))
    SetOwnership(mlp,0)

    # set the training dataset
    #mlp.SetTrainingDataSet(listTrain)
    
    # set the testing dataset
    #mlp.SetTestDataSet(listTest)

    # now set the learning method
    mlp.SetLearningMethod(getattr(TMultiLayerPerceptron,"k"+learning_method))

    # now set eta,etadecay,delta and reset
    mlp.SetEta(eta)
    mlp.SetEtaDecay(etadecay)
    mlp.SetDelta(delta)
    mlp.SetReset(reset)

    if debug:
        print "before training"
        print "Eta",mlp.GetEta()
        print "EtaDecay",mlp.GetEtaDecay()
        print "Delta",mlp.GetDelta()
        print "Reset",mlp.GetReset()

    # we need to create a canvas first so that the plots produced by default will 
    # be saved to a .pdf file, otherwise we lose them
    # for example, NN error vs number epochs

    # Create a canvas with a left and right side
    c=TCanvas(name,name,200,10,800,500)

    # divide the canvas into 4, as we will plot 4 plots
    c.Divide(2,2)
    
    # go o the first one (top left corner)
    c.cd(1)
    # now we train the NN with the desired number of epochs, 
    # while also getting a canvas with the NN error vs the number of epochs
    # and a text with these values
    #
    # now open the files when saving the cout from NN training to file  
    # but first save the number of epochs to a file
    # so that we can manipulate that info to get the best number of epochs
    # for which the test error is minimum
    save=os.dup(sys.stdout.fileno())
    fileErrors="./errors/"+name+".txt"
    newout=open(fileErrors,"w")
    os.dup2(newout.fileno(),sys.stdout.fileno())
    #
    # but we want to measure how long it takes to train
    # so get the current time (in seconds since 1970 ...)
    sec_start=int(round(time.time()))
    # now we can train 
    # mlp.Train(100,"text graph update=10") # for example
    # the plot NN error vs number epochs is created here if 
    # option contains the string "graph current"
    # now ready to train NN
    # randomize the NN numbers only if we say so, and the option should have by default + it so that 
    # the randomization is not updated if we do not want to
    # this is crucial for finding the best number of epochs and then running again on the same NN
    # i.e. with the same random number as before, i.e. without randomization
    fileWeights="./weights/"+name_weights+"_weights.txt"
    if doRandomize:
        mlp.Randomize()
        mlp.DumpWeights(fileWeights)
    else:
        mlp.LoadWeights(fileWeights)
        if os.path.exists(fileWeights):
            os.remove(fileWeights)
    # now ready to train
    mlp.Train(epochs,option)
    # finished NN training
    # finished training, so now get the current time (in seconds since 1970 ...)
    sec_finish = int(round(time.time()))
    NN_run_time=sec_finish-sec_start
    if debug:
        print "Run time:",NN_run_time, "seconds"  
    # now close the files when saving the cout from NN training to file    
    os.dup2(save,sys.stdout.fileno())
    newout.close()
    os.close(save)
    # now we can find the best number of epochs
    nrEpoch,testError=studyFileErrors(fileErrors,False)

    # go to the second one (top right corner)
    c.cd(2)
    # draws the mlp already trained with the structure and thicker lines 
    # for the most important synapses (connection between the neurons)
    mlp.Draw()

    # go to the third one (bottom left corner)
    c.cd(3)
    # define ana an object that analyses the mlp already trained
    ana=TMLPAnalyzer(mlp)
    # now fill ana with the information it has to analyse
    ana.GatherInformations()
    # draws the inputs derivatives (the smaller the value, 
    # the less sensitive is the NN output on the variable change in the input)
    ana.DrawDInputs()

    # go to the fourth one (bottom right corner)
    c.cd(4)
    # draws truth deviations
    ana.DrawTruthDeviations("")
    #ana.DrawDInput(1)
    # now the canvas is ready, we can save it to a file
    c.Print("./plot/"+name+".pdf")
    # c.Print("./plot/"+name+".eps")
    # c.Print("./plot/"+name+".gif")

    if debug:
        print "after training"
        print "Eta",mlp.GetEta()
        print "EtaDecay",mlp.GetEtaDecay()
        print "Delta",mlp.GetDelta()
        print "Reset",mlp.GetReset()


    # then save the NN function in Python format 
    mlp.Export(name, "Python")
    call(["mv",name+".py",folder])
    # if we want, we can also save it in C++ format (.cxx and .h)
    mlp.Export(name, "C++")
    # now move the NN files to the NN folder
    call(["mv",name+".cxx",folder])
    call(["mv",name+".h",folder])

    # save info about NN
    file_training=open(file_training_name,"a")
    file_training.write(name+" trained for "+str(NN_run_time)+" seconds, best nrEpoch "+str(nrEpoch)+" best testError "+str(testError)+" : "+stringNN(NN,"b")+"\n")

    file_training.close()

    # now we are done
    print "############## End trainNN(...) #################"
    # return the name of the NN
    return nrEpoch,testError
# function definition ended

#########################################################################################
#### import a NN from its module based on its name                                 ######
#########################################################################################

def get_info_NN(nnName,treeName,debug):
    if debug:
        print "Retrieveing the info about the NN of name",nnName,"and tree",treeName
    list_NN_all=get_list_NN_all()
    if debug:
        print "list_NN_all",list_NN_all
        print " "
    list_names_to_keep=[nnName]
    if debug:
        print "list_names_to_keep",list_names_to_keep
    list_NN=get_sublist_NN_to_keep(list_NN_all,list_names_to_keep)
    # now the list has only one NN name with our choice, but there is in fact
    # a dictionary of name to NNs for all jets, per jet1 and per jet 2.
    dict_NN=list_NN[0]
    # from the dictionary get the NN of the type we want (per jet1, for example)
    info_NN=dict_NN[treeName]
    if debug:
        print "info_NN",info_NN
        print " "
    return info_NN
# function definition ended

#########################################################################################
#### import a NN from its module based on its name                                 ######
#########################################################################################

def importNN(name,debug):
    if debug:
        print "Importing Python module for NN named",name
    NN_module=__import__(name)
    NN_class=getattr(NN_module, name)
    NN_instance=NN_class() # the instance of the class is our NN
    return NN_instance
# function definition ended

