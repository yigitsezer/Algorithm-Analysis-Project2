from collections import defaultdict
from heapq import *
import networkx as nx
import matplotlib.pyplot as plt
import random
import timeit

NODE_COUNT = 100
EDGE_PROBABILITY = 0.2

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen, mins = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path += (v1,)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None

# initialize the graph
n = NODE_COUNT
p = EDGE_PROBABILITY
G = nx.gnp_random_graph(n, p, directed=True)
edgelist = []

# gives all nodes weights
for i in G.edges:
    G[i[0]][i[1]]["weight"] = 1 + random.randint(0, 20)
    edgelist.append((i[0], i[1], G[i[0]][i[1]]["weight"]))

print(edgelist)

# initial graph
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='blue', with_labels=False, node_size=250)


# select two random nodes as long as they
# can be connected, use dijkstra on them
nodes = list(G.nodes)
print("searching...")
s = random.choice(nodes)
e = random.choice(nodes)
dijkstra_out = dijkstra(edgelist, s, e)
while (dijkstra_out[1] == None):
    s = random.choice(nodes)
    e = random.choice(nodes)
    dijkstra_out = dijkstra(edgelist, s, e)
    print(s, e)
print("search done")

print("For", NODE_COUNT, "number of nodes, time elapsed (in seconds):", timeit.timeit("dijkstra(edgelist, s, e)", setup="from __main__ import dijkstra, edgelist, s, e", number=100))

# path nodes refer to nodes on the shortest path
path_nodes = dijkstra_out[1]
print(dijkstra_out)

# edges on the shortest path
path_edges = list(zip(path_nodes, path_nodes[1:]))
print(path_nodes)

# highlight shortest path
nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='r', node_size=250)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r')

plt.show()
