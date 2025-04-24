
import numpy as np
from random import shuffle

class State:
    def __init__(self, tour: list, cost: float):
        self.tour = tour  # Complete tour including start/end at city 0
        self.cost = cost  # Total cost of the tour
        self.parent = None

    def __eq__(self, other):
        return tuple(self.tour) == tuple(other.tour)

    def __hash__(self):
        return hash(tuple(self.tour))

    def __str__(self):
        return f"Tour: {self.tour}, Cost: {self.cost}"

def compute_tour_cost(tour: list, dist_matrix: np.ndarray) -> float:
    """Calculate the total cost of a tour."""
    cost = 0.0
    for i in range(len(tour) - 1):
        cost += dist_matrix[tour[i], tour[i + 1]]
    return cost

def get_neighbors(state: State, dist_matrix: np.ndarray) -> list:
    """Generate neighboring states using 2-opt swaps."""
    neighbors = []
    n = len(state.tour) - 1  # Exclude the final return to city 0
    for i in range(1, n - 1):  # Start from 1 to skip city 0
        for j in range(i + 1, n):
            # Create new tour by swapping cities at positions i and j
            new_tour = state.tour.copy()
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            cost = compute_tour_cost(new_tour, dist_matrix)
            neighbor = State(new_tour, cost)
            neighbor.parent = state
            neighbors.append(neighbor)
    return neighbors

def generate_initial_tour(n: int) -> list:
    """Generate a random initial tour starting and ending at city 0."""
    tour = [0] + list(range(1, n)) + [0]
    shuffle(tour[1:-1])  # Shuffle cities except start/end
    return tour

def hill_climbing_tsp(dist_matrix: np.ndarray) -> tuple:
    """
    Solve TSP using Hill Climbing with 2-opt swaps.
    
    Args:
        dist_matrix: NxN numpy array of distances between cities.
    
    Returns:
        Tuple of (optimal tour, total cost).
    """
    n = len(dist_matrix)
    if n <= 1:
        return [0], 0.0

    # Generate initial random tour
    initial_tour = generate_initial_tour(n)
    initial_cost = compute_tour_cost(initial_tour, dist_matrix)
    current_state = State(initial_tour, initial_cost)

    print(f"Initial: {current_state}")

    while True:
        # Generate neighbors
        neighbors = get_neighbors(current_state, dist_matrix)
        if not neighbors:
            break

        # Find the best neighbor (lowest cost)
        best_neighbor = min(neighbors, key=lambda x: x.cost)

        # If no improvement, stop
        if best_neighbor.cost >= current_state.cost:
            print("No better neighbor found. Stopping.")
            break

        # Move to the best neighbor
        current_state = best_neighbor
        print(f"Improved: {current_state}")

    print("Goal found!")
    return current_state.tour, current_state.cost

def print_solution(tour: list, cost: float):
    """Print the solution path for TSP."""
    if tour:
        print("\nSolution Path:")
        print(f"Tour: {tour}")
        print(f"Total Cost: {cost}")

# Example usage
if __name__ == "__main__":
    # Example distance matrix (symmetric TSP)
    dist_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    tour, cost = hill_climbing_tsp(dist_matrix)
    print_solution(tour, cost)