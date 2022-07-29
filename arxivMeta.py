""" Fiddle with Andy's arXiv dataset using all authors;
modified from arxivMeta10.py
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools


def load_astro(fname='data/metadata-all-authors.csv'):
    """load astro-ph metadata into Pandas dataframe
    """
    print("Loading data...")
    md = pd.read_csv(fname)
    print("... done")
    mdastro = md[md.primary_parent_category=='astro-ph'] #extract astro papers
    md = None
    return mdastro

def clean_authors(authors):
    """Remove unwanted characters from string
    containing list of authors
    """
    chars = ['.','-',':','{','}','[',']','(',')','0','1','2','3','4','5','6','7','8','9']
    authors_clean = authors
    for char_remove in chars:
        authors_clean = authors_clean.replace(char_remove,'')
    return authors_clean

def clean_name(author):
    """Format input string as lastname, 1st initial 2nd initial
    continuing on for further initials as needed
    """
    names = author.split(',')
    name_clean = names[0].lstrip()
    if len(names)>1:
        if not names[1].isspace():
            temp = names[1].split()
            for first_names in temp:
                name_clean = name_clean + ' ' + first_names.lstrip()[0]
    return name_clean

display = True
mdastro = load_astro()

#Dump authors into dictionary and build graph based on 1st 10 authors for each paper
print("---- Building collaboration graph and author dictionary ---")
#outfile = open('problem_names.txt','w')
G = nx.Graph()
authors_list = mdastro.all_authors.to_list()
num_authors = mdastro['num_authors'].to_numpy()

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
    if num_authors[i]<=np.inf:
        node_list=[]
        problem = False
        authors_clean = clean_authors(authors)
        for name in authors_clean.split(';')[:]:
            if not name.isspace():
                name_clean = clean_name(name)
                if not name_clean.isspace():
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
            #outfile.write(authors+'\n')
            problem_ind.append(i)

        if len(node_list)>1:
            edges = list(itertools.combinations(node_list,2))
            for e in edges:
                if G.has_edge(e[0],e[1]):
                    G[e[0]][e[1]]['weight']+=1
                else:
                    G.add_edge(e[0],e[1],weight=1)
#outfile.close()

#basic graph characteristics
n = G.number_of_nodes()
m = G.number_of_edges()

#c_all = nx.clustering(G)
#c_ave = np.mean(list(c_all.values()))

H = nx.degree_histogram(G)
q = np.array(nx.degree(G))
ind = np.arange(len(H))

if display:
    print("Graph has %d nodes and %d edges" %(n,m))
#    print("Average clustering coefficient: %f" %(c_ave))
    print("Average number of collaborators per author: %f" %(q[:,1].mean()))
    plt.figure() #Cf. figure 1 in Newman (2001)
    plt.loglog(ind,np.array(H)/n,'.',markersize=2)
    plt.xlabel('Number of collaborators')
    plt.ylabel('Fraction of authors')
    plt.grid()
    plt.show()
