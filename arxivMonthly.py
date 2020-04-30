""" Some code to fiddle with Arxiv monthly
submissions data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



Df = pd.read_csv('data/arxiv_monthly.csv')
ind_2006 = Df.index[Df.month=='2006-01'][0]
data = Df.iloc[:,1:].to_numpy()


#Monthly submissions from 2006 on
plt.figure()
plt.semilogy(data[ind_2006:,0],'.')
plt.xlabel('months from 1/2006')
plt.ylabel('Monthly submissions')
plt.title("Arxiv paper submissions")
plt.grid()


#Monthly submissions from 7/1991
plt.figure()
plt.semilogy(data[:,0],'.')
plt.xlabel('months from 7/1991')
plt.ylabel('Monthly submissions')
plt.title("Arxiv paper submissions")
plt.grid()

plt.figure()
plt.loglog(data[:,0],'.')
plt.xlabel('months from 7/1991')
plt.ylabel('Monthly submissions')
plt.title("Arxiv paper submissions")
plt.grid()
