import random

def compute_tour_cost(tour, dist_matrix):
    """Calculate the total cost of a tour."""
    cost = 0.0
    for i in range(len(tour) - 1):
        cost += dist_matrix[tour[i]][tour[i + 1]]
    return cost

def get_neighbors(tour, dist_matrix):
    """Generate neighboring tours using 2-opt swaps."""
    neighbors = []
    n = len(tour) - 1  # Exclude final return to city 0
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            new_tour = tour.copy()
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            cost = compute_tour_cost(new_tour, dist_matrix)
            neighbors.append((new_tour, cost))
    return neighbors

def generate_initial_tour(n):
    """Generate a random initial tour starting and ending at city 0."""
    tour = [0] + list(range(1, n)) + [0]
    random.shuffle(tour[1:-1])
    return tour

def hill_climbing_tsp(dist_matrix):
    """Solve TSP using hill climbing with 2-opt swaps."""
    n = len(dist_matrix)
    if n <= 1:
        return [0], 0.0

    # Generate initial tour
    current_tour = generate_initial_tour(n)
    current_cost = compute_tour_cost(current_tour, dist_matrix)
    print(f"Initial tour: {current_tour}, Cost: {current_cost}")

    while True:
        neighbors = get_neighbors(current_tour, dist_matrix)
        if not neighbors:
            break

        # Find best neighbor
        best_tour, best_cost = min(neighbors, key=lambda x: x[1])

        # Stop if no improvement
        if best_cost >= current_cost:
            print("No better neighbor found. Stopping.")
            break

        # Move to best neighbor
        current_tour, current_cost = best_tour, best_cost
        print(f"Improved tour: {current_tour}, Cost: {current_cost}")

    print("Final tour found!")
    return current_tour, current_cost

# Example usage
if __name__ == "__main__":
    # Example distance matrix
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tour, cost = hill_climbing_tsp(dist_matrix)
    print(f"\nSolution: Tour: {tour}, Cost: {cost}")
