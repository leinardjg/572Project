import networkx as nx
import random
import numpy as np
from datetime import datetime
#import matplotlib.pyplot as plt
from networkx import double_edge_swap

# modified from
# https://networkx.org/documentation/stable/_modules/networkx/algorithms/swap.html#double_edge_swap

def double_edge_swap(G, nswap=1, max_tries=100, seed=None):
    
    if nswap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
        
    n = 0
    swapcount = 0
    keys, degrees = zip(*G.degree())  # keys, degree
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree
    discrete_sequence = nx.utils.discrete_sequence
    while swapcount < nswap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = discrete_sequence(2, cdistribution=cdf, seed=seed)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        
        # choose target uniformly from neighbors

        if (len(list(G[u])) - 1 < 0 or len(list(G[x])) - 1 < 0):
            continue
        
        vRand = random.randint(0, len(list(G[u])) - 1)
        yRand = random.randint(0, len(list(G[x])) - 1)
        
        v = list(G[u])[vRand]
        y = list(G[x])[yRand]
        if v == y:
            continue  # same target, skip

        if u == y or x == v:
            continue

        if (y not in G[u]) and (v not in G[x]):  # don't create parallel edges
            
            # modification
            #G.add_edge(u, x)
            #G.add_edge(v, y)
            #G.remove_edge(u, v)
            #G.remove_edge(x, y)
            
            G.add_edge(u, y)
            G.add_edge(x, v)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            
            swapcount += 1
        if n >= max_tries:
            e = (
                f"Maximum number of swap attempts ({n}) exceeded "
                f"before desired swaps achieved ({nswap})."
            )
            raise nx.NetworkXAlgorithmError(e)
        n += 1
    return G


# our graph

# EDGEFILE = "./edge_list.csv"
# G = nx.read_weighted_edgelist(EDGEFILE, delimiter="\t", create_using=nx.DiGraph)

EDGEFILE = "./forks.csv"
G = nx.read_weighted_edgelist(EDGEFILE, delimiter=", ", create_using=nx.DiGraph)

print(f"Created a graph with {len(G.nodes)} nodes and {len(G.edges)} links.")


def getLargeWCC(G):
    largest = max(nx.strongly_connected_components(G), key=len)
    #Making a sub graph of LSCC
    cc = G.subgraph(largest).copy()
    return cc

# gephi C = Average Clustering Coefficient: 0.118
C = np.mean(list(nx.clustering(G).values()))
dW = getLargeWCC(G)
d = nx.average_shortest_path_length(dW)
print("Average Clustering Coefficient: ", C)
print("Average Shortest Path Length: ", d)


# test setup
def getDES(G):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting...")

    original_degree = dict(G.degree())
    original_indegree = dict(G.in_degree())
    original_outdegree = dict(G.out_degree())

    swaps = 10 * G.number_of_edges()
    tries = 10 * swaps

    while True:
        try:
            G2 = double_edge_swap(G, nswap = swaps, max_tries=tries)
            break;
        except ValueError as e:
            continue

    swapped_degree = dict(G2.degree())
    swapped_indegree = dict(G2.in_degree())
    swapped_outdegree = dict(G2.out_degree())
    return G2

# unit tests






DP = G.copy() # the function edits the graph in place

# Let's create the ensemble.

clustering_DP = []
short_path_DP = []

for i in range(100): # 1000 is better
    # no garuntee of connectivity in this model
    getDES(DP)
    C_DP = np.mean(list(nx.clustering(DP).values()))
    c = getLargeWCC(DP)
    d_DP = nx.average_shortest_path_length(c)
    short_path_DP.append(d_DP)
    clustering_DP.append(C_DP)
    
    
print(np.mean(clustering_DP))
print(np.std(clustering_DP))

print(np.mean(short_path_DP))
print(np.std(short_path_DP))


########

# for node in G.nodes():
#     print(f"{node} -> ", end='', flush=True)
#     for neighbor in G.neighbors(node):
#         print(f"{neighbor},", end='', flush=True)
#     print("")

print(f"{len(list(nx.nodes_with_selfloops(G)))} with self loops.")

# nx.draw_spring(G, node_size=50, width = .1, with_labels = True)
# plt.show()

"""
---------- Followers network. ----------

# using weakly connected Component

Created a graph with 3010 nodes and 17401 links.
Average Clustering Coefficient RealG:  0.12110959357559899
Average Shortest Path Length RealG:  2.054917853504188



Average clustering Coefficeint DP: 0.024569473771424863
SD of clustering Coefficeint DP: 0.0010835356693730945

Average Shortest Path Length DP: 1.864397925129224
SD of Shortest Path Length DP: 0.034676311063847255

0 with self loops.

>>>>>>>>>>>>Updates Values

##  using strongly connected components ##

Average Clustering Coefficient RealG:  0.12110959357559899
Average Shortest Path Length RealG:  5.183995114548734


Average Clustering Coefficient DP: 0.024436859437042647
SD of clustering Coefficeint DP: 0.0009444124490467848

Average Shortest Path Length DP: 4.375639203727429
SD of Shortest Path Length DP: 0.04709140624658055
0 with self loops.


----------------Forks Netork Measure -----------------

Average Clustering Coefficient RealG:  0.044183339705234546
Average Shortest Path Length Real G:  5.989886464912621


Average Clustering Coefficient DP: 0.009522656076025524
Average Clustering Coefficient DP: 0.0009252774622990017
Average Shortest Path Length DP: 5.18841220828414
SD of Shortest Path Length DP: 0.1157081266346077

0 with self loops.
"""