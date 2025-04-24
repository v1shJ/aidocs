import numpy as np
from typing import List, Tuple
import heapq

def calculate_distance_matrix(cities: List[Tuple[float, float]]) -> np.ndarray:
    """Calculate Euclidean distance matrix between cities."""
    n = len(cities)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = np.sqrt(
                    (cities[i][0] - cities[j][0])**2 + 
                    (cities[i][1] - cities[j][1])**2
                )
    return dist_matrix

def total_distance(path: List[int], dist_matrix: np.ndarray) -> float:
    """Calculate total distance of a path."""
    distance = 0
    for i in range(len(path) - 1):
        distance += dist_matrix[path[i]][path[i + 1]]
    return distance

def simple_heuristic(unvisited: List[int], dist_matrix: np.ndarray, current_city: int, start_city: int) -> float:
    """Simple heuristic: minimum edge cost for unvisited cities plus return to start."""
    if not unvisited:
        return dist_matrix[current_city][start_city]
    # Minimum cost to visit an unvisited city
    min_edge = min(dist_matrix[current_city][i] for i in unvisited)
    # Minimum cost to return to start from any unvisited city
    min_return = min(dist_matrix[i][start_city] for i in unvisited)
    return min_edge + min_return

def astar_tsp(dist_matrix: np.ndarray, max_iterations: int = 10000) -> Tuple[List[int], float]:
    """Solve TSP using A* Search with a simple heuristic."""
    n = len(dist_matrix)
    start_city = 0
    
    # Priority queue: (f_score, g_score, path, unvisited)
    open_set = [(0, 0, [start_city], set(range(n)) - {start_city})]
    heapq.heapify(open_set)
    
    best_path = None
    best_distance = float('inf')
    iteration = 0
    
    while open_set and iteration < max_iterations:
        iteration += 1
        f_score, g_score, path, unvisited = heapq.heappop(open_set)
        
        # If all cities visited, check return to start
        if not unvisited:
            total_dist = g_score + dist_matrix[path[-1]][start_city]
            if total_dist < best_distance:
                best_distance = total_dist
                best_path = path + [start_city]
            continue
        
        # Expand to neighboring cities
        current_city = path[-1]
        for next_city in unvisited:
            new_path = path + [next_city]
            new_g_score = g_score + dist_matrix[current_city][next_city]
            new_unvisited = unvisited - {next_city}
            
            # Calculate heuristic
            h_score = simple_heuristic(list(new_unvisited), dist_matrix, next_city, start_city)
            f_score = new_g_score + h_score
            
            heapq.heappush(open_set, (f_score, new_g_score, new_path, new_unvisited))
    
    return best_path, best_distance

def main():
    # Example usage
    np.random.seed(42)
    n_cities = 10
    cities = [(np.random.rand(), np.random.rand()) for _ in range(n_cities)]
    dist_matrix = calculate_distance_matrix(cities)
    
    # Parameters
    max_iterations = 10000
    
    # Run A* Search
    path_astar, dist_astar = astar_tsp(dist_matrix, max_iterations)
    print(f"A* Search - Best path: {path_astar}")
    print(f"A* Search - Total distance: {dist_astar:.4f}")

if __name__ == "__main__":
    main()