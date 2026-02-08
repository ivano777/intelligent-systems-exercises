from collections import deque
import json
from pathlib import Path


def bfs_percorso(labirinto):
    N, M = len(labirinto), len(labirinto[0])
    queue = deque([(0, 0, 0)])
    visitati = set([(0, 0)])
    padre = {(0, 0): None}  # dizionario (mappa) per ricostruire il percorso
    direzioni = [(0, 1), (1, 0), (0, -1), (-1, 0)] # destra, giù, sinistra, su
    while queue:
        r, c, dist = queue.popleft()
        if r == N-1 and c == M-1:
            #ricostruisce il percorso risalendo i "padre"
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = padre[cur]
            path.reverse()
            return path  # invece di dist
        for dr, dc in direzioni:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M and labirinto[nr][nc] == 0 and (nr, nc) not in visitati:
                queue.append((nr, nc, dist + 1))
                padre[(nr, nc)] = (r, c)
                visitati.add((nr, nc))
    return None # Nessun percorso trovato


labirinto_1 = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto1.json").read_text(encoding="utf-8"))
labirinto_3 = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto3.json").read_text(encoding="utf-8"))

print(f"Il percorso più breve è: {bfs_percorso(labirinto_1)}")
print(f"Il percorso più breve sul labirinto esteso è: {bfs_percorso(labirinto_3)}")
