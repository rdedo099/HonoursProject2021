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

def isEqual(x,y):
    if x == y:
        return True
    else:
        return False

#Current and nearest are same cluster then true otherwise false
def checkClus(x,y):
    boolArr = list(map(isEqual, x, y))
    return boolArr

def consensus(boolArr): #form boolean array from checkClus, if majority are true then the node should be in the cluster, otherwise not
    trueCount, total = sum(boolArr), len(boolArr)
    if (trueCount)/(total) > 0.5:
        #pass vote of node being in cluster
        return True
    else:
        #pass the false vote - node is not in cluster
        return False

def comprehension(X,labels,x):
    print(x)
    near, tempLab = nearest(X, x, 3, labels)
    boolArr1 = checkClus(tempLab[0],tempLab[1])
    boolArr2 = checkClus(tempLab[0],tempLab[2])
    if consensus(boolArr1):
        return tempLab[0][0] #need to sort this out such that we assign a valid cluster number
    elif consensus(boolArr2): #here we check its second nearest neighbor before reclustering
        return tempLab[1][0]
    else: #recluster somehow
        return tempLab[0][0]

    