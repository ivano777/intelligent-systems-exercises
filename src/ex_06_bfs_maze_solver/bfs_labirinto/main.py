from collections import deque
import json
from pathlib import Path

def bfs_labirinto(labirinto):
    N, M = len(labirinto), len(labirinto[0])
    queue = deque([(0, 0, 0)]) # (riga, colonna, distanza)
    visitati = set([(0, 0)])
    direzioni = [(0, 1), (1, 0), (0, -1), (-1, 0)] # destra, giù, sinistra, su
    while queue:
        r, c, dist = queue.popleft()
        if r == N-1 and c == M-1:
            return dist # Trovata l'uscita
        for dr, dc in direzioni:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M and labirinto[nr][nc] == 0 and (nr, nc) not in visitati:
                queue.append((nr, nc, dist + 1))
                visitati.add((nr, nc))
    return -1 # Nessun percorso trovato

labirinto_1 = labirinto = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto1.json").read_text(encoding="utf-8"))
labirinto_2 = labirinto = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto2.json").read_text(encoding="utf-8"))
labirinto_3 = labirinto = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto3.json").read_text(encoding="utf-8"))

risultato = bfs_labirinto(labirinto)
print(f"La lunghezza del percorso più breve è: {risultato}")
print(f"La lunghezza del percorso più breve aggiungendo un ostacolo in (2,1) è: {bfs_labirinto(labirinto_2)}")
print(f"La lunghezza del percorso più breve sul labirinto esteso è: {bfs_labirinto(labirinto_3)}")
