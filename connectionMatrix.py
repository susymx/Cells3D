# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:52:51 2021

@author: susan
"""
import numpy as np;
import probabilityFuncion as pf;
# This function creates a squared matrix indicating the distances between each pair of cells
# Receives a list containing the cells objects
# Returns a numpy matrix where matrix[int(A)][int(B)] contains the distance between cell A and B
def distanceMatrix3D(cells):
    size = len(cells)                       # Get the number of cells
    matrix = np.empty((size, size))         # Create the matrix
    for i, cellA in enumerate(cells):       # Iterates over all the cells
        for j in range(i, size):                # Iterates with optimization
            cellB = cells[j]                            # Get the current cell
            distance = pf.getDistance3D(cellA, cellB)     # Calculates the distance
            matrix[cellA.name][cellB.name] = distance   # Get it into the matrix
            matrix[cellB.name][cellA.name] = distance   # Get it into the matrix
    return matrix                           # Return the matrix

#This function calculates the overlap volume between two cells
#Recives the same radius for both cells and the distance between them
#Returs the volume 
def overlapVolume(distance,radius):
    if radius*2 < distance:     # If they does not even touch
        return 0                    # returns 0
    ra=(radius**2-(distance/2)**2)**0.5 #Variable that apears more than twice in the formula
    volume=np.pi* ((4/3 * (radius**2) * ra) + 
                   ((distance**2)/6)*ra - 
                   distance*radius**2 * np.arcsin(ra/radius)  ) #Formula for volume
    return volume

def probabilityMatrix3D(cells, criteria, radius):
    size = len(cells)                                       # Get the total number of nodes on dict
    matrix = np.empty((size, size))                         # Creates the numpy matrix
    for i, cellA in enumerate(cells):                       # Iterates over each node
        for j in range(i, size):
            cellB = cells[j]                        # Get the current second cell
            distance = pf.getDistance3D(cellA, cellB) # Get the distance between cellA and cellB
            mValue = 0                              # Auxiliary var for final probability
            if criteria == 1:                       # Checks if we're dealing with criteria 1
                mValue = pf.directUnion(distance, radius)# Gets corresponding value, either 1 or 0
            elif criteria == 2:                     # Checks if we're dealing with criteria 2
                mValue = pf.probability(distance, radius)# Gets corresponding value, from 0.0 to 1.0
            else:                                   # Gets inside here if it's a different criteria
                return None                              # Error value
            matrix[cellA.name][cellB.name] = mValue   # Set that probability value on the matrix
            matrix[cellB.name][cellA.name] = mValue   # Set that probability value on the matrix
    return matrix   # Returns the final table

# Creates a binary matrix for a given probability matrix and criterion 0.0-1.0
# Receives a probability numpy matrix and a float value as a threshold, from 0.0 to 1.0
# Returns a numpy matrix and a adjacency list with the thresholded data, just 1's and 0's
def binaryMatrix3D(matrix, criterion):
    size = matrix.shape[0]              # Get the number of nodes
    binMatrix = np.empty((size, size))  # Creates a new numpy matrix
    adjList = {}                        # Dict for the adjacency list
    for i in range(size):               # Iterates over all the cells
        for j in range(i, size):            # Little optimization
            adjList[i] = adjList.get(i, []) # Get the current adj-list or creates a new one
            adjList[j] = adjList.get(j, []) # Same for node j
            if matrix[i][j] > criterion:    # If the threshold is reached
                binMatrix[i][j] = 1             # Mark with 1 the corresponding position in matrix
                binMatrix[j][i] = 1             # Mirroed matrix
                if i != j:                      # Avoid to put a node in it's own adj-list
                    adjList[i].append(j)            # Append the current node to the adj-list
                    adjList[j].append(i)            # Same for the other node
            else:                           # If the threshold is not reached
                binMatrix[i][j] = 0         # Mark with 0 the corresponding position
                binMatrix[j][i] = 0         # Mirroed. Nothing to do with adj-lists
# =============================================================================
#     size = matrix.shape[0]              # Simplified binMatrix, whitout adjacency matrix
#     binMatrix = np.zeros((size, size))
#     ind=matrix>criterion
#     binMatrix[ind]=1
# =============================================================================
    return binMatrix, adjList   