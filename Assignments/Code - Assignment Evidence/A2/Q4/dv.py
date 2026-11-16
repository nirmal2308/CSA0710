"""Distance-vector routing (Bellman-Ford exchange) among five campus routers."""
import sys
INF = 99
names = "ABCDE"
cost = {("A", "B"): 2, ("A", "C"): 7, ("B", "C"): 3, ("B", "D"): 8,
        ("C", "D"): 1, ("D", "E"): 4}
if len(sys.argv) > 1 and sys.argv[1] == "fail":
    cost[("C", "D")] = 99                       # link C-D has failed
link = {}
for (u, v), c in cost.items():
    link[u, v] = link[v, u] = c
table = {u: {v: (0 if u == v else link.get((u, v), INF)) for v in names} for u in names}

def show(label):
    print(label)
    print("   " + " ".join(f"{v:>2}" for v in names))
    for u in names:
        print(u, " ", " ".join(f"{table[u][v]:2d}" for v in names))

if "-v" in sys.argv:
    show("initial (direct neighbours only)")
rounds = 0
changed = True
while changed:
    changed = False
    rounds += 1
    old = {u: dict(table[u]) for u in names}       # vectors received this round
    for u in names:
        for n in names:
            if (u, n) not in link or link[u, n] >= INF:
                continue
            for dest in names:
                # TODO 1 (completed): Bellman-Ford update through neighbour n
                if link[u, n] + old[n][dest] < table[u][dest]:
                    table[u][dest] = min(INF, link[u, n] + old[n][dest])
                    changed = True
    if "-v" in sys.argv and changed:
        show(f"after round {rounds}")
print(f"converged after {rounds} rounds")
for u in names:
    print(u, " ".join(f"{table[u][v]:2d}" for v in names))
