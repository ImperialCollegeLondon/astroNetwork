""" Fiddle with Andy's arXiv dataset using 1st 10 authors data
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools

display = True
print("Loading data...")
md = pd.read_csv('data/metadata.csv')
print("... done")

mdastro = md[md.primary_parent_category=='astro-ph'] #extract astro papers


#Dump authors into dictionary and build graph based on 1st 10 authors for each paper
print("---- Building collaboration graph and author dictionary ---")
G = nx.Graph()
authors10 = mdastro.first_10_authors.to_list()
a10dict = {}
id=0
for i,a10 in enumerate(authors10):
    if i%1000==0: print("processed %d papers" %(i))
    node_list=[]
    for name in a10.split(';'):
        name_clean = name.lstrip()
        if name_clean in a10dict:
            a10dict[name_clean][1]+=1
            node_list.append(a10dict[name_clean][0])
        else:
            id+=1
            a10dict[name_clean]=[id,1]
            node_list.append(id)

    if len(node_list)>1:
        edges = itertools.combinations(node_list,2)
        G.add_edges_from(edges)


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
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()
