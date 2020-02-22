#!/usr/bin/env python3

# import for data analysis and plotting
import matplotlib.pylab as pylab
#import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.axes as ax
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.gridspec as gridspec
import copy

# a general function to print the values and other properties of a numpy array
# use to see the values of the numpy arrays in our code for debugging and understanding the code flow
def print_nparray(name,nparray):
    print("")
    print(name)
    print(nparray)
    print("type",type(nparray),"shape",nparray.shape,"min_value=%.3f"%np.min(nparray),"min_position=%.0f"%np.argmin(nparray),"max_value=%.3f"%np.max(nparray),"max_position=%.0f"%np.argmax(nparray))
# done function

# overlay two or more numpy arrays as graphs
# info_legend="best", "uppler right", "lowerleft", etc
# info_y: info_y=["Figure of merit of performance",[0.0,100000.0,-1]
# info_y: info_y=["Figure of merit of performance",[-1,-1,1.5]

def overlayGraphsValues(list_tupleArray,outputFileName="overlay",extensions="pdf,png",info_x=["Procent of data reduced",[0.0,1.0],"linear"],info_y=["Figure of merit of performance",[0.0,100000.0,-1],"log"],info_legend=["best",6],title="Compared performance of 3D point cloud compression",doShow=False,debug=False):
    if debug:
        print("Start overlayGraphsValues")
        print("outputFileName",outputFileName)
        print("extensions",extensions)
        print("info_x",info_x)
        print("info_y",info_y)
        print("info_legend",info_legend)
        print("title",title)
    # x axis
    x_label=info_x[0]
    x_lim=info_x[1]
    x_lim_min=x_lim[0]
    x_lim_max=x_lim[1]
    if x_lim_min==-1 and x_lim_max==-1:
        x_set_lim=False
    else:
        x_set_lim=True
    x_scale=info_x[2]
    if debug:
        print("x_label",x_label,type(x_label))
        print("x_lim_min",x_lim_min,type(x_lim_min))
        print("x_lim_max",x_lim_max,type(x_lim_max))
        print("x_set_lim",x_set_lim,type(x_set_lim))
        print("x_scale",x_scale,type(x_scale))
    # y axis
    y_label=info_y[0]
    y_lim=info_y[1]
    y_lim_min=y_lim[0]
    y_lim_max=y_lim[1]
    y_lim_scale_min=y_lim[2]
    y_lim_scale_max=y_lim[3]
    if y_lim_min==-1 and y_lim_max==-1:
        y_set_lim=False
    else:
        y_set_lim=True
    y_scale=info_y[2]
    if debug:
        print("y_label",y_label,type(y_label))
        print("y_lim_min",y_lim_min,type(y_lim_min))
        print("y_lim_max",y_lim_max,type(y_lim_max))
        print("y_lim_scale_min",y_lim_scale_min,type(y_lim_scale_min))
        print("y_lim_scale_max",y_lim_scale_max,type(y_lim_scale_max))
        print("y_set_lim",y_set_lim,type(y_set_lim))
        print("y_scale",y_scale,type(y_scale))
    # find the maximum y value
    max_y=np.NINF
    min_y=np.inf
    for i,tupleArray in enumerate(list_tupleArray):
        if debug:
            print("i",i,"len",len(tupleArray))
        temp_max=np.max(tupleArray[1])
        if temp_max>max_y:
            max_y=temp_max
        temp_min=np.min(tupleArray[1])
        if temp_min<min_y:
            min_y=temp_min
    # done for loop
    if debug:
        print("max_y",max_y)
    # create empty figure
    plt.figure(1)
    # set x-axis
    plt.xlabel(x_label)
    if x_set_lim==True:
        plt.xlim(x_lim_min,x_lim_max)
    plt.xscale(x_scale)
    # set y-axis
    plt.ylabel(y_label)
    if y_set_lim==True:
        plt.ylim(y_lim_min,y_lim_max)
    else:
        if max_y>0 and min_y>0:
            # multiply by y_lim_scale upwards to give enough space for the legend and by 0.9 downwards
            plt.ylim(min_y*y_lim_scale_min,max_y*y_lim_scale_max)
        # done if
    # done if
    plt.yscale(y_scale)
    # set title
    plt.title(title)
    # fill content of plot
    for i,tupleArray in enumerate(list_tupleArray):
        if debug:
            print("i",i,"len",len(tupleArray))
        x=tupleArray[0]
        y=tupleArray[1]
        color=tupleArray[2]
        marker=tupleArray[3]
        l=tupleArray[4]
        # print("c",c)
        # plt.plot(x,y,c,label=l)
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
        plt.plot(x,y,color=color,marker=marker,label=l)
    # done loop over each element to plot
    # set legend
    if True:
        plt.legend(loc=info_legend[0],prop={'size':info_legend[1]})
    if doShow:
        plt.show()
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print("Saving plot at",fileNameFull)
        plt.savefig(fileNameFull)
    # close the figure
    plt.close()
