import heapq
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
    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return False
        return self.stato == other.stato
def a_star(stato_iniziale, test_obiettivo, successori, h):
    nodo_iniziale = Nodo(stato_iniziale, h=h(stato_iniziale))
    frontiera = [nodo_iniziale]
    esplorati = set()
    while frontiera:
        nodo_corrente = heapq.heappop(frontiera)
        if test_obiettivo(nodo_corrente.stato):
            return ricostruisci_percorso(nodo_corrente)
        esplorati.add(nodo_corrente.stato)
        for azione, stato, costo_passo in successori(nodo_corrente.stato):
            nuovo_costo = nodo_corrente.costo + costo_passo
            nuovo_nodo = Nodo(stato, nodo_corrente, azione, nuovo_costo, h(stato))
            if stato not in esplorati and nuovo_nodo not in frontiera:
                heapq.heappush(frontiera, nuovo_nodo)
            elif stato in frontiera:
                indice = frontiera.index(nuovo_nodo)
                if frontiera[indice].costo > nuovo_costo:
                    frontiera[indice] = nuovo_nodo
                    heapq.heapify(frontiera)
    return None
def ricostruisci_percorso(nodo):
    percorso = []
    while nodo:
        percorso.append((nodo.azione, nodo.stato))
        nodo = nodo.genitore
    return list(reversed(percorso))
GOAL_STATE = (3,3)
stato_iniziale = (0,0)
def test_obiettivo(state):
    return GOAL_STATE == state
def h(state):
    r,c = state
    gr,gc = GOAL_STATE
    return abs(gr - r) + abs(gc - c)

def successori(state):
    N, M = len(GRID_COSTS), len(GRID_COSTS[0])
    r, c = state
    res = []
    for action in ACTIONS:
        name, move = action
        dr, dc = move
        nr = r+dr
        nc = c+dc
        if(0 <= nr < N and 0 <= nc < M): #resta nei limiti della griglia
            cost = GRID_COSTS[nr][nc]
            if(cost >= 0): #evita i muri (-1)
                res.append((name ,(nr,nc), cost))
    return res #ritornare una list di: azioni_valide; stati_di_arrivo; costi_associati

GRID_COSTS = [
    [1,     1,      1,      1],
    [1,     -1,     -1,     5],
    [1,     1,      5,      5],
    [1,     1,      1,      1],
]
ACTIONS = [("Right",(0,1)),("Down",(1,0)),("Left",(-1,0)),("Su",(0,-1))] #destra,giù,sinistra,sù; vanno sommate allo stato

# Funzioni da implementare:
# def test_obiettivo(stato):
# def successori(stato):
# def h(stato):
# Esempio di utilizzo:
# stato_iniziale = ...
#
soluzione = a_star(stato_iniziale, test_obiettivo, successori, h)
if soluzione:
    print("Soluzione trovata:", soluzione)
else:
    print("Nessuna soluzione trovata")