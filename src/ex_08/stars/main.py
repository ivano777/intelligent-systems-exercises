import heapq
import time

class Nodo:
    def __init__(self, stato, genitore=None, azione=None, costo=0, h=0):
        self.stato = stato
        self.genitore = genitore
        self.azione = azione
        self.costo = costo
        self.h = h
        self.f = costo + h

    def __lt__(self, altro):
        return self.f < altro.f

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.stato)
        node = node.genitore
    return list(reversed(path))

def a_star(start, goal, h, successors):
    start_node = Nodo(start, h=h(start))
    frontier = []
    heapq.heappush(frontier, start_node)
    explored = set()
    
    while frontier:
        current_node = heapq.heappop(frontier)
        if current_node.stato == goal:
            return reconstruct_path(current_node)
        
        explored.add(current_node.stato)
        
        for successor, cost in successors(current_node.stato):
            new_cost = current_node.costo + cost
            new_node = Nodo(successor, current_node, None, new_cost, h(successor))
            
            if successor not in explored and successor not in [n.stato for n in frontier]:
                heapq.heappush(frontier, new_node)
            elif successor in [n.stato for n in frontier]:
                index = [n.stato for n in frontier].index(successor)
                if frontier[index].costo > new_cost:
                    frontier[index] = new_node
                    heapq.heapify(frontier)
    return None

def ida_star(start, goal, h, successors):
    def search(path, g, f_limit):
        node = path[-1]
        f = g + h(node)
        if f > f_limit:
            return f
        if node == goal:
            return "FOUND"
        min_cost = float('inf')
        for successor, cost in successors(node):
            if successor not in path:
                path.append(successor)
                t = search(path, g + cost, f_limit)
                if t == "FOUND":
                    return "FOUND"
                if t < min_cost:
                    min_cost = t
                path.pop()
        return min_cost

    f_limit = h(start)
    while True:
        t = search([start], 0, f_limit)
        if t == "FOUND":
            return "Solution found"
        if t == float('inf'):
            return "Solution not found"
        f_limit = t

def ara_star(start, goal, h, successors, time_limit):
    def reconstruct_path_ara(came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return list(reversed(path))

    def improve_path():
        while open_set and time.time() < end_time:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return reconstruct_path_ara(came_from, current)
            
            closed_set.add(current)
            for neighbor, cost in successors(current):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = g_score[neighbor] + epsilon * h(neighbor)
                    
                    if neighbor not in [n for _, n in open_set]:
                        heapq.heappush(open_set, (f_score, neighbor))
                    else:
                        for i, (_, n) in enumerate(open_set):
                            if n == neighbor:
                                open_set[i] = (f_score, neighbor)
                                heapq.heapify(open_set)
                                break
        return None

    epsilon = 3.0
    end_time = time.time() + time_limit
    open_set = [(h(start), start)]
    closed_set = set()
    came_from = {}
    g_score = {start: 0}

    while time.time() < end_time:
        path = improve_path()
        if path:
            return path
        epsilon = max(1.0, epsilon - 0.5)
        open_set = [(h(start), start)]
        closed_set.clear()
        came_from.clear()
        g_score = {start: 0}
        
    return None

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_successors(node, grid):
    successors = []
    x, y = node
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != 2:
            successors.append(((new_x, new_y), grid[new_x][new_y]))
    return successors

# Test e confronto
grid = [
    [1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1],
    [1, 1, 1, 3, 1],
    [1, 2, 2, 3, 1],
    [1, 1, 1, 1, 1]
]
start = (0, 0)
goal = (4, 4)

print("A*:")
start_time = time.time()
path = a_star(start, goal, lambda x: manhattan_distance(x, goal), lambda x: get_successors(x, grid))
print(f"Tempo: {time.time() - start_time:.5f} secondi")
print(f"Percorso: {path}")

print("\nIDA*:")
start_time = time.time()
result = ida_star(start, goal, lambda x: manhattan_distance(x, goal), lambda x: get_successors(x, grid))
print(f"Tempo: {time.time() - start_time:.5f} secondi")
print(f"Risultato: {result}")

print("\nARA*:")
start_time = time.time()
path = ara_star(start, goal, lambda x: manhattan_distance(x, goal), lambda x: get_successors(x, grid), 1.0)
print(f"Tempo: {time.time() - start_time:.5f} secondi")
print(f"Percorso: {path}")