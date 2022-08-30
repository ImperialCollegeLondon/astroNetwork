"""Community analysis of graph using nested stochastic block model inference method
implemented in graph-tool package"""
import numpy as np
#import networkx as nx
import graph_tool.all as gt
import pickle
from time import time
import os

os.environ["OMP_NUM_THREADS"] = "2"
gfname = 'sci'
years = list(range(2017, 2020))
ed = 'real-exponential'
offset = 1
reps = 2
anneal = True
write_all_states = True
outfname = 'sci'
#load graph
entropy = [[] for i in years]
count = 0
for year in years:
    print("==== year = %d ====" % year)
    infile = gfname+str(year)+'g1.graphml'
    g = gt.load_graph(infile)
    print(g)

    t1 = time()

    #initial state computation
    stateW = gt.minimize_nested_blockmodel_dl(
        g, state_args=dict(recs=[g.ep.weight], rec_types=[ed]))
    print("Initial state entropy:", stateW.entropy())
    entropy[count].append(stateW.entropy())
    #"minimize" entropy
    if anneal:
        for i in range(reps):
            print("-----------")
            print("i=", i)
            print("-----------")
            gt.mcmc_anneal(stateW, beta_range=(1, 10), niter=1000,
                           mcmc_equilibrate_args=dict(force_niter=10))
            print("Entropy after annealing:", stateW.entropy())
            entropy[count].append(stateW.entropy())

    #compute number of communities
    stateW.print_summary()
    level = stateW.get_levels()[0]
    b = level.get_blocks()
    u, v = np.unique(list(b), return_counts=True)
    print("number of communities:", len(u))
    print("community node counts:", v)

    t2 = time()
    print("elaspsed time:", t2-t1)

    if write_all_states:
        #outfname = 'stateW'+str(count)+'.p'
        outfile = outfname+str(year)+ed+'stateW.p'
        pickle.dump(stateW, open(outfile, 'wb'))
    count += 1
