# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:38:14 2021

@author: susan
"""
import paths
import connectedComponents as co;
import readCSV;
import matplotlib.pyplot as plt
import plots
import connectionMatrix
import cluster
import numpy as np
import cellsDistribution
import nullModel

#fileLocation='P3D.csv'  #proof file
#cells = readCSV.extractCells3D(fileLocation, 'all', False)

nullrMin = 1250     # Arbitrary size of one side
nullrMax = int(nullModel.rMax(14.0756, nullrMin))
nsli=2 #number of slices
sliDistance=50
cells= nullModel.generateCell3DA(False, nullrMin, nullrMax, nsli, sliDistance,True) #Proof with equations from extrapolation
criteria=2
criterion=0.1
slices="1 y 2"
section='all'
saveFigs=False;

#matrix = co.distanceMatrix3D(cells)    #cells must have cells from diferent slices
matrixP = connectionMatrix.probabilityMatrix3D(cells, criteria, 125)
nCells=len(cells)
matrixbin, adList = connectionMatrix.binaryMatrix3D(matrixP, criterion)
components, nodes= co.connectedComponents( matrixbin)
edgesPN = co.edgesPerNode(matrixbin)
centrality  =paths.brandeAlgorithm(adList)
localClustering = cluster.localClusteringCoef(range(0, nCells), adList, matrixbin)
nodesPCC_WOZ  = co.nodesPerCC_WOZ(components)
#print(cells.x)

ccClustering = np.empty(len(components)-1)
for i in range(0, len(components)-1):
    ccClusteringTemp    = cluster.localClusteringCoef(components[i+1], adList, matrixbin)
    ccClustering[i]     = cluster.globalClusteringCoef(ccClusteringTemp)
ccTransitivity = np.empty(len(components)-1)
for i in range(0, len(components)-1):
    ccTransitivity[i]   = cluster.transitivityCoef(components[i+1], adList,  matrixbin)


fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

plots.drawNodes(cells, ax1, True)
#plots.drawConnectedComponents(components, matrixbin, cells, ax1)
plots.drawEdges(matrixbin, cells, ax1)
plots.markThisCells(components[0], cells, '#FFFFFF', ax1) 
plt.show()

figNodes, axNodes = plt.subplots(1, 3)  # Figs for the histograms for individual nodes
binsND = int(np.amax(edgesPN))
if binsND <= 0:
    binsND = 10
axNodes[0].hist(edgesPN, bins = binsND)
axNodes[1].hist(centrality, bins=12)
axNodes[2].hist(localClustering, bins=12)

figCC, axCC = plt.subplots(1, 3)        # Figs for individual connected components
axCC[0].hist(nodesPCC_WOZ, bins=10)
axCC[1].hist(ccClustering, bins=10)
axCC[2].hist(ccTransitivity, bins=12)

# =============================================================================
# figDist, axDist = plt.subplots()        # Figs for 2D histogram of distribution
# binsX = list(range(-500, 5500, 500))
# binsY = list(range(-500, 7000, 500))
# binsZ = list(range(-500, 7000, 500))
# distCellsX = cellsDistribution.distribution1D(range(1, nCells), cells, 'x')
# distCellsY = cellsDistribution.distribution1D(range(1, nCells), cells, 'y')
# distCellsZ = cellsDistribution.distribution1D(range(1, nCells), cells, 'z')
# axDist.hist2d(distCellsX, distCellsY,distCellsZ, bins=(binsX,binsY), cmap=plt.cm.jet)
# =============================================================================

# Style and info for the network figure
fig.set_size_inches((7.15,9.1))
fig.suptitle('Connectivity model - Criteria ' + str(criteria), fontsize=20)
ax1.set_title( '01' + ' - Section ' + slices + '\n' + 'Connectivity criterion ' + str(criterion) + '  ' + 'Radius size fixed at 125um', fontsize=12)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlabel('X coordinates (um)')
ax1.set_ylabel('Y coordinates (um)')
ax1.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
ax1.legend()
ax1.set_xlim(-500, nullrMin+500)
ax1.set_ylim(-500, nullrMax+500)
figNetworkName = '01'+ '-' + slices + '-' + section + '.png'

# =============================================================================
# # Style and info for the 2D histogram
# figDist.set_size_inches((7.15,9.1))
# figDist.suptitle('Density of cells', fontsize=20)
# axDist.set_title( animal + ' - Section ' + slice + '\n', fontsize=12)
# axDist.spines['top'].set_visible(False)
# axDist.spines['right'].set_visible(False)
# axDist.set_xlabel('X coordinates (um)')
# axDist.set_ylabel('Y coordinates (um)')
# figDistName = animal + '-' + slice + '-' + section + ' - Hist2d.png'
# =============================================================================

# Style and info for the histograms of individual nodes
figNodes.set_size_inches((12, 5))
figNodes.suptitle('Histograms per node', fontsize=16)
axNodes[0].set_title('Node degree', fontsize=10)
axNodes[0].spines['top'].set_visible(False)
axNodes[0].spines['right'].set_visible(False)
axNodes[0].set_xlabel('Degree')
axNodes[0].set_ylabel('Amount of nodes')
axNodes[0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
axNodes[1].set_title('Centrality of each node', fontsize=10)
axNodes[1].spines['top'].set_visible(False)
axNodes[1].spines['right'].set_visible(False)
axNodes[1].set_xlabel('Centrality')
axNodes[1].set_ylabel('Amount of nodes')
axNodes[1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
axNodes[2].set_title('Clustering coefficient per node', fontsize=10)
axNodes[2].spines['top'].set_visible(False)
axNodes[2].spines['right'].set_visible(False)
axNodes[2].set_xlabel('Clustering coefficient')
axNodes[2].set_ylabel('Amount of nodes')
axNodes[2].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
figNodesName = '01' + '-' + slices + '-' + section + ' - Hist per nodes.png'

    
    # Style and info for the histograms of individual connected components
figCC.set_size_inches((12, 5))
figCC.suptitle('Histograms per connected component (cc)', fontsize=16)
axCC[0].set_title('Amount of nodes per cc', fontsize=10)
axCC[0].spines['top'].set_visible(False)
axCC[0].spines['right'].set_visible(False)
axCC[0].set_xlabel('Quantity')
axCC[0].set_ylabel('Amount of cc')
axCC[0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
axCC[1].set_title('Global clustering coefficient per cc', fontsize=10)
axCC[1].spines['top'].set_visible(False)
axCC[1].spines['right'].set_visible(False)
axCC[1].set_xlabel('Global clustering coefficient')
axCC[1].set_ylabel('Amount of cc')
axCC[1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
axCC[2].set_title('Transitivity per cc', fontsize=10)
axCC[2].spines['top'].set_visible(False)
axCC[2].spines['right'].set_visible(False)
axCC[2].set_xlabel('Transitivity coefficient')
axCC[2].set_ylabel('Amount of cc')
axCC[2].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
figCCName = '01' + '-' + slices + '-' + section + ' - Hist per cc.png'

# =============================================================================
# if saveFigs:    # Saves the figures if indicated
#     figNetwork.savefig(dataFolder + '/ ' + figNetworkName, format='png')
#     figDist.savefig(dataFolder + '/ ' + figDistName, format='png')
#     figNodes.savefig(dataFolder + '/ ' + figNodesName, format='png')
#     figCC.savefig(dataFolder + '/ ' + figCCName, format='png')
# 
# if showFigs:    # Shows the figures if indicated
#     plt.show()
# else:
#     plt.close('all')
# 
# =============================================================================


