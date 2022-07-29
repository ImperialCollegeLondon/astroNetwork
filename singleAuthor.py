"""Look at number of single author papers by category
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import datetime

fname='data/metadata-all-authors.csv'
minPapers = 15000
md = pd.read_csv(fname)
md['year']=pd.DatetimeIndex(md['created']).year

years = np.arange(2008,2020)

physics_cats = ['cond-mat','math_ph','astro-ph','hep-th','quant-ph','gr-qc','physics','nucl-th','hep-ph']

cats0 = list(md.primary_parent_category.unique())
cats = cats0.copy()
for category in cats0:
    lencat = len(md[md.primary_parent_category==category])
    print('category,size=',category,lencat)
    if lencat<minPapers:
        cats.remove(category)



Nc = len(cats)
Ny = years.size

numPapers = np.zeros((Ny,Nc))
allPapers = np.zeros((Ny,Nc))

for j,category in enumerate(cats):
    #pull out category data
    mdcat = md[md.primary_parent_category==category]
    #pull out single-author papers
    mdcat1 = mdcat[mdcat.num_authors==1]

    #iterate through year-by-year
    for i,year in enumerate(years):
        numPapers[i,j] = len(mdcat1[mdcat1.year==year])
        allPapers[i,j] = len(mdcat[mdcat.year==year])

totalPapers = numPapers.sum(axis=1)
fracPapers = numPapers/allPapers

plt.figure()
for j,category in enumerate(cats):
    plt.semilogy(years,fracPapers[:,j]/fracPapers[0,j],label=category)

#plt.semilogy(years,totalPapers/totalPapers[0],'k--',label='All')
plt.grid()
plt.xlabel('year')
plt.ylabel('Fraction of single author papers (relative to 2008 fraction)')
plt.legend()


#Physics only
plt.figure()
totalPhysics = np.zeros(totalPapers.size)
for j,category in enumerate(cats):
    if category in physics_cats:
        totalPhysics += numPapers[:,j]
        plt.plot(years,fracPapers[:,j]/fracPapers[0,j],label=category)
#plt.plot(years,totalPhysics/totalPhysics[0],'k--',label='All')

plt.grid()
plt.xlabel('year')
plt.ylabel('Number of single author papers (relative to 2008)')
plt.legend()
