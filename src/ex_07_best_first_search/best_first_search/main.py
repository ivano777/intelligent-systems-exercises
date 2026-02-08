import heapq
class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def best_first_search(initial_state, goal_test, successors, heuristic):
    frontier = []
    explored = set()
    start_node = Node(initial_state, heuristic=heuristic(initial_state))
    heapq.heappush(frontier, start_node)
    while frontier:
        node = heapq.heappop(frontier)
        if goal_test(node.state):
            return reconstruct_path(node)
        explored.add(node.state)
        for action, state, step_cost in successors(node.state):
            if state not in explored:
                child = Node(state, node, action, node.cost + step_cost, heuristic(state))
                heapq.heappush(frontier, child)
    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.action, node.state))
        node = node.parent
    return list(reversed(path))

GOAL_STATE = (3, 3)
def goal_test(state):
    return state == GOAL_STATE

# i valori rappresentano i costi per arrivare a quel nodo; -1 non attraversabile
GRID_COSTS = [
    [1,     1,      1,      1],
    [1,     -1,     -1,     5],
    [1,     1,      5,      5],
    [1,     1,      1,      1],
]
ACTIONS = [(0,1),(1,0),(-1,0),(0,-1)] #destra,giù,sinistra,sù; vanno sommate allo stato
def successors(state):
    N, M = len(GRID_COSTS), len(GRID_COSTS[0])
    r, c = state
    res = []
    for action in ACTIONS:
        dr, dc = action
        nr = r+dr
        nc = c+dc
        if(0 <= nr < N and 0 <= nc < M): #resta nei limiti della griglia
            cost = GRID_COSTS[nr][nc]
            if(cost >= 0): #evita i muri (-1)
                res.append((action ,(nr,nc), cost))
    return res #ritornare una list di: azioni_valide; stati_di_arrivo; costi_associati

def heuristic(state):
    r,c = state
    gr,gc = GOAL_STATE
    return abs(gr - r) + abs(gc - c) 

# Esempio di utilizzo:
# [Implementare qui le funzioni goal_test, successors, e heuristic specifiche per il problema]
initial_state = (0,0)
solution = best_first_search(initial_state, goal_test, successors, heuristic)
if solution:
    print("Soluzione trovata:", solution)
else:
    print("Nessuna soluzione trovata")