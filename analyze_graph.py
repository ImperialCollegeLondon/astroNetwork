import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib
matplotlib.use('TKAgg')

#make plots of in- and out- degree distributions with logarithmic binning

colors = ['k', 'b', 'r']

gfname = 'sci'
years = [2011, 2015, 2019]
#years = [2019]
fig0, ax0 = plt.subplots()
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for i, year in enumerate(years):
    infile = gfname+str(year)+'g2.graphml'
    G = nx.read_graphml(infile)
    k_in = np.array(list(G.in_degree())).astype(int)
    k_in = k_in[np.argsort(k_in[:, 0]), :]
    a_in, b_in = np.unique(k_in[:, 1], return_counts=True)

    bin_max = np.log10(1.2*k_in[:, 1].max())
    bins = np.logspace(0, bin_max, 30)
    widths = bins[1:]-bins[:-1]
    hist = np.histogram(k_in[:, 1], bins=bins)
    ax1.bar(bins[:-1], hist[0], widths, color='w', edgecolor='k', align='edge')
    ax1.set_xscale('log')
    ax0.semilogy(sorted(k_in[:, 1]), '-', color=colors[i])

    k_out = np.array(list(G.out_degree())).astype(int)
    k_out = k_out[np.argsort(k_out[:, 0]), :]
    a_out, b_out = np.unique(k_out[:, 1], return_counts=True)
    bin_max = np.log10(1.2*k_out[:, 1].max())
    bins = np.logspace(0, bin_max, 30)
    widths = bins[1:]-bins[:-1]
    hist = np.histogram(sorted(k_out[:, 1]), bins=bins)
    ax2.bar(bins[:-1], hist[0], widths, color='w', edgecolor='b', align='edge')
    ax2.set_xscale('log')
    ax0.semilogy(a_out, '--', color=colors[i])

ax0.grid()
ax0.set_xlabel('$i^{th}$ largest degree')
ax0.set_ylabel('$k_i$')
