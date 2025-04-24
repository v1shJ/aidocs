import heapq
import math

def mst_cost(graph, vertices):
    """Compute the cost of the Minimum Spanning Tree for vertices using Prim's algorithm."""
    if not vertices:
        return 0
    n = len(graph)
    visited = set([vertices[0]])
    edges = [(graph[vertices[0]][j], vertices[0], j) for j in range(n) if j in vertices[1:]]
    heapq.heapify(edges)
    total_cost = 0

    while edges and len(visited) < len(vertices):
        cost, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            total_cost += cost
            for w in range(n):
                if w in vertices and w not in visited:
                    heapq.heappush(edges, (graph[v][w], v, w))

    return total_cost

def astar_tsp(graph, start=0):
    n = len(graph)  # Number of cities
    # State: (f_score, current_city, visited_cities, g_score, path)
    pq = [(0, start, frozenset([start]), 0, [start])]
    visited_states = {}  # (current_city, visited_cities): min g_score
    best_tour = None
    best_distance = float('inf')

    print(f"Starting A* TSP from city {start}")
    while pq:
        f_score, current, visited, g_score, path = heapq.heappop(pq)
        print(f"Exploring state: current={current}, path={path}, g={g_score}, f={f_score}")

        # If all cities visited, try returning to start
        if len(visited) == n:
            return_distance = graph[current][start]
            total_distance = g_score + return_distance
            if total_distance < best_distance:
                best_tour = path + [start]
                best_distance = total_distance
                print(f"Found tour: {best_tour}, distance={best_distance}")
            continue

        # Skip if we've seen this state with a lower g_score
        state_key = (current, visited)
        if state_key in visited_states and visited_states[state_key] <= g_score:
            continue
        visited_states[state_key] = g_score

        # Explore unvisited cities
        unvisited = [i for i in range(n) if i not in visited]
        for next_city in unvisited:
            new_visited = frozenset(visited | {next_city})
            new_g_score = g_score + graph[current][next_city]

            # Heuristic: MST cost of unvisited cities + min edges to connect
            remaining = [i for i in range(n) if i not in new_visited]
            mst = mst_cost(graph, remaining)
            # Min distance from current to remaining (if any)
            min_to_remaining = min((graph[next_city][i] for i in remaining), default=0)
            # Min distance from remaining to start (if any)
            min_to_start = min((graph[i][start] for i in remaining), default=0)
            h_score = mst + min_to_remaining + min_to_start
            f_score = new_g_score + h_score

            new_path = path + [next_city]
            print(f"  Adding next={next_city}, g={new_g_score}, h={h_score}, f={f_score}")
            heapq.heappush(pq, (f_score, next_city, new_visited, new_g_score, new_path))

    return best_tour, best_distance

# Example usage
def main():
    # Sample distance matrix (symmetric, undirected graph)
    graph = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 30, 20, 15, 0]
    ]

    # Run A* starting from city 0
    tour, distance = astar_tsp(graph, start=0)

    if tour:
        print("A* TSP Tour:", " -> ".join(map(str, tour)))
        print("Total Distance:", distance)
    else:
        print("No tour found")

if __name__ == "__main__":
    main()