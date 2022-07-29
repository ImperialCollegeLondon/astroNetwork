""" Clean author lists, arXiv, astro-ph
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import itertools

display = True
print("Loading data...")
md = pd.read_csv('data/metadata-all-authors.csv')
print("... done")


def clean_authors(authors):
    """Remove unwanted characters from string
    containing list of authors
    """
    chars = ['.','-','{','}','[',']','(',')','0','1','2','3','4','5','6','7','8','9']
    authors_clean = authors
    for char_remove in chars:
        authors_clean = authors_clean.replace(char_remove,'')
    return authors_clean

def clean_name(author):
    """Format input string as lastname, 1stinitial 2nd initial
    continuing on for further initials as needed
    """
    names = author.split(',')
    name_clean = names[0]
    temp = names[1].split()
    for first_names in temp:
        name_clean = name_clean + ' ' + first_names.lstrip()[0]
    return name_clean
mdastro = md[md.primary_parent_category=='astro-ph'] #extract astro papers
md = None
authors_list = mdastro.all_authors.to_list()
