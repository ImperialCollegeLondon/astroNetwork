import json
import pandas as pd
infile = open('data/arxiv-metadata-oai-snapshot.json','r')
outfile = open('data/temp.json','w')

categories=['stat']
years = [2016,2017,2018,2019,2020]
months = [5,6,7]
#months = list(range(1,13))
delete_abstract = False

papers = 0
df = pd.DataFrame()
for count,l in enumerate(infile):
    if count%100000==0: print("count=",count)
    d = json.loads(l)
    id = d['id']
    if '/' in id:
        temp = id.split('/')
        yr = int(temp[1][:2])
        month = int(temp[1][2:4])
    else:
        yr = int(id[:2])
        month = int(id[2:4])
    if yr>21:
        yr+=1900
    else:
        yr+=2000
    if (yr in years) and (month in months):
        temp = d['categories']
        temp = temp.split()[0]
        cat = temp.split('.')[0]
        if cat in categories:
            if delete_abstract: del d['abstract']
            d['year']=yr
            d['month']=month
            d['cat1']=temp
            df=df.append(d,ignore_index=True)
infile.close()
outfile.close()
