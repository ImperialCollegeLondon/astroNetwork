"""
extract unique categories in astro 2021 data
"""
import networkx as nx
import numpy as np
import pickle

fname = 'data/all2021df.pickle'

print("loading data...")
df = pickle.load(open(fname, 'rb'))
print("... done")

print("creating category sets and dict...")
L = df['categories'].unique()
cat0Set = set()
catfSet = set()

for l in L:
    catfSet.update(l.split())

#create dictionary with count of how often each category occurs along
#with label
catfDict = {}
for i, c in enumerate(catfSet):
    catfDict[c] = [i, 0]
for row in df.iterrows():
    cats = row[1].categories.split()
    for c in cats:
        catfDict[c][1] += 1


for c in catfSet:
    name = c.split('.')[0]
    cat0Set.add(name)


#Create dictionary cat:label
cat0Dict = {}
for i, c in enumerate(cat0Set):
    cat0Dict[c] = i
print("...done")


#Create co-occurrence Graph
#Iterate through abstracts
#for each abstract, extract distinct super-categories
#if there is more than one, check if edge is in graph
#if it is, increment edge weight
#otherwise add edge with weight=1

#Graph of primary category only
print("making graph1...")
G1 = nx.Graph()
for row in df.iterrows():
    cats = row[1].categories.split()
    s = set()
    for c in cats:
        s.add(c.split('.')[0])
    n = len(s)
    s = list(s)
    if n > 0:
        for i in range(n-1):
            a = cat0Dict[s[i]]
            for j in range(i+1, n):
                b = cat0Dict[s[j]]
                if (a, b) in G1.edges():
                    G1[a][b]['weight'] += 1
                else:
                    G1.add_edge(a, b, weight=1)
print("...done")

print("making graph2...")
#Weighted graph of full categories, weights normalize based on number of subcategories per paper
G2 = nx.DiGraph()
for k, v in catfDict.items():
    G2.add_node(v[0], cat=k)
for row in df.iterrows():
    cats = row[1].categories.split()
    n = len(cats)-1
    if n > 0:
        a = catfDict[cats[0]][0]
        for c in cats[1:]:
            b = catfDict[c][0]
            if (a, b) in G2.edges():
                G2[a][b]['weight'] += 1/n
            else:
                G2.add_edge(a, b, weight=1/n)
print("...done")

print("making graph3...")
#MultiGraph of full categories
G3 = nx.MultiDiGraph()
for k, v in catfDict.items():
    G3.add_node(v[0], cat=k)
for row in df.iterrows():
    cats = row[1].categories.split()
    if len(cats) > 1:
        a = catfDict[cats[0]][0]
        for c in cats[1:]:
            b = catfDict[c][0]
            G3.add_edge(a, b)
print("...done")


print("making graph4...")
#Undirected graph of full categories
G4 = nx.MultiGraph()
for row in df.iterrows():
    cats = row[1].categories.split()
    n = len(cats)
    if n > 1:
        for i in range(n-1):
            a = catfDict[cats[i]][0]
            for j in range(i+1, n):
                b = catfDict[cats[j]][0]
                G4.add_edge(a, b)
print("...done")


#analyze graph
G = G2
k_in = np.array(list(G.in_degree(weight='weight')))
k_in = k_in[np.argsort(k_in[:, 0]), :]
a_in, b_in = np.unique(k_in[:, 1], return_counts=True)

k_out = np.array(list(G.out_degree(weight='weight')))
k_out = k_out[np.argsort(k_out[:, 0]), :]
a_out, b_out = np.unique(k_out[:, 1], return_counts=True)
