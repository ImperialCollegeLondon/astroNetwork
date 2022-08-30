"""Community analysis of unweighted graph using nested stochastic block model inference method
implemented in graph-tool package"""
import numpy as np
import graph_tool.all as gt
import pickle
from time import time
import os
os.environ["OMP_NUM_THREADS"] = "4"

gfname = 'sci'
years = list(range(2011, 2020))
write_all_states = True
outfname = 'sci'
reps = 2
anneal = True
entropy = [[] for i in years]
count = 0
for year in years:
    print("==== year = %d ====" % year)
    infile = gfname+str(year)+'g2.graphml'
    g = gt.load_graph(infile)
    print(g)

    t1 = time()
    #initial state computation
    stateUW = gt.minimize_nested_blockmodel_dl(g)
    print("Initial state entropy:", stateUW.entropy())
    entropy[count].append(stateUW.entropy())

    #"minimize" entropy
    if anneal:
        for i in range(reps):
            print("-----------")
            print("i=", i)
            print("-----------")
            gt.mcmc_anneal(stateUW, beta_range=(1, 10), niter=1000,
                           mcmc_equilibrate_args=dict(force_niter=10))
            print("Entropy after annealing:", stateUW.entropy())
            entropy[count].append(stateUW.entropy())

    if write_all_states:
        #outfname = 'stateW'+str(count)+'.p'
        outfile = outfname+str(year)+'stateUW.p'
        pickle.dump(stateUW, open(outfile, 'wb'))
    count += 1

    t2 = time()
    print("elaspsed time:", t2-t1)
