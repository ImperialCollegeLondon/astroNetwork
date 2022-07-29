""" Elementary analysis of astro-ph collaboration network
from https://snap.stanford.edu/data/ca-AstroPh.html
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

display = True

#read data and construct graph
print("reading data...")
d = np.loadtxt('data/ca-AstroPh.txt',skiprows=4)
print("... done")
G = nx.Graph()
G.add_edges_from(d)

#basic graph characteristics
n = G.number_of_nodes()
m = G.number_of_edges()

c_all = nx.clustering(G)
c_ave = np.mean(list(c_all.values()))

H = nx.degree_histogram(G)
q = np.array(nx.degree(G))

if display:
    print("Graph has %d nodes and %d edges" %(n,m))
    print("Average clustering coefficient: %f" %(c_ave))
    print("Average number of collaborators per author: %f" %(q[:,1].mean()))
    plt.figure() #Cf. figure 1 in Newman (2001)
    plt.loglog(np.array(H)/n,'.')
    plt.xlabel('Number of collaborators')
    plt.ylabel('Fraction of authors')
    plt.grid()
    plt.show()
