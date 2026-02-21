import numpy as np
import matplotlib.pyplot as plt
def himmelblau(x, y):
    return -(x**2 + y - 11)**2 - (x + y**2 - 7)**2
def hill_climbing(f, start, step_size=0.01, max_iterations=10000):
    current = np.array(start, dtype=float, copy=True)
    single_point = (current.ndim == 1)
    current = np.atleast_2d(current)
    directions = np.array([
        [step_size, 0], [-step_size, 0],
        [0, step_size], [0, -step_size]
    ])
    current_values = f(current[:, 0], current[:, 1])

    for _ in range(max_iterations):
        neighbors = current[:, np.newaxis, :] + directions
        neighbor_values = f(neighbors[:, :, 0], neighbors[:, :, 1])
        neighbor_values_best_idxes = np.argmax(neighbor_values, axis=1)
        row_idx = np.arange(current.shape[0])
        best_neighbors = neighbors[row_idx, neighbor_values_best_idxes]
        best_neighbor_values = neighbor_values[row_idx, neighbor_values_best_idxes]
        improved_mask = best_neighbor_values > current_values
        if not np.any(improved_mask):
            break
        current[improved_mask] = best_neighbors[improved_mask]
        current_values[improved_mask] = best_neighbor_values[improved_mask]
    return current[0] if single_point else current

def multi_start(hill_climbing_fn, n_agents, low=-5, high=5):
    start_points = np.random.uniform(low, high, size=(n_agents, 2))
    return hill_climbing_fn(start_points)

# Esecuzione dell'algoritmo

results = multi_start(lambda srt_pts: hill_climbing(himmelblau, srt_pts), 100)
results_unique = np.unique(np.round(results, 4), axis=0)
max_result = results_unique[np.argmax(himmelblau(results_unique[:, 0], results_unique[:, 1]))]
print(f"Trovate {len(results_unique)} soluzioni distinte")

print(f"Massimo migliore trovato: {max_result}")
print(f"Valore della funzione: {himmelblau(*max_result)}")

# Visualizzazione
x = np.linspace(-5, 5, 500)
y = np.linspace(-5, 5, 500)
X, Y = np.meshgrid(x, y)
Z = himmelblau(X, Y)

plt.figure(figsize=(10, 8), dpi=350) #dimensioni aumentate per vedere le fluttuazioni nei massimi relativi
plt.contour(X, Y, Z, levels=100)
plt.colorbar(label='f(x,y)')

# Tutti i risultati: piccoli puntini arancioni
plt.scatter(results_unique[:, 0], results_unique[:, 1], color='orange', s=0.01, alpha=0.35, label='Massimi locali')

plt.scatter(max_result[0], max_result[1], color='red', s=1, label='Massimo migliore')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ottimizzazione della funzione di Himmelblau con Multi-start Hill Climbing')
plt.show()