G = nx.random_regular_graph(3, 10)
# G = load_graph(21)  # load the 21st first graph from file 
save_graph(G)         # in case it turns out to be interesting

# Fix layout
seed = 42
pos = nx.spring_layout(G, seed=seed)

# Compute partitions
A1, B1 = satisfying_partition(G)
A2, B2 = satisfying_partition_3_regular(G)
A3, B3 = exhaustive_search_partition(G)
P = all_satisfying_partitions(G)
print(P)
print(f"Found {len(P)} satisfying partitions (with duplicates)")

# Plotting
n_plots = 3
n_cols = 2
n_rows = math.ceil(n_plots / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
axes = axes.flatten()

# Draw all of them on the same layout
plot_comparison(G, A1, B1, 
                pos, ax=axes[0], 
                title="Heuristic partition")
plot_comparison(G, A2, B2, 
                pos, ax=axes[1], 
                title="Cycle-based partition")
plot_comparison(G, A3, B3, 
                pos, ax=axes[2], 
                title="Exhaustive search partition")
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