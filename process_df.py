import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import matplotlib
matplotlib.use('TKAgg')

fname = 'df1121.p'

print("loading data...")
df = pickle.load(open(fname, 'rb'))
print("... done")
numcats = list(df.subcat_count.value_counts().to_dict().keys())
years = df.year.unique()
allDict = {}

for year in years:
    print("processing year ", year, "...")
    dfyr = df[df.year == year]
    yrDict = {}
    yrDict['total'] = len(dfyr)
    for i in numcats:
        key = 'cat'+str(i+1)
        numcatsyr = dfyr.subcat_count.value_counts().to_dict()
        if i in numcatsyr:
            yrDict[key] = numcatsyr[i]
        else:
            yrDict[key] = 0
    allDict[year] = yrDict
    print("... done")

dfpost = pd.DataFrame(allDict).transpose()
A = dfpost.to_numpy()
plt.figure()
plt.semilogy(years, A[:, 0])
plt.xlabel('year')
plt.ylabel('total number of papers')
plt.grid()
plt.figure()
for i in numcatsyr:
    y = A[:, i+1]/A[:, 0]
    plt.plot(years, y, 'x--', label=str(i)+' subcategories')

plt.figure()
B = np.transpose(A.T/A[:, 0])
C = B[:, 1:5]
C[:, -1] = B[:, 4:].sum(axis=1)
labels = ['0 subcategories', '1', '2', '3 or more']
plt.plot(years, B[:, 1], 'x--', label='0 subcategories')
plt.plot(years, B[:, 2], 'x--', label='1')
plt.plot(years, B[:, 3], 'x--', label='2')
plt.plot(years, B[:, 4:].sum(axis=1), 'x--', label='3 or more')
plt.grid()
plt.xlabel('year')
plt.ylabel('fraction of papers')
plt.legend()

fig, ax = plt.subplots()
ax.stackplot(years, C.T, labels=labels)
ax.set_xlabel('year')
ax.set_ylabel('fraction of submitted papers')
ax.set_xlim([2011, 2019])
ax.set_ylim([0, 1])
ax.legend(loc='lower right')
