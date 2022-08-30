"""
extract unique categories in astro 2021 data
"""

import pickle
fname = 'data/astro2021df.pickle'

df = pickle.load(open(fname, 'rb'))

L = df['categories'].unique()
catSet = set()

for l in L:
    catSet.update(l.split())
