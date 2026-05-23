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
                    # found a cycle
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