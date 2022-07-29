""" Fiddle with Andy's arXiv dataset using all authors;
modified from arxivMeta10.py
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools

display = True
print("Loading data...")
md = pd.read_csv('data/metadata-all-authors.csv')
print("... done")

mdastro = md[md.primary_parent_category=='astro-ph'] #extract astro papers
md = None

#Dump authors into dictionary and build graph based on 1st 10 authors for each paper
print("---- Building collaboration graph and author dictionary ---")
outfile = open('problem_names.txt','w')
G = nx.Graph()
authors_list = mdastro.all_authors.to_list()
dates = mdastro.created.to_list()
mdastro = None
adict = {}
iddict = {}
last_names = []
full_names = []
problem_names=[]
problem_ind = []
id=0
for i,authors in enumerate(authors_list):
    if i%1000==0: print("processed %d papers and %d authors" %(i,id))
    node_list=[]
    problem = False
    for name in authors.split(';'):
        name_clean = name.lstrip().replace('.','')
        if name_clean in adict:
            adict[name_clean][1]+=1
            node_list.append(adict[name_clean][0])
        else:
            id+=1
            adict[name_clean]=[id,1]
            node_list.append(id)
            last_names.append(name_clean.split(',')[0])
            full_names.append(name_clean)
            iddict[id]=name_clean
        if len(name_clean)<=3:
            problem = True
    if problem:
        problem_names.append(authors)
        outfile.write(authors+'\n')
        problem_ind.append(i)

    if len(node_list)>1:
        edges = itertools.combinations(node_list,2)
        G.add_edges_from(edges)

outfile.close()

#basic graph characteristics
n = G.number_of_nodes()
m = G.number_of_edges()

#c_all = nx.clustering(G)
#c_ave = np.mean(list(c_all.values()))

H = nx.degree_histogram(G)
q = np.array(nx.degree(G))

if display:
    print("Graph has %d nodes and %d edges" %(n,m))
#    print("Average clustering coefficient: %f" %(c_ave))
    print("Average number of collaborators per author: %f" %(q[:,1].mean()))
    plt.figure() #Cf. figure 1 in Newman (2001)
    plt.loglog(np.array(H)/n,'.')
    plt.xlabel('Number of collaborators')
    plt.ylabel('Fraction of authors')
    plt.grid()
    plt.show()
