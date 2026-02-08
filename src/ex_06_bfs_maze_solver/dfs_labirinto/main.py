import json
from pathlib import Path

def dfs_labirinto(labirinto):
    N, M = len(labirinto), len(labirinto[0])
    stack = [(0, 0, 0)]     # qui usiamo uno stack al posto di una queue
    visitati = set([(0, 0)])
    direzioni = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while stack:
        r, c, dist = stack.pop() #qui usiamo pop invece che popleft
        if r == N-1 and c == M-1:
            return dist 
        for dr, dc in direzioni:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M and labirinto[nr][nc] == 0 and (nr, nc) not in visitati:
                stack.append((nr, nc, dist + 1))
                visitati.add((nr, nc))
    return -1

labirinto_1 = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto1.json").read_text(encoding="utf-8"))
labirinto_3 = labirinto = json.loads((Path(__file__).resolve().parent.parent / "resources" / "labirinto3.json").read_text(encoding="utf-8"))

print(f"La lunghezza del percorso più breve usando dfs è: {dfs_labirinto(labirinto_1)}")
print(f"La lunghezza del percorso più breve sul labirinto esteso è: {dfs_labirinto(labirinto_3)}")
