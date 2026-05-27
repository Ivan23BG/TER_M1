def exhaustive_search_partition(G):
    # fix a node in A then try all partitions of the rest
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