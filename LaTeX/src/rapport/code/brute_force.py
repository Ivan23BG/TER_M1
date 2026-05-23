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
