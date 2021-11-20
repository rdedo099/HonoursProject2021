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
    maxList = list()
    for i in range(len(itera)):
        maxList.append(silVal[int(itera[i])])
    max_value = max(maxList)
    max_index = maxList.index(max_value)
    if max_index == 0:
        return x
    else:
        return y[max_index-1][0]         
def isEqual(x,y):
    if x == y:
        return True
    else:
        return False

#Current and nearest are same cluster then true otherwise false
def checkClus(x,y):#check all nodes are of the same array
    ret = list()
    for i in range(5):
        boolArr = list(map(isEqual, x, y[i]))
        ret.append(boolArr)
    return ret
    
def equalRow(boolArr, rowNum):
    for i in range(5):
        if boolArr[i][rowNum] == False:
            return False
    return True     

def consensus(x,y,labels,silVal,itera,silVal1): #form boolean array from checkClus, if majority are true then the node should be in the cluster, otherwise not
    boolArr=checkClus(x,y)#change to accept y as array
    #trueCount, total,first = sum(boolArr), len(boolArr), firstTrue(boolArr)
    if equalRow(boolArr, 0) == True:
        return True, x[0]
    for i in range(1,5):
        if equalRow(boolArr, i): #when consensus is passed but what our clustering is based on does not agree
            print("did not fully pass")
            loca = list()
            ind1 = lookUp(labels,x[i],i)#val to check with
            ind2 = lookUp(labels,x[0],0)#or if the current nodes value is better
            ind3, ind4, ind5, ind6, ind7 = lookUp(labels,y[0][0],0), lookUp(labels,y[1][0],0), lookUp(labels,y[2][0],0), lookUp(labels,y[3][0],0), lookUp(labels,y[4][0],0)
            firstValList = np.intersect1d(ind1, ind2, assume_unique=False, return_indices=False)
            secondValList = np.intersect1d(ind1, ind3, assume_unique=False, return_indices=False)
            thirdValList = np.intersect1d(ind1, ind4, assume_unique=False, return_indices=False)
            fourthValList = np.intersect1d(ind1, ind5, assume_unique=False, return_indices=False)
            fifthValList = np.intersect1d(ind1, ind6, assume_unique=False, return_indices=False)
            sixthValList = np.intersect1d(ind1, ind7, assume_unique=False, return_indices=False)
            x1, x2, x3, x4, x5, x6 = np.shape(firstValList), np.shape(secondValList), np.shape(thirdValList), np.shape(fourthValList), np.shape(fifthValList), np.shape(sixthValList)
            loca.extend([x1,x2,x3,x4,x5,x6])
            max_value = max(loca)
            max_index = loca.index(max_value)
            if max_index == 0: #determine which node classification is agreed on more
                print("replacing "+ str(x[0]) +" with "+ str(x[0]) + " at "+str(itera))
                return True, x[0]
            else:
                print("replacing "+ str(x[0]) +" with "+ str(y[max_index -1][0])+ " at "+str(itera))
                return True, y[max_index -1][0]
    else:
        print("failed!")
        
        #pass the false vote - node is not in cluster
        return False, recluster(x[0],y,silVal1,itera)

def comprehension(X,labels,x,itera,silVal):
    silValed = silVal
    lb = list()
    lb.append(labels[0][itera])
    lb.append(labels[1][itera])
    lb.append(labels[2][itera])
    lb.append(labels[3][itera])
    lb.append(labels[4][itera])
    labelsed = (np.reshape(np.array(labels),(-1,5))).tolist()
    labs = labels
    it = list()
    #if itera > 5:
        #X = np.delete(X,slice(0,itera-5), axis = 0)
        #labels = np.delete(labels,slice(0,itera-5), axis = 1)
        #silValed = np.delete(silVal,slice(0,itera-5), axis = 0)
    near, tempLab,inds = nearest(X, x, 6, labels)
    it.append(itera)
    it.extend(inds[1:6])
    boolArr1,res1 = consensus(lb,tempLab[1:6],labs,silValed,it,silVal)
    if boolArr1 == True:
        return int(res1) #need to sort this out such that we assign a valid cluster number
    else: #recluster somehow
        print("Failed - reclustering")
        return int(res1)

    

    

    

    

    

    

    

    
    

    
    