# done function

def draw_histogram_from_nparray(nparray,outputFileName="./output_histo_from_nparray",extensions="png,pdf",nrBins=100,info_x=["x-axis","linear"],info_y=["Number of points","linear"],title="Title",text=None,debug=False,verbose=False):
    if debug:
        print("Start draw_histogram_from_nparray()")
        print("outputFileName",outputFileName)
        print("extensions",extensions)
        print("info_x",info_x)
        print("info_y",info_y)
        print("title",title)
    # 
    fig=pylab.figure()
    #fig=matplotlib.pylab.figure()
    ax = fig.add_subplot(111)
    n,b,patches=ax.hist(nparray,bins=nrBins)
    if debug:
        print("n",n)
        print("b",b)
        print("patches",patches)
        print("max",n.max())
    # axes
    x_label,x_scale=info_x
    y_label,y_scale=info_y
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale(x_scale)
    plt.yscale(y_scale)
    plt.ylim(0,n.max()*1.2)
    # title
    plt.title(title)
    # text
    if text is not None:
        plt.text(0.2,0.9,text,bbox=dict(facecolor='red', alpha=0.5),horizontalalignment="left",fontstyle="oblique",transform=ax.transAxes)
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print("Saving plot at",fileNameFull)
        plt.savefig(fileNameFull)
    # close the figure
    plt.close()
# done function

# histtype: bar, barstacked, step, stepfilled
# nrBins: 100 or list of bins edges
# option A: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.hist.html
# only option A works if we want to add a text in the plot whose size is relative to the plot and not to the values plotted
# option B: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.hist.html
# to color different bins in different colors, like a rainbow gradient https://stackoverflow.com/questions/23061657/plot-histogram-with-colors-taken-from-colormap
# obtain the max value: # https://stackoverflow.com/questions/15558136/obtain-the-max-y-value-of-a-histogram
# plotting two histograms in one plt.hist did not work for me easily, but I loop over list of arrays anyway, as I need to give them different labels and colors etc
def overlay_histogram_from_nparray(list_tupleArray,outputFileName="./output_histo_from_nparray",extensions="png,pdf",nrBins=100,histtype="step",info_x=["x-axis"],info_y=["Number of points"],title="Title",text=None,info_legend=["best"],debug=False,verbose=False):
    if debug:
        print("Start draw_histogram_from_nparray()")
        print("outputFileName",outputFileName)
        print("extensions",extensions)
        print("info_x",info_x)
        print("info_y",info_y)
        print("title",title)
    # 
    style="A"
    if style=="A":
        fig=pylab.figure()
        for i,(nparray,legendText) in enumerate(list_tupleArray):
            ax = fig.add_subplot(111)
            n,b,patches=ax.hist(nparray,bins=nrBins,alpha=1.0,color=list_color[i],histtype=histtype,label=legendText)
            max_y=n.max()
            if debug:
                print("n",n)
                print("b",b)
                print("patches",patches)
                print("max_y",max_y)
    if style=="B":
        for i,tupleArray in enumerate(list_tupleArray):
            print("tupleArray",tupleArray)
            nparray,legendText=tupleArray
            print("nparray",nparray)
            print("legendText",legendText)
            print("i",i)
            
            y,x,a=plt.hist(nparray,bins=nrBins,alpha=1,color=list_color[i],histtype=histtype,label=legendText)
            # note y (vertical) is returned before x (horizontal)
            print("x",type(x),x)
            print("y",type(y),y)
            #print(type(x),x,len(x),x.shape,np.min(x),np.max(x),np.sum(x))
            #print(type(y),y,len(y),y.shape,np.min(y),np.max(y),np.sum(y))
            #print(type(a),a)
            max_y=np.max(y)
            #print_nparray("x",legendText,"x",x)
            #print_nparray("x",legendText,"y",y)
            #print_nparray("x",legendText,"a",a)
    # axes
    x_label,x_scale=info_x
    y_label,y_scale=info_y
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(0,max_y*1.2)
    # title
    plt.title(title)
    # text
    if text is not None:
        plt.text(0.2,0.9,text,bbox=dict(facecolor='red', alpha=0.5),horizontalalignment="left",fontstyle="oblique",transform=ax.transAxes)
    # legend
    # set legend
    plt.legend(loc=info_legend[0])
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print("Saving plot at",fileNameFull)
        plt.savefig(fileNameFull)
    # close the figure
    plt.close()
