# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:44:13 2021

@author: susan
"""
import numpy as np
import random

def drawNodes(cells, ax, tags):
    
    listX = []      # List for 'x' coordinates
    listY = []      # List for 'y' coordinates
    listZ = []      # List for 'x' coordinates
    slices= []      # List for segment
    colors= []
    for cell in cells:                  # Iterate over the dict items
        if cell.name == 0:                  # Ignores the foo cell at [0]
            continue
        listX.append(cell.x)                # Adds each coordinate to respective list
        listY.append(cell.y)
        listZ.append(cell.z)
        slices.append(cell.segment)
        colors.append((cell.segment+1)/255)
  
        # Plots those coordinates with given color and label
    ax.scatter(listX, listY, listZ, marker='.',c=colors, alpha=1, edgecolor='none', label='Dorsal medial', zorder=3)
   
    if tags:    # If true then plot each node name, recommended only for small references
       for i, tag in enumerate(range(len(listX))):
              ax.annotate(tag, (listX[i], listY[i]))

# This function puts on ax each valid edge in a given binary matrix
# Receives a binary matrix, a list of cells and a matplotlib object ax
# Does not return anything but draws all the edges in ax
def drawEdges(matrix, cells, ax):
    size = matrix.shape[0]              # Calculates the number of nodes
    for i in range(1,size):               # Iterates over each node
        for j in range(i, size):            # Only iterate over one side of the symmetric matrix
            if matrix[i][j] == 1 and not i == j:      # If that connection exists not with itself
                xValues = [cells[i].x, cells[j].x]    # Extract the 'y' coordinates of every cell
                yValues = [cells[i].y, cells[j].y]    # And the 'x' coordinates too
                zValues = [cells[i].z, cells[j].z]
                ax.plot(xValues, yValues,zValues, zorder=1, color='#FF99FF')     # Plot that edge
              
# Draw with different colors each connected component
# Receives a dict of connected components, a binary matrix, a list of cells and a matplotlib ax
# Does not returns anything but prints every connected component with different colors
def drawConnectedComponents(ccomponents, matrix, cells, ax):
    size = matrix.shape[0]      # Get the number of cells
    colors = []                 # List for the different colors
    visited = np.zeros(size)    # Numpy array for visited nodes on the BFS
    queue = []                  # List to use as a queue on the BFS

    sComp = len(ccomponents)    # Get the number of connected components
    for i in range(sComp):      # For each connected component we generate a new color
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))    # Add each color to colors list
    cit = 0                     # Iterator for the colors list
    # Implementation of a BFS to find all the different connected components
    for i in range(1, sComp):           # Iterates over each connected component
        queue.append(ccomponents[i][0])     # Add the first node of the current connected component
        while len(queue) > 0:               # While we haven't finished reaching every node
            now = queue.pop(0)                  # Get a node from the queue
            if visited[now] == 0:               # If we haven't visited that node
                visited[now] = 1                    # Mark as visited
                currentCompSize = len(ccomponents[i])   # Get the number of neighbours of that node
                for j in range(0, currentCompSize):         # Iterates over every node
                    node = ccomponents[i][j]                    # Get a neighbour
                    if matrix[now][node] == 1 and visited[node] == 0:   # If is valid
                        queue.append(node)                      # Add it to the queue
                        xValues = [cells[now].x, cells[node].x] # Extract the 'y' coordinates
                        yValues = [cells[now].y, cells[node].y] # And the 'x' coordinates too
                        zValues = [cells[now].z, cells[node].z]
                        ax.plot(xValues, yValues,zValues, zorder=2, color=colors[cit])  # Plot that edge
        cit += 1 # At this point we have finished with the cc i-1, so move on to the next color

# This function marks a given list of nodes, here is marking the isolated cells with white on ax
# Receives a list with the cells to draw, the main list of cells, color to use and matplotlib ax
# Does not return anything but draws the given list of cells with the specified color
def markThisCells(toDraw, cells, color, ax):
    listX = []                  # List of X coordinates
    listY = []                  # List of Y coordinates
    listZ = []                  # List of Z coordinates
    for cell in toDraw:         # Iterates over the given list of cells
        temp = cells[cell]          # Get the info of the current cell from the main cells list
        listX.append(temp.x)        # Add it's coordinates to the corresponding list
        listY.append(temp.y)
        listZ.append(temp.z)
    if len(listX) > 0:          # If we added some cells then plot those with label
        ax.scatter(listX, listY,listZ, marker='.', c=color, alpha=1, edgecolor='none', zorder=5, label='Isolated cell')