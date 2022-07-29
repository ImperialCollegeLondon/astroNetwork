""" Look at distribution of authors per paper in astro-ph
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools
import datetime

#load data
display = True
scale = True
print("Loading data...")
md = pd.read_csv('data/metadata-all-authors.csv')
print("... done")
#category = 'astro-ph'
category = 'cond-mat'
#category = 'hep-ph'
#category = 'cs'
mdastro = md[md.primary_parent_category==category] #extract astro papers
md = None

#Extract authors per paper and year
mdastro['year']=pd.DatetimeIndex(mdastro['created']).year
num_authors = mdastro[['num_authors','year']].to_numpy()

#Distributions for whole dataset
na_unique,na_counts = np.unique(num_authors[:,0],return_counts=True)
years,years_counts = np.unique(num_authors[:,1],return_counts=True)

#Distributions by year
year1 = 2008
year2 = 2019
bin = 1
ylist = range(year1,year2+1,bin)
dist = []

for ind,year in enumerate(ylist):
    ind_year = np.where(num_authors[:,1]==year)
    na_temp = num_authors[ind_year[0],:]
    out = np.unique(na_temp[:,0],return_counts=True)
    dist.append(np.array(out).T)


if display:
    plt.figure()
    f8 = dist[0]
    f19 = dist[-1]
    if scale:
        scale8 = f8[:,1].sum()
        scale19 = f19[:,1].sum()
    else:
        scale8 = 1
        scale19 = 1
    plt.loglog(f8[:,0],f8[:,1]/scale8,'.',label='2008')
    plt.loglog(f19[:,0],f19[:,1]/scale19,'.',label='2019')
    plt.xlabel('Number of authors')
    plt.ylabel('Fraction of papers')
    plt.title(category)
    plt.grid()
    plt.legend()
    plt.show()
