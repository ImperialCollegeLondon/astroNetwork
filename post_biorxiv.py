import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools


bdf = pd.read_csv('data/biorxiv_monthly.csv')
bdf.columns = ['date','new','cum new','revised','cum revised','new+revised','cum new+revised']
