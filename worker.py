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

from sklearn.metrics import silhouette_samples
from sklearn.metrics.cluster import contingency_matrix


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
def recluster(x,y,itera,labels,X): #Recluster based on silhouette coefficient (i.e whichever node here has a higher coefficient)
    acL = labels[0]
    acL[itera] = x
    acSilVal = silhouette_samples(X, acL)
    hdbL = labels[0]
    hdbL[itera] = y
    hdbSilVal = silhouette_samples(X, hdbL)
    if hdbSilVal[itera] > acSilVal[itera]:
        return y
    else:
        return x
def isEqual(x,y):
    if x == y:
        return True
    else:
        return False

#Current and nearest are same cluster then true otherwise false
def checkClus(x,y):#check all nodes are of the same array
    ret = list()
    for i in range(3):
        boolArr = list(map(isEqual, x, y[i]))
        ret.append(boolArr)
    return ret
    
def equalRow(boolArr, rowNum):
    for i in range(5):
        if boolArr[i][rowNum] == False:
            return False
    return True

def counting(boolArr,rowNum):
    count = 0
    indices = list()
    for x in range(3):
        if boolArr[x][rowNum] == True:
            count = count+1
        else:
            indices.append(x)
    return count,indices

def vote(a,h):
    if a < 3 and h < 3: #if majority of nodes are in another cluster
        return False
    else:
        return True

def consensus(x,y,labels,silVal,itera,acLookUpList,hdbLookUpList,X): #form boolean array from checkClus, if majority are true then the node should be in the cluster, otherwise not
    #x is the labels of our node
    #y is a 2d array where we have our k labels ac labels and our hdb labels (IN THAT ORDER) of the neighbours
    #labels is our total labels
    #silVal is our silhouette values (All silhouette values)
    #itera is the corresponding row number in the array to the 6 nodes (node A and its 5 nearest neighbours)
    #Then we have our two lookup lists where index corresponds to that algos cluster, and the value is the k means equivalent
    
    #First step - translate the lists
    klabels = [x[0],y[0][0],y[1][0],y[2][0],y[3][0],y[4][0]]
    acLabels = [acLookUpList[int(y[0][1])],acLookUpList[int(y[1][1])],acLookUpList[int(y[2][1])],acLookUpList[int(y[3][1])],acLookUpList[int(y[4][1])]]
    hdbLabels = [hdbLookUpList[int(y[0][2])],hdbLookUpList[int(y[1][2])],hdbLookUpList[int(y[2][2])],hdbLookUpList[int(y[3][2])],hdbLookUpList[int(y[4][2])]]    
    #Operating with the assumption that x is in the same cluster for each node
    #Second step - determine if majority of nodes are in the same array as that of x in the k means algorithm
    #As we have 5 neighbours anything less than 3 in the same cluster is a minority - thus we recluster here
    ac = max(set(acLabels), key=list(acLabels).count)
    hdb = max(set(hdbLabels), key=list(hdbLabels).count)
    noRecluster = (ac == hdb == klabels[0])               
    
    #Third step - if we are to recluster, determine on the cluster from ac and hdb
    if (noRecluster == False):#2 cases here
        #Case 1: ac and hdb agree on the cluster to place x in
        if (ac == hdb):
            print("replacing "+ str(x[0]) +" with "+ str(ac) + " at "+str(itera[0]))
            return noRecluster, ac #Return the agreed upon value
        #Case 2: They disagree on the cluster to place thus we recluster based on the silhouette score
        #We will calculate whichever has a higher silval at itera[0]
        elif ac == x[0] or hdb == x[0]:
            return False, x[0]
        else:
            print("Silhouete - Fail")
            return noRecluster, recluster(ac,hdb,itera[0],labels,X)                    
    #If ac and hdb cannot agree we rely on silhouette values to determine a better cluster for node x
    else: #If the most common cluster assignment of neighbours aligns with x
            return True, klabels[0]
    


def comprehension(X,labels,x,itera,silVal,acLookUpList,hdbLookUpList):
    silValed = silVal
    Xed = X
    lb = list()
    lb.append(labels[0][itera])
    lb.append(labels[1][itera])
    lb.append(labels[2][itera])
    
    labelsed = (np.reshape(np.array(labels),(-1,3))).tolist()
    labs = labels
    it = list()
    X = np.delete(X,itera, axis = 0)
    labels = np.delete(labels,itera, axis = 1)
    silValed = np.delete(silVal,itera, axis = 0)
    near, tempLab,inds = nearest(X, x, 5, labels)
    it.append(itera)
    it.extend(inds)
    print(it)
    boolArr1,res1 = consensus(lb,tempLab,labs,silVal,it,acLookUpList,hdbLookUpList,Xed)
    if boolArr1 == True:
        return int(res1) #need to sort this out such that we assign a valid cluster number
    else: #recluster somehow
        print("Failed - reclustering")
        return int(res1)



