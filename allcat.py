"""
extract unique categories in astro 2021 data
"""
import networkx as nx
import numpy as np
import pickle

fname = 'df1121.p'
years = list(range(2011, 2020))
#year = 2019
write_graphs = True
gfname = 'sci'

print("loading data...")
dfall = pickle.load(open(fname, 'rb'))
print("... done")

print("creating category sets and dict...")
L0 = dfall['cat1'].unique()
L1 = dfall['subcats'].tolist()
catfSet = set(L0)

for l in L1:
    catfSet.update(l)

#create dictionary with count of how often each category occurs along
#with label
catfDict = {}
for i, c in enumerate(catfSet):
    catfDict[c] = [i, 0]
for row in dfall.iterrows():
    cats = row[1].subcats
    for d in cats:
        catfDict[d][1] += 1
    d = row[1].cat1
    catfDict[d][1] += 1


for year in years:
    print("==== year = %d ====" % year)
    df = dfall[dfall.year == year]

    print("making graph1...")
    #Weighted graph of full categories, weights normalize based on number of subcategories per paper
    G1 = nx.DiGraph()
    for k, v in catfDict.items():
        G1.add_node(v[0], cat=k)
    for row in df.iterrows():
        cat0 = row[1].cat1
        cats = row[1].subcats
        n = len(cats)
        if n > 0:
            a = catfDict[cat0][0]
            for c in cats:
                b = catfDict[c][0]
                if (a, b) in G1.edges():
                    G1[a][b]['weight'] += 1/n
                else:
                    G1.add_edge(a, b, weight=1/n)
    print("...done")

    if write_graphs:
        outfile = gfname+str(year)+'g1.graphml'
        nx.write_graphml(G1, outfile)

    print("making graph2...")
    #MultiGraph of full categories
    G2 = nx.MultiDiGraph()
    for k, v in catfDict.items():
        G2.add_node(v[0], cat=k)
    for row in df.iterrows():
        cat0 = row[1].cat1
        cats = row[1].subcats
        if len(cats) > 0:
            a = catfDict[cat0][0]
            for c in cats:
                b = catfDict[c][0]
                G2.add_edge(a, b)
    print("...done")

    if write_graphs:
        outfile = gfname+str(year)+'g2.graphml'
        nx.write_graphml(G2, outfile)
