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
    size, y = np.shape(x)
    itera = np.arange(0,size).reshape(-1,1)
    for i in range(len(labels)):
        distances = np.c_[distances,labels[i]]
    distances = np.c_[distances,itera]
    distances = distances[np.argsort(distances[:, 0])]
    neighborsList, neighborsLabels, iteraList = list(), list(), list()
    for i in range(neighbors): #27093
        neighborsList.append(distances[i][0])
        neighborsLabels.append(distances[i][1:len(distances[i])-1])
        iteraList.append(distances[i][len(distances[i])-1])
    return neighborsList,neighborsLabels,iteraList
    
def lookUp(labels, lookup, which):
    arr = np.array(labels)
    x,y = np.shape(arr)
    indices = np.argwhere(arr[which] == lookup)
    return indices
def firstTrue(boolArr):
    for i in range(len(boolArr)):
        if boolArr[i] == True:
            return i
def recluster(x,y,silVal, itera): #Recluster based on silhouette coefficient (i.e whichever node here has a higher coefficient)
    print(itera)
    if silVal[int(itera[0])] > silVal[int(itera[1])]:
        return x
    else:
        return y          
def isEqual(x,y):
    if x == y:
        return True
    else:
        return False

#Current and nearest are same cluster then true otherwise false
def checkClus(x,y):
    boolArr = list(map(isEqual, x, y))
    return boolArr

def consensus(x,y,labels,silVal,itera,silVal1): #form boolean array from checkClus, if majority are true then the node should be in the cluster, otherwise not
    boolArr=checkClus(x,y)
    trueCount, total,first = sum(boolArr), len(boolArr), firstTrue(boolArr)
    if (trueCount)/(total) > 0.5:
        #pass vote of node being in cluster
        if (boolArr[0] == False): #when consensus is passed but what our clustering is based on does not agree
            print("did not fully pass")
            ind1 = lookUp(labels,x[first],first)#need to sort this out such that we determine if the nearest nodes value is better
            ind2 = lookUp(labels,x[0],0)#or if the current nodes value is better
            ind3 = lookUp(labels,y[0],0)
            firstValList = np.intersect1d(ind1, ind2, assume_unique=False, return_indices=False)
            x1 = np.shape(firstValList)
            secondValList = np.intersect1d(ind1, ind3, assume_unique=False, return_indices=False)
            x2 = np.shape(secondValList)
            if x1 > x2: #determine which node classification is agreed on more
                print("replacing "+ str(x[0]) +" with "+ str(x[0]) + " at "+str(itera))
                return True, x[0]
            else:
                print("replacing "+ str(x[0]) +" with "+ str(y[0])+ " at "+str(itera))
                return True, y[0]
            #return True, recluster(x[0],y[0],silVal1,itera)
        return True, x[0]
    else:
        print("failed!")
        
        #pass the false vote - node is not in cluster
        return False, recluster(x[0],y[0],silVal1,itera)

def comprehension(X,labels,x,itera,silVal):
    silValed = silVal
    lb = list()
    lb.append(labels[0][itera])
    lb.append(labels[1][itera])
    lb.append(labels[2][itera])
    labelsed = (np.reshape(np.array(labels),(-1,3))).tolist()
    labs = labels
    it = list()
    if itera > 0:
        X = np.delete(X,[0,itera-1], axis = 0)
        labels = np.delete(labels,[0,itera-1], axis = 1)
        silValed = np.delete(silVal,[0,itera-1], axis = 0)
    near, tempLab,inds = nearest(X, x, 2, labels)
    it.append(itera)
    it.append(inds[1])
    boolArr1,res1 = consensus(lb,tempLab[1],labs,silValed,it,silVal)
    if boolArr1 == True:
        return int(res1) #need to sort this out such that we assign a valid cluster number
    else: #recluster somehow
        print("Failed - reclustering")
        return int(res1)

    

    

    

    

    
    

    
    