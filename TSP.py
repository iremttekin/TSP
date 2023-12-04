import pulp as pl

distance_matrix = [
    [0, 100, 100, 2, 1, 100],
    [7, 0, 1, 100, 100, 100],
    [6, 5, 0, 3, 6, 100],
    [5, 3, 9, 0, 7, 100],
    [100, 100, 8, 100, 0, 1],
    [3, 100, 100, 7, 9, 0]
]

num_cities = len(distance_matrix)

tsp = pl.LpProblem("Travelling Salesperson Problem")

x = pl.LpVariable.dicts("x", [(i, j) for i in range(num_cities) for j in range(num_cities) if i != j], 0, 1, pl.LpBinary)
u = pl.LpVariable.dicts("u", [i for i in range(num_cities)], 0, num_cities - 1, pl.LpInteger)
tsp += pl.lpSum([distance_matrix[i][j] * x[i, j] for i in range(num_cities) for j in range(num_cities) if i != j])

for i in range(num_cities):
    tsp += pl.lpSum([x[i, j] for j in range(num_cities) if i != j]) == 1

for j in range(num_cities):
    tsp += pl.lpSum([x[i, j] for i in range(num_cities) if i != j]) == 1

for i in range(num_cities):
    for j in range(num_cities):
        if i != j and i and j != 0:
            tsp += u[i] - u[j] + 1 <= (num_cities - 1) * (1 - x[i, j])

tsp += u[0] == 0
tsp.solve()
if pl.LpStatus[tsp.status] == "Optimal":
    print("Optimal solution found.")
else:
    print("Problem couldn't be solved.")

print("Path:")
i = 0
while True:
    j_list = [j for j in range(num_cities) if i != j and pl.value(x[i, j]) == 1]
    if j_list:
        j = j_list[0]
        print(f"City {i + 1} to City {j + 1}")
        i = j
        if i == 0:
            break
    else:
        break
