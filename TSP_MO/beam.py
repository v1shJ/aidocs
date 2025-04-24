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

def beam_search_tsp(dist_matrix, beam_width=3, max_iterations=50):
    """Solve TSP using beam search with 2-opt swaps."""
    n = len(dist_matrix)
    if n <= 1:
        return [0], 0.0

    # Generate initial beam with one random tour
    current_beam = [(generate_initial_tour(n), 0.0)]
    current_beam[0] = (current_beam[0][0], compute_tour_cost(current_beam[0][0], dist_matrix))
    print(f"Initial tour: {current_beam[0][0]}, Cost: {current_beam[0][1]}")

    best_tour = current_beam[0][0]
    best_cost = current_beam[0][1]

    for iteration in range(max_iterations):
        next_beam = []
        # Generate neighbors for each tour in the current beam
        for tour, _ in current_beam:
            neighbors = get_neighbors(tour, dist_matrix)
            next_beam.extend(neighbors)

        # If no neighbors, stop
        if not next_beam:
            break

        # Sort by cost and keep top beam_width tours
        next_beam.sort(key=lambda x: x[1])
        current_beam = next_beam[:beam_width]

        # Update best solution if improved
        for tour, cost in current_beam:
            if cost < best_cost:
                best_tour, best_cost = tour, cost
                print(f"Iteration {iteration + 1}: Improved tour: {best_tour}, Cost: {best_cost}")

        # Stop if all tours in beam are complete and no improvement
        if all(len(tour) == n + 1 for tour, _ in current_beam) and current_beam[0][1] >= best_cost:
            print("No better tours found. Stopping.")
            break

    print("Final tour found!")
    return best_tour, best_cost

# Example usage
if __name__ == "__main__":
    # Example distance matrix
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tour, cost = beam_search_tsp(dist_matrix)
    print(f"\nSolution: Tour: {tour}, Cost: {cost}")
