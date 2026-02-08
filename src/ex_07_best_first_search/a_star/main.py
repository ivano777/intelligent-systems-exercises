import heapq
import numpy as np

class Node:
    def __init__(self, pos, g, h, parent=None):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
    def __lt__(self, other):
        return self.f < other.f
    def __eq__(self, other):
            if not isinstance(other, Node):
                return False
            return self.pos == other.pos

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, grid):
    rows, cols = grid.shape
    open_list = []
    closed_set = set()
    start_node = Node(start, 0, manhattan_distance(start, goal))
    heapq.heappush(open_list, start_node)
    while open_list:
        current = heapq.heappop(open_list)
        if current.pos == goal:
            path = []
            while current:
                path.append(current.pos)
                current = current.parent
            return path[::-1]
        closed_set.add(current.pos)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current.pos[0] + dx, current.pos[1] + dy)
            if (next_pos[0] < 0 or next_pos[0] >= rows or next_pos[1] < 0 or next_pos[1] >= cols or grid[next_pos] == 2 or next_pos in closed_set):
                continue
            g = current.g + grid[next_pos]
            h = manhattan_distance(next_pos, goal)
            neighbor = Node(next_pos, g, h, current)
            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            else:
                idx = open_list.index(neighbor)
                if open_list[idx].g > g:
                    open_list[idx].g = g
                    open_list[idx].f = g + h
                    open_list[idx].parent = current
                    heapq.heapify(open_list)
    return None
# Esempio di utilizzo
grid = np.array([
    [1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1],
    [1, 1, 1, 3, 1],
    [1, 2, 2, 3, 1],
    [1, 1, 1, 1, 1]
])
start = (0, 0)
goal = (4, 4)
path = a_star(start, goal, grid)
print("Percorso ottimale:", path)