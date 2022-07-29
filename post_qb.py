import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools


print("Loading data...")
fname = 'data/qbio-test.json'
qb = pd.read_json(fname,lines=True)
print("...done")

def clean_authors_list(L):
    cleanList = []
    for l in L: #l is list of authors on a paper
        names = []
        for name in l: #name is one author in l
            clean_name = []
            for parts in name:
                if parts=='':
                    break
                else:
                    if ' ' in parts:
                        parts_list = parts.split()
                        clean_name.extend(parts_list)
                    else:
                        clean_name.append(parts)
            if len(clean_name)<2:
                print("Warning, name has 1 or less parts: ",l)
            else: names.append(clean_name)
        cleanList.append(names)
    return cleanList
#extract ids in array
#creat dictionary with key: value = month.year: count


print("extracting peak papers...")
paperid_list = qb.id.to_list()
dateid_list = []
year_list = []
paperid_dict = {}
for s in paperid_list:
    id = s.replace('q-bio/','')[:4]
    if id=='0309': print(s)
    if id in paperid_dict:
        paperid_dict[id]+=1
    else:
        paperid_dict[id]=1
    dateid_list.append(id)
    year_list.append(2000+int(id[:2]))
qb['dateid']=dateid_list
qb['year']=year_list
keys = np.array(list(paperid_dict.keys()),dtype=int)
values = np.array(list(paperid_dict.values()))
qbpeak = qb[qb.dateid=='2004']
qbexpeak = qb[qb.dateid!='2004']
print("...done")


print("Extracting peak authors...")
adict = {}
iddict = {}
last_names = []
full_names = []
problem_names=[]
problem_ind = []
authors_list = qbpeak.authors_parsed.to_list()
authorsClean = clean_authors_list(authors_list)
authorsCleanFlat = [item for sublist in authorsClean for item in sublist]
authorsp = []
for a in authorsCleanFlat:
    if a not in authorsp: authorsp.append(a)
authorsp.sort()
print("...done")

print("Extractin ex-peak authors...")
authors_list_ex_peak = qbexpeak.authors_parsed.to_list()
authorsClean_ex_peak = clean_authors_list(authors_list_ex_peak)
authorsCleanFlat_ex_peak = [item for sublist in authorsClean_ex_peak for item in sublist]
authorsexp = []
for a in authorsCleanFlat_ex_peak:
    if a not in authorsexp: authorsexp.append(a)
authorsexp.sort()

authorsexp_last = []
for a in authorsexp:
    authorsexp_last.append(a[0])
print("...done")

# unique_authors_dict = {}
# for ind,author in enumerate(authors_list_ex_peak):
#     name = author[0]
#     #name = ''.join(author)
#     if name in unique_authors_dict:
#         unique_authors_dict[name]+=1
#     else:
#         unique_authors_dict[name]={ind:1}

print("Find exact matches...")
matches = []
exact_matches = []
for name in authorsp:
    if name in authorsexp:
        exact_matches.append(name)
    # elif name[0] in authorsexp_last:
    #     matches.append([name])

print("...done")
