# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:55:24 2021

@author: susan
"""
import math
import numpy as np 

# Corresponding to the first criteria
# Receives two parameters, distance between cells and the radius (same for both)
# Binary function, returns either 1 or 0
def directUnion(distance, radius):
    # Checks if the dendritic fields may touch each other
    isTouching = distance < 2*radius
    if isTouching:
        return 1    # If they are, the function returns 1
    else:
        return 0    # If not, the function returns 0

# This function calculates the distance between two cells using Pythagoras theorem
# Receives two cell objects
# Returns the euclidean distance between the given cells
def getDistance3D(cellA, cellB):
    dx = abs(cellA.x - cellB.x)                 # Distance on x
    dy = abs(cellA.y - cellB.y)                 # Distance on y
    dz = abs(cellA.z - cellB.z)                 # Distance on z
    distance = math.sqrt((dx**2) + (dy**2) + (dz**2))     # Calculates final distance using Pythagoras theorem
    return distance              # Returns that

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

# Calculates the proportion of overlap when considering same radius
# Receives the distance and radius of the cells
# Returns the proportion of overlap over the maximum possible overlap
def proportion(distance, radius):
    return overlapVolume(distance, radius)/overlapVolume(0, radius)

# Sigmoid function, not in use but keeping it here just in case...
def sigmoid(x):
    return 1/(1+math.exp(-x))

# The initial proposal probability of connection between two cells at distance d and same radius
# DISCLAIMER: deprecated but keeping it here just for historical reasons
def probability_deprec(distance, radius):
    if distance > 2*radius:     # If their dendritic fields would never touch
        return 0                    # arbitrary probability of 0
    if distance <= radius:      # If they touch beyond somas
        return 1                    # arbitrary probability of 1
    # On every other case, we return an adjusted probability
    return sigmoid(proportion(distance, radius)) + (1 - sigmoid(proportion(radius, radius)))

# The actual probability of connection between two cells of same radius
# Receives the distance between the two cells and the radius (same for both)
# Returns the probability of connection
def probability(distance, radius):
    distance = abs(distance)        # Working only with positive values
    radius = abs(radius)            # Working only with positive values
    if radius == 0:                 # If the radius is 0 then we return 0
        return 0
    return overlapVolume(distance, radius)/overlapVolume(0, radius)     # The probability is the proportion
