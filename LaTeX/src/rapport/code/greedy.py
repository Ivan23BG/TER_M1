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
