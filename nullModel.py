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
def generateCell3DB(randRad,rx,ry,zi,zf,sliceDistance,ctrl):
    h = rx/2                                # Calculates the center of the ellipse, no negative
    k = ry/2 
    nullCells =[]
    nullCells.append(Cell3D(0,0,0,0,0,0))
    s=1
    name=1
    while zi <= zf: 
      rz=zi/1000.0
      if ctrl:
        c=round( 503.5 - 4.644*rz - 132.7*(rz**2))
      else:
        c=round( 223.1 + 64.52*rz + 141.0*(rz**2))
      for i in range(c):               # Iterates over the given range
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
        newCell = Cell3D(coordX, coordY,coordZ, name, s-1, radius) # When valid coord, creates a new cell
        nullCells.append(newCell)                           # Append that cell to the list
        name=name+1  # To get the name of each cell
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
