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


def is_satisfying(G, A, B):
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


def plot_partitioned_graph(G, A, B, figsize=(8,6), node_size=600, font_size=12):
    """
    Plot a NetworkX graph with partitioned nodes and colored edges.
    
    Parameters:
    - G: networkx.Graph
    - A: set of nodes in partition A
    - B: set of nodes in partition B
    - figsize: tuple, figure size
    - node_size: int, node size
    - font_size: int, label font size
    """
    # Node colors
    color_map = ["skyblue" if v in A else "salmon" for v in G.nodes()]
    
    # Edge colors
    edge_colors = []
    for u, v in G.edges():
        if (u in A and v in A) or (u in B and v in B):
            edge_colors.append("green")  # internal
        else:
            edge_colors.append("red")    # external
    
    # Draw
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G)  # nice layout
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
    plt.show()


# Preuve que ca marche pas pour K4 et K3,3
# G = nx.complete_graph(4)
# A, B = satisfying_partition(G)
# print("K4 valid:", is_satisfying(G, A, B))

# G = nx.complete_bipartite_graph(3, 3)
# A, B = satisfying_partition(G)
# print("K3,3 valid:", is_satisfying(G, A, B))


# On retrouve la partition satisfaisante pour un graphe 3-regulier aleatoire
G = nx.random_regular_graph(3, 8)
# Get partitions
A, B = satisfying_partition(G)

# Plot
plot_partitioned_graph(G, A, B)