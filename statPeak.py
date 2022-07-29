import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


years = df.year.unique()
N = years.size
cats = df.cat1.unique()
Ncats = cats.size
cats_count = np.zeros((N,Ncats))

ML = np.zeros(N)
ME = np.zeros(N)
All = np.zeros(N)



for ind,year in enumerate(years):
    temp = df[df.year==year]
    All[ind] = temp.shape[0]
    for j,cat in enumerate(cats):
        if any(temp.cat1==cat):
            cats_count[ind,j] += temp[temp['cat1']==cat].shape[0]

    ML[ind] = temp[temp['cat1']=='stat.ML'].shape[0]
    ME[ind] = temp[temp['cat1']=='stat.ME'].shape[0]


plt.figure()
plt.plot(years.astype(int),All,'x--',label='stat (all)')
plt.plot(years.astype(int),ML,'.--',label='stat.ML')
plt.plot(years.astype(int),ME,'+--',label='stat.ME')
plt.plot(years.astype(int),cats_count[:,1],'^--',label='stat.AP')
plt.grid()
plt.xlabel('Year')
plt.ylabel('Papers submitted May-July')
plt.legend()


terms=['Covid','covid','COVID','coronavirus','Coronavirus',
 'SARS','sars','Sars','epidemic','pandemic','Epidemic',
 'Pandemic','infectious','lockdown','Lockdown']


df20 = df[df.year==2020]
count = 0
cat_dict = {}
for index,row in df20.iterrows():
    data = row['title']+' '+row['abstract']
    for t in terms:
        if t in data:
            if row.cat1 in cat_dict:
                cat_dict[row.cat1]+=1
            else:
                cat_dict[row.cat1]=1
            count+=1
            break
