import numpy as np
from typing import List, Tuple
import random

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
    # Return to start city
    distance += dist_matrix[path[-1]][path[0]]
    return distance

def beam_search_tsp(dist_matrix: np.ndarray, beam_width: int, max_iterations: int = 100) -> Tuple[List[int], float]:
    """Solve TSP using Beam Search."""
    n = len(dist_matrix)
    # Initialize with random starting paths
    current_beam = [[i] for i in range(min(beam_width, n))]
    
    best_path = None
    best_distance = float('inf')
    
    for _ in range(max_iterations):
        if not current_beam:
            break
            
        # Generate all possible next states
        next_beam = []
        for path in current_beam:
            last_city = path[-1]
            # Get unvisited cities
            unvisited = [i for i in range(n) if i not in path]
            
            for next_city in unvisited:
                new_path = path + [next_city]
                distance = total_distance(new_path, dist_matrix)
                next_beam.append((new_path, distance))
        
        # Sort by distance and keep top beam_width paths
        next_beam.sort(key=lambda x: x[1])
        current_beam = [path for path, _ in next_beam[:beam_width]]
        
        # Update best solution if complete path found
        for path, distance in next_beam:
            if len(path) == n and distance < best_distance:
                best_path = path
                best_distance = distance
                
        # If all cities visited, break
        if all(len(path) == n for path in current_beam):
            break
    
    return best_path, best_distance

def beam_stochastic_search_tsp(dist_matrix: np.ndarray, beam_width: int, max_iterations: int = 100, temperature: float = 1.0) -> Tuple[List[int], float]:
    """Solve TSP using Beam Stochastic Search."""
    n = len(dist_matrix)
    current_beam = [[i] for i in range(min(beam_width, n))]
    
    best_path = None
    best_distance = float('inf')
    
    for _ in range(max_iterations):
        if not current_beam:
            break
            
        next_beam = []
        for path in current_beam:
            last_city = path[-1]
            unvisited = [i for i in range(n) if i not in path]
            
            for next_city in unvisited:
                new_path = path + [next_city]
                distance = total_distance(new_path, dist_matrix)
                next_beam.append((new_path, distance))
        
        # Calculate selection probabilities using Boltzmann distribution
        if next_beam:
            distances = np.array([d for _, d in next_beam])
            probabilities = np.exp(-distances / temperature)
            probabilities /= probabilities.sum()
            
            # Stochastically select beam_width paths
            indices = np.random.choice(
                len(next_beam),
                size=min(beam_width, len(next_beam)),
                replace=False,
                p=probabilities
            )
            current_beam = [next_beam[i][0] for i in indices]
            
            # Update best solution
            for path, distance in next_beam:
                if len(path) == n and distance < best_distance:
                    best_path = path
                    best_distance = distance
        
        if all(len(path) == n for path in current_beam):
            break
    
    return best_path, best_distance

def main():
    # Example usage
    # Generate random cities (x, y coordinates)
    np.random.seed(42)
    n_cities = 10
    cities = [(np.random.rand(), np.random.rand()) for _ in range(n_cities)]
    dist_matrix = calculate_distance_matrix(cities)
    
    # Parameters
    beam_width = 5
    max_iterations = 100
    temperature = 1.0
    
    # Run Beam Search
    path_beam, dist_beam = beam_search_tsp(dist_matrix, beam_width, max_iterations)
    print(f"Beam Search - Best path: {path_beam}")
    print(f"Beam Search - Total distance: {dist_beam:.4f}")
    
    # Run Beam Stochastic Search
    path_stochastic, dist_stochastic = beam_stochastic_search_tsp(
        dist_matrix, beam_width, max_iterations, temperature
    )
    print(f"Stochastic Beam Search - Best path: {path_stochastic}")
    print(f"Stochastic Beam Search - Total distance: {dist_stochastic:.4f}")

if __name__ == "__main__":
    main()