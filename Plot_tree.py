# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 21:10:10 2018

@author: Administrator
"""

import matplotlib.pyplot as plt

# Define text box and arrow formats
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

# Draw annotations with arrows
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def Num_of_leaf(myTree):
    """Calculate the number of leaf nodes in this tree"""
    num_leaf = 0
    first_node = list(myTree.keys())[0]  # Access first key directly after converting to list
    second_dict = myTree[first_node]
    # Python3 uses LIST conversion, [0] direct indexing is only for Python2
    # For the tree, check each value for dictionary, recurse if dict, else increment
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            num_leaf += Num_of_leaf(second_dict[key])
        else:
            num_leaf += 1
    return num_leaf


def Depth_of_tree(myTree):
    """Calculate the total depth of this tree"""
    depth = 0
    first_node = list(myTree.keys())[0]
    second_dict = myTree[first_node]

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            pri_depth = 1 + Depth_of_tree(second_dict[key])
        else:
            pri_depth = 1
        # For the tree, check if value is dict, recurse if true, else increment
        if pri_depth > depth:
            depth = pri_depth
    return depth


def retrieveTree(i):
    """
    Saved tree test data
    """
    listOfTrees = [
        {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
        {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
    ]
    return listOfTrees[i]


def plotmidtext(cntrpt, parentpt, txtstring):
    """Calculate the middle position of the tree
    cntrpt: start position, parentpt: end position, txtstring: text label
    """
    xmid = (parentpt[0] - cntrpt[0]) / 2.0 + cntrpt[0]
    # cntrPt start coordinates, child node coordinates
    # parentPt end coordinates, parent node coordinates
    ymid = (parentpt[1] - cntrpt[1]) / 2.0 + cntrpt[1]  # Find the middle of x and y
    createPlot.ax1.text(xmid, ymid, txtstring)


def plottree(mytree, parentpt, nodetxt):
    numleafs = Num_of_leaf(mytree)
    firststr = list(mytree.keys())[0]
    cntrpt = (plottree.xoff + (1.0 + float(numleafs)) / 2.0 / plottree.totalw, plottree.yoff)
    # Calculate child node coordinates
    plotmidtext(cntrpt, parentpt, nodetxt)  # Draw text on the line
    plotNode(firststr, cntrpt, parentpt, decisionNode)  # Draw node
    seconddict = mytree[firststr]
    plottree.yoff = plottree.yoff - 1.0 / plottree.totald
    # Each time a graph is drawn, reduce y by 1.0/plottree.totald, ensuring depth on y-axis
    for key in seconddict.keys():
        if type(seconddict[key]).__name__ == 'dict':
            plottree(seconddict[key], cntrpt, str(key))
        else:
            plottree.xoff = plottree.xoff + 1.0 / plottree.totalw
            plotNode(seconddict[key], (plottree.xoff, plottree.yoff), cntrpt, leafNode)
            plotmidtext((plottree.xoff, plottree.yoff), cntrpt, str(key))
    plottree.yoff = plottree.yoff + 1.0 / plottree.totald


def createPlot(intree):
    # Like Matlab's figure, define a canvas, background is white
    fig = plt.figure(1, facecolor='white')
    fig.clf()  # Clear the canvas
    axprops = dict(xticks=[], yticks=[])
    # createPlot.ax1 is global, handle for drawing, subplot defines a plot
    # 111 means 1 row, 1 column, i.e., 1 graph, the last 1 is the first graph
    # frameon indicates whether to draw the axes rectangle
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)

    plottree.totalw = float(Num_of_leaf(intree))
    plottree.totald = float(Depth_of_tree(intree))
    plottree.xoff = -0.5 / plottree.totalw
    plottree.yoff = 1.0
    plottree(intree, (0.5, 1.0), '')
    plt.show()