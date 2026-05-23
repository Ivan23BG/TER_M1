def random_3_regular_graph(n):
    if n < 4 or (3 * n) % 2 != 0:
        raise ValueError("No 3-regular graph exists for this n")
    return nx.random_regular_graph(3, n)


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