import numpy as np
import matplotlib.pyplot as plt
def himmelblau(x, y):
    return -(x**2 + y - 11)**2 - (x + y**2 - 7)**2
def hill_climbing(f, start, step_size=0.01, max_iterations=10000):
    current = start
    for _ in range(max_iterations):
        neighbors = [
            (current[0] + step_size, current[1]),
            (current[0] - step_size, current[1]),
            (current[0], current[1] + step_size),
            (current[0], current[1] - step_size)
        ]
        neighbor_values = [f(*n) for n in neighbors]
        best_neighbor = neighbors[np.argmax(neighbor_values)]
        if f(*best_neighbor) <= f(*current):
            return current
        current = best_neighbor
    return current
# Esecuzione dell'algoritmo
start_point = (np.random.uniform(-5, 5), np.random.uniform(-5, 5))
result = hill_climbing(himmelblau, start_point)
print(f"Punto di partenza: {start_point}")
print(f"Massimo locale trovato: {result}")
print(f"Valore della funzione: {himmelblau(*result)}")
# Visualizzazione
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = himmelblau(X, Y)
plt.figure(figsize=(10, 8))
plt.contour(X, Y, Z, levels=50)
plt.colorbar(label='f(x,y)')
plt.plot(*start_point, 'ro', label='Punto di partenza')
plt.plot(*result, 'go', label='Massimo locale trovato')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ottimizzazione della funzione di Himmelblau con HillClimbing')
plt.show()