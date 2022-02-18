# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:19:36 2021

@author: susan
"""

import math
import random

"""From getData"""
class Cell3D:
    def __init__(self, x, y, z, name, segment, radius):  # Constructor, coords, name, slice and radius
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.name = int(name)
        self.segment = int(segment)
        self.radius = int(radius)
        
"""From here functions are from nullModel"""
        
# Function to validate if a point at coord x,y is inside of an ellipse
# with center at h,k and minor and major diameters rx, ry
# Receives coordinates h, k, the radius rx and ry and the coordinates x, y
# Returns a boolean value, either is inside or not of the ellipse
def validPoint(h, k, rx, ry, x, y):
    rx = rx/2           # Calculates the minor radius
    ry = ry/2           # Calculates the major radius
    eq = ((x-h)**2)/(rx**2) + ((y-k)**2)/(ry**2)    # From the ellipse equation
    if eq <= 1:
        return True     # Inside the ellipse
    else:
        return False    # Out of the ellipse

# This function creates a list of Cells. total is the total amount of cells to creates
# It creates them inside of an ellipse with minor diameter of rx and mayor diameter of ry
# Also, creates the radius of each cell at random or at constant value
# Receives the number of cells to create, a boolean value to indicate random radius, and coordinates
# Returns a list of null cells, just like the one we get when reading real values
def generateCells3D(total, randRad, rx, ry,nsegment,sliceDistance):
    h = rx/2                                # Calculates the center of the ellipse, no negative
    k = ry/2                                # Calculates the center of the ellipse
    nullCells = []                          # List of null cells
    nullCells.append(Cell3D(0, 0, 0, 0, 0, 0))   # Foo cell, at nullCells[0]
    for s in range(nsegment): 
     coordZ = s*sliceDistance
     for i in range(0, total[s]):               # Iterates over the given range
        name = i *(s+1)                           # To get the name of each cell
        if randRad:                         # True if we want random radius
            radius = random.randint(125, 150)   # Random radius
        else:
            radius = 125                        # Fixed value
        coordX = 0                          # Initial foo coords at x
        coordY = 0 
                                # Initial foo coords at y
        while not validPoint(h, k, rx, ry, coordX, coordY): # Find a valid coord
            coordX = random.randint(0, rx)                      # Generates at random the coords
            coordY = random.randint(0, ry)
        newCell = Cell3D(coordX, coordY,coordZ, name, s, radius) # When valid coord, creates a new cell
        nullCells.append(newCell)                           # Append that cell to the list
    return nullCells                        # Return the cells

# This function creates a list of Cells. 
# It creates them inside of an ellipse with minor diameter of rx and mayor diameter of ry, 
# and a deepness of nSlice*sliceDistance
# Also, creates the radius of each cell at random or at constant value
# Receives the number of cells to create, a boolean value to indicate random radius, and coordinates
# Returns a list of null cells, just like the one we get when reading real values
# nSlice is the number of slices, sliceDistance is the distance between each slice
# The boolean ctrl choose a equation for the number of cells in each slice. True means that the model is control.
# False means that the model is AVP.
# Y=B0 + B1*X + B2*X^2. Interpolation with four slices. X is the slice number from rostral to caudal. 
# Y is the number of cells that will be in the sliceDistance
def generateCell3SD(randRad,rx,ry,nSlice,sliceDistance,ctrl):
    h = rx/2                                # Calculates the center of the ellipse, no negative
    k = ry/2 
    nullCells =[]
    nullCells.append(Cell3D(0,0,0,0,0,0))
    for s in range(nSlice): 
     rz=(s+1)
     if ctrl:
         c=round( 371.2 - 96.64*rz + 17.56*(rz**2))
     else:
         c=round( 195.6 + 204.6*rz - 33.75*(rz**2))
     for i in range(c):               # Iterates over the given range
        name = name = i *rz                           # To get the name of each cell
        if randRad:                         # True if we want random radius
            radius = random.randint(125, 150)   # Random radius
        else:
            radius = 125                        # Fixed value
        coordX = 0                          # Initial foo coords at x
        coordY = 0 
                                # Initial foo coords at y
        while not validPoint(h, k, rx, ry, coordX, coordY): # Find a valid coord
            coordX = random.randint(0, rx)                      # Generates at random the coords
            coordY = random.randint(0, ry)
            coordZ = random.randint((rz-1)*sliceDistance, rz*sliceDistance-1)
        newCell = Cell3D(coordX, coordY,coordZ, name, s, radius) # When valid coord, creates a new cell
        nullCells.append(newCell)                           # Append that cell to the list
    return nullCells

# This function creates a list of Cells. 
# It creates them inside of an ellipse with minor diameter of rx and mayor diameter of ry, 
# and a deepness of nSlice*sliceDistance
# Also, creates the radius of each cell at random or at constant value
# Receives the number of cells to create, a boolean value to indicate random radius, and coordinates
# Returns a list of null cells, just like the one we get when reading real values
# nSlice is the number of slices, sliceDistance is the distance between each slice
# The boolean ctrl choose a equation for the number of cells in each slice. True means that the model is control.
# False means that the model is AVP.
# Y=B0 + B1*X + B2*X^2. Interpolation with four slices. X is the bregma coordinate. 
# The coordinate is from -0.4 mm to 1 mm 
# Y is the number of cells that will be in 50 μm. SliceDistance must be at least 50 μm
# zi is the initial z and zf is the final z
def generateCell3SD(randRad,rx,ry,zi,zf,sliceDistance,ctrl):
    h = rx/2                                # Calculates the center of the ellipse, no negative
    k = ry/2 
    nullCells =[]
    nullCells.append(Cell3D(0,0,0,0,0,0))
    s=0
    while zi <= zf: 
     rz=zi/1000.0
     if ctrl:
         c=round( 503.5 - 4.644*rz - 132.7*(rz**2))
     else:
         c=round( 223.1 + 64.52*rz + 141.0*(rz**2))
     for i in range(c):               # Iterates over the given range
        name = name = i *s                           # To get the name of each cell
        if randRad:                         # True if we want random radius
            radius = random.randint(125, 150)   # Random radius
        else:
            radius = 125                        # Fixed value
        coordX = 0                          # Initial foo coords at x
        coordY = 0 
                                # Initial foo coords at y
        while not validPoint(h, k, rx, ry, coordX, coordY): # Find a valid coord
            coordX = random.randint(0, rx)                      # Generates at random the coords
            coordY = random.randint(0, ry)
            coordZ = random.randint(zi,zi+50)
        newCell = Cell3D(coordX, coordY,coordZ, name, s, radius) # When valid coord, creates a new cell
        nullCells.append(newCell)                           # Append that cell to the list
        zi=zi+50+sliceDistance
       s=s+1
    return nullCells

# Auxiliary function to calculate the minor radius of an ellipse when knowing everything else
# Receives the desired area of the resulting ellipse and the major radius
# Returns the minor radius value
def rMin(area, rMaxC):
    return area*1000000/(math.pi*rMaxC)

# Auxiliary function to calculate the major radius of an ellipse when knowing everything else
# Receives the desired area of the resulting ellipse and the minor radius
# Returns the major radius value
def rMax(area, rMinC):
    return area*1000000/(math.pi*rMinC)
