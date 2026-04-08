import math

import networkx as nx
import random
import matplotlib.pyplot as plt


def random_3_regular_graph(n):
    if n < 4 or (3 * n) % 2 != 0:
        raise ValueError("No 3-regular graph exists for this n")
    return nx.random_regular_graph(3, n)


def satisfying_partition(G, max_attempts=100):
    nodes = list(G.nodes())
    n = len(nodes)
    
    for attempt in range(max_attempts):
        random.shuffle(nodes)
        A = set(nodes[:n//2])
        B = set(nodes[n//2:])
        
        improved = True
        while improved:
            improved = False
            for v in list(G.nodes()):
                if v in A:
                    d_int = sum(1 for u in G.neighbors(v) if u in A)
                    d_ext = sum(1 for u in G.neighbors(v) if u in B)
                    if d_ext > d_int and len(A) > 1:
                        A.remove(v)
                        B.add(v)
                        improved = True
                        break
                else:
                    d_int = sum(1 for u in G.neighbors(v) if u in B)
                    d_ext = sum(1 for u in G.neighbors(v) if u in A)
                    if d_ext > d_int and len(B) > 1:
                        B.remove(v)
                        A.add(v)
                        improved = True
                        break
        
        if is_satisfying(G, A, B):
            return A, B
    
    return A, B


def find_cycle(G):
    visited = set()
    parent = {}

    def dfs(v, p):
        visited.add(v)
        for u in G.neighbors(v):
            if u == p:
                continue
            if u in visited:
                # reconstruct cycle
                cycle = [u, v]
                cur = v
                while cur != u:
                    cur = parent[cur]
                    cycle.append(cur)
                return cycle
            parent[u] = v
            res = dfs(u, v)
            if res:
                return res
        return None

    for start in G.nodes():
        if start not in visited:
            parent[start] = None
            cycle = dfs(start, None)
            if cycle:
                return list(set(cycle))  # remove duplicates

    return None


def find_two_disjoint_cycles(G):
    C1 = shortest_cycle(G)
    if not C1:
        return None, None
    
    G_prime = G.copy()
    G_prime.remove_nodes_from(C1)

    C2 = find_cycle(G_prime)
    return C1, C2


def is_exception(G):
    return nx.is_isomorphic(G, nx.complete_graph(4)) or \
        nx.is_isomorphic(G, nx.complete_bipartite_graph(3, 3))


def satisfying_partition_from_cycles(G, C1, C2):
    A = set(C1)
    B = set(G.nodes()) - A

    locked = set(C1) | set(C2)

    improved = True
    while improved:
        improved = False
        
        for v in G.nodes():
            if v in locked:
                continue

            if v in A:
                d_int = sum(1 for u in G.neighbors(v) if u in A)
                d_ext = sum(1 for u in G.neighbors(v) if u in B)
                
                if d_ext >= 2:  # since 3-regular
                    A.remove(v)
                    B.add(v)
                    improved = True
                    break
            else:
                d_int = sum(1 for u in G.neighbors(v) if u in B)
                d_ext = sum(1 for u in G.neighbors(v) if u in A)
                
                if d_ext >= 2:
                    B.remove(v)
                    A.add(v)
                    improved = True
                    break

    return A, B


def satisfying_partition_3_regular(G):
    if is_exception(G):
        return None  # no solution

    C1, C2 = find_two_disjoint_cycles(G)

    if not C1 or not C2:
        raise ValueError("Theoretical guarantee failed (should not happen)")

    return satisfying_partition_from_cycles(G, C1, C2)


def shortest_cycle(G):
    import collections
    
    best_cycle = None
    best_length = float('inf')

    for start in G.nodes():
        dist = {start: 0}
        parent = {start: None}
        queue = collections.deque([start])

        while queue:
            v = queue.popleft()
            for u in G.neighbors(v):
                if u not in dist:
                    dist[u] = dist[v] + 1
                    parent[u] = v
                    queue.append(u)
                elif parent[v] != u:
                    # Found a cycle
                    cycle_length = dist[v] + dist[u] + 1
                    
                    if cycle_length < best_length:
                        # reconstruct cycle
                        path_v = []
                        x = v
                        while x is not None:
                            path_v.append(x)
                            x = parent[x]

                        path_u = []
                        x = u
                        while x is not None:
                            path_u.append(x)
                            x = parent[x]

                        # find LCA
                        set_v = set(path_v)
                        lca = next(x for x in path_u if x in set_v)

                        cycle = []
                        x = v
                        while x != lca:
                            cycle.append(x)
                            x = parent[x]
                        cycle.append(lca)

                        tmp = []
                        x = u
                        while x != lca:
                            tmp.append(x)
                            x = parent[x]

                        cycle.extend(reversed(tmp))

                        best_cycle = cycle
                        best_length = cycle_length

    return best_cycle
# ^ O(n * (n + m)) au pire, O(n^2) pour les 3-reguliers, c'est long...

def is_satisfying(G, A, B):
    if not A or not B:
        return False
    for v in G.nodes():
        if v in A:
            d_int = sum(1 for u in G.neighbors(v) if u in A)
            d_ext = sum(1 for u in G.neighbors(v) if u in B)
        else:
            d_int = sum(1 for u in G.neighbors(v) if u in B)
            d_ext = sum(1 for u in G.neighbors(v) if u in A)
        
        if d_int < d_ext:
            return False
    return True


def plot_comparison(G, A, B, pos, ax, title="", node_size=600, font_size=12):
    color_map = ["skyblue" if v in A else "salmon" for v in G.nodes()]
    
    edge_colors = []
    for u, v in G.edges():
        if (u in A and v in A) or (u in B and v in B):
            edge_colors.append("green")
        else:
            edge_colors.append("red")
    
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=color_map,
        edge_color=edge_colors,
        node_size=node_size,
        font_size=font_size,
        width=2
    )
    
    ax.set_title(title)


def plot_single(G, A, B, pos=None, title="", node_size=600, font_size=12):
    if pos is None:
        pos = nx.spring_layout(G)

    color_map = ["skyblue" if v in A else "salmon" for v in G.nodes()]
    
    edge_colors = []
    for u, v in G.edges():
        if (u in A and v in A) or (u in B and v in B):
            edge_colors.append("green")
        else:
            edge_colors.append("red")
    
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=color_map,
        edge_color=edge_colors,
        node_size=node_size,
        font_size=font_size,
        width=2
    )
    
    plt.title(title)


def save_graph(G, filename="graphs.txt"):
    with open(filename, "a") as f:
        edges = list(G.edges())
        f.write(repr(edges) + "\n")


def load_graph(line_number, filename="graphs.txt"):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    edges = eval(lines[line_number].strip())
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def exhaustive_search_partition(G):
    # fix a node in A then try all partitions of the rest to ensure we don't miss the solution
    nodes = list(G.nodes())
    n = len(nodes)
    A = {nodes[0]}
    B = set(nodes[1:])
    for i in range(1, 2**(n-1)):
        A = {nodes[0]} | {nodes[j] for j in range(1, n) if (i & (1 << (j-1))) > 0}
        B = set(nodes) - A
        if is_satisfying(G, A, B):
            return A, B
    return None, None


def all_satisfying_partitions(G):
    nodes = list(G.nodes())
    n = len(nodes)
    if n % 2 != 0:
        raise ValueError("Graph must have an even number of nodes to be k-regular")
    A = {nodes[0]}
    B = set(nodes[1:])
    satisfying_partitions = []
    for i in range(1, 2**(n-1)):
        A = {nodes[0]} | {nodes[j] for j in range(1, n) if (i & (1 << (j-1))) > 0}
        B = set(nodes) - A
        if is_satisfying(G, A, B):
            satisfying_partitions.append((A, B))
    return satisfying_partitions




# Preuve que ca marche pas pour K4 et K3,3
# G = nx.complete_graph(4)
# A, B = satisfying_partition(G)
# print("K4 valid:", is_satisfying(G, A, B))

# G = nx.complete_bipartite_graph(3, 3)
# A, B = satisfying_partition(G)
# print("K3,3 valid:", is_satisfying(G, A, B))


# On retrouve la partition satisfaisante pour un graphe 3-regulier aleatoire
G = nx.random_regular_graph(3, 10)
# G = load_graph(21)  # load the first graph from file 
# 21 VERY interesting
save_graph(G)

# Fix layout
seed = 42
pos = nx.spring_layout(G, seed=seed)

# Compute partitions
A1, B1 = satisfying_partition(G)
A2, B2 = satisfying_partition_3_regular(G)
A3, B3 = exhaustive_search_partition(G)
P = all_satisfying_partitions(G)
print(P)
print(f"Found {len(P)} satisfying partitions (including duplicates)")

# Plotting
n_plots = 3
n_cols = 2
n_rows = math.ceil(n_plots / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
axes = axes.flatten()

# Draw both on the same layout
plot_comparison(G, A1, B1, pos, ax=axes[0], title="Heuristic partition")
plot_comparison(G, A2, B2, pos, ax=axes[1], title="Cycle-based partition")
plot_comparison(G, A3, B3, pos, ax=axes[2], title="Exhaustive search partition")
fig.delaxes(axes[3])

# Or draw just one
# plot_single(G, A1, B1, pos=pos, title="Heuristic partition")

plt.show()

print("Now showing all partitions:")
n_plots = len(P)
n_cols = 3
n_rows = math.ceil(n_plots / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
axes = axes.flatten()
for i, (A, B) in enumerate(P):
    plot_comparison(G, A, B, pos, ax=axes[i], title=f"Partition {i+1}")
for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])
plt.show()