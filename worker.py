#This will allow us to multi process - thus make things run faster!

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os
import pickle
import sys
import random
import itertools


#Nearest neighbour - gets x number of nearest nodes
def nearest(x, y_row, neighbors, labels): #specify number of neighbours to return
    distances = np.linalg.norm(x - y_row, axis=1)#numpy array of distances
    for i in labels:
        distances = np.c_[distances,i]
    distances = distances[np.argsort(distances[:, 0])]
    neighborsList, neighborsLabels = list(), list()
    for i in range(neighbors): #27093
        neighborsList.append(distances[i][0])
        neighborsLabels.append(distances[i][1:len(distances)-1])
    return neighborsList,neighborsLabels
    
def lookUp(labels, lookup, which):
    arr = np.array(labels)
    x,y = np.shape(arr)
    indices = np.argwhere(arr[which] == lookup)
    return indices
def firstTrue(boolArr):
    for i in range(len(boolArr)):
        if boolArr[i] == True:
            return i


def isEqual(x,y):
    if x == y:
        return True
    else:
        return False

#Current and nearest are same cluster then true otherwise false
def checkClus(x,y):
    boolArr = list(map(isEqual, x, y))
    return boolArr

def consensus(x,y,labels): #form boolean array from checkClus, if majority are true then the node should be in the cluster, otherwise not
    boolArr=checkClus(x,y)
    trueCount, total,first = sum(boolArr), len(boolArr), firstTrue(boolArr)
    if (trueCount)/(total) > 0.5:
        #pass vote of node being in cluster
        if (boolArr[0] == False):
            print("did not fully pass")
            print(x)
            print(y)
            ind1 = lookUp(labels,x[first],first)
            ind2 = lookUp(labels,x[0],0)
            finalind = next((a for a in ind1 if a in ind2), None)
            xVal = labels[0][finalind]
            return True,xVal
        return True, x[0]
    else:
        print("failed!")
        #pass the false vote - node is not in cluster
        return False,0#,recluster(x,y,labels)

def comprehension(X,labels,x,itera):
    if itera > 0:
        X = np.delete(X,[0,itera-1], axis = 0)
        labels = np.delete(labels,[0,itera-1], axis = 1)
    near, tempLab = nearest(X, x, 3, labels)
    boolArr1,res1 = consensus(tempLab[0],tempLab[1],labels)
    boolArr2,res2 = consensus(tempLab[0],tempLab[2],labels)
    if boolArr1:
        return res1 #need to sort this out such that we assign a valid cluster number
    elif boolArr2: #here we check its second nearest neighbor before reclustering
        return res2
    else: #recluster somehow
        return tempLab[0][0]

    