# done function

# histtype: bar, barstacked, step, stepfilled
# nrBins: 100 or list of bins edges
# option A: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.hist.html
# only option A works if we want to add a text in the plot whose size is relative to the plot and not to the values plotted
# option B: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.hist.html
# to color different bins in different colors, like a rainbow gradient https://stackoverflow.com/questions/23061657/plot-histogram-with-colors-taken-from-colormap
# obtain the max value: # https://stackoverflow.com/questions/15558136/obtain-the-max-y-value-of-a-histogram
# plotting two histograms in one plt.hist did not work for me easily, but I loop over list of arrays anyway, as I need to give them different labels and colors etc
def overlay_histogram_from_nparray_with_ratio(list_tupleArray,outputFileName="./output_histo_from_nparray",extensions="png,pdf",nrBins=100,histtype="step",info_x=["x-axis"],info_y=["Number of points"],title="Title",text=None,info_legend=["best"],list_color="r,g,b,k,y".split(","),doAddRatioPad=False,debug=False,verbose=False):
    if debug:
        print("Start draw_histogram_from_nparray()")
        print("outputFileName",outputFileName)
        print("extensions",extensions)
        print("info_x",info_x)
        print("info_y",info_y)
        print("title",title)
    # 
    max_y=np.NINF # negative infinity
    fig=pylab.figure()
    n_reference=0
    for i,(nparray,legendText) in enumerate(list_tupleArray):
        if debug:
            print("i",i,legendText,nparray)
        if doAddRatioPad:
            ax=fig.add_subplot(211)
        else:
            ax=fig.add_subplot(111)
        n,b,patches=ax.hist(nparray,bins=nrBins,alpha=1.0,color=list_color[i],histtype=histtype,label=legendText)
        if n.max()>max_y:
            max_y=n.max()
        if debug:
            print_nparray("n",n)
            print_nparray("b",b)
            print("patches",patches)
            print("max_y",max_y)
        if doAddRatioPad:
            if i==0:
                n_reference=copy.deepcopy(n)
            # calculate ratio of number of bins
            n_ratio=n/n_reference
            if debug:
                print_nparray("n_reference",n_reference)
                print_nparray("n_ratio",n_ratio)
            # add the ratio as numpy arrays
            ax2=fig.add_subplot(212)
            ax2.plot(b[1:],n_ratio,c=list_color[i],label=legendText)
        # done if doAddRatioPad
    # done loop over histograms
    # axes
    x_label=info_x[0]
    y_label=info_y[0]
    # ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(0,max_y*1.2)
    # title
    ax.set_title(title)
    # text
    if text is not None:
        ax.text(0.2,0.9,text,bbox=dict(facecolor='red', alpha=0.5),horizontalalignment="left",fontstyle="oblique",transform=ax.transAxes)
    # legend
    # set legend
    ax.legend(loc=info_legend[0])
    if doAddRatioPad:
        ax2.legend(loc=info_legend[0])
        ax2.set_ylabel("Ratio to "+list_tupleArray[0][1])
        ax2.set_xlabel(x_label)
    else:
        ax.set_xlabel(x_label)
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print("Saving plot at",fileNameFull)
        plt.savefig(fileNameFull)
        # close the figure
    plt.close()
# done function


# x=horizontal, y=vertical; nrBins=100, or nrBins=[0,1,2,3,4]
def draw_histogram_2d(x,y,outputFileName="./output_histo_2D",extensions="png,pdf",nrBins=100,info_x=["x-axis"],info_y=["y-axis"],title="Title",plotColorBar=True,debug=False,verbose=False):
    plt.hist2d(x,y,bins=nrBins,cmin=1)
    if plotColorBar:
        plt.colorbar()
    # axes
    x_label=info_x[0]
    y_label=info_y[0]
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # title
    plt.title(title)
    # save plots
    for extension in extensions.split(","):
        plt.savefig(outputFileName+"."+extension)
    # done loop over extension
    plt.close()
# done function
