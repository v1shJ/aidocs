import random

def compute_tour_cost(tour, dist_matrix):
    """Calculate the cost of a tour (partial or complete)."""
    cost = 0.0
    for i in range(len(tour) - 1):
        cost += dist_matrix[tour[i]][tour[i + 1]]
    return cost

def get_or_successors(tour, dist_matrix, unvisited):
    """Generate OR successors by adding one unvisited city."""
    successors = []
    for city in unvisited:
        new_tour = tour[:-1] + [city] + [tour[-1]]  # Insert before return to 0
        cost = compute_tour_cost(new_tour, dist_matrix)
        new_unvisited = unvisited - {city}
        successors.append((new_tour, cost, new_unvisited))
    return successors

def get_and_successors(tour, dist_matrix):
    """Generate AND successors using 2-opt swaps for complete tours."""
    successors = []
    n = len(tour) - 1  # Exclude final return to city 0
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            new_tour = tour.copy()
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            cost = compute_tour_cost(new_tour, dist_matrix)
            successors.append((new_tour, cost, set()))
    return successors

def ao_star_tsp(dist_matrix, max_iterations=50):
    """Solve TSP using AO* search with an And/Or graph."""
    n = len(dist_matrix)
    if n <= 1:
        return [0], 0.0

    # Initialize with a partial tour [0, 0]
    start_tour = [0, 0]
    start_cost = 0.0
    unvisited = set(range(1, n))
    open_set = {tuple(start_tour): (start_cost, unvisited, None)}  # (cost, unvisited, parent)
    best_tour = start_tour
    best_cost = float('inf')

    print(f"Initial tour: {start_tour}, Cost: {start_cost}")

    for iteration in range(max_iterations):
        if not open_set:
            break

        # Select node to expand (lowest cost)
        current_tour = min(open_set, key=lambda x: open_set[x][0])
        current_cost, current_unvisited, _ = open_set[current_tour]
        del open_set[current_tour]

        # If complete tour, check for AND successors (2-opt swaps)
        if not current_unvisited:
            if current_cost < best_cost:
                best_tour, best_cost = list(current_tour), current_cost
                print(f"Iteration {iteration + 1}: Improved tour: {best_tour}, Cost: {best_cost}")
            successors = get_and_successors(list(current_tour), dist_matrix)
            for new_tour, new_cost, _ in successors:
                open_set[tuple(new_tour)] = (new_cost, set(), current_tour)
            continue

        # OR node: expand by adding unvisited cities
        successors = get_or_successors(list(current_tour), dist_matrix, current_unvisited)
        for new_tour, new_cost, new_unvisited in successors:
            open_set[tuple(new_tour)] = (new_cost, new_unvisited, current_tour)

        # Backpropagate costs
        while current_tour:
            if current_tour not in open_set:
                break
            cost, unvisited, parent = open_set[current_tour]
            if not unvisited:  # AND node
                successors = get_and_successors(list(current_tour), dist_matrix)
                if successors:
                    min_cost = min(s_cost for _, s_cost, _ in successors)
                    open_set[current_tour] = (min_cost, unvisited, parent)
            else:  # OR node
                successors = get_or_successors(list(current_tour), dist_matrix, unvisited)
                if successors:
                    min_cost = min(s_cost for _, s_cost, _ in successors)
                    open_set[current_tour] = (min_cost, unvisited, parent)
            current_tour = parent

    print("Final tour found!")
    return best_tour, best_cost

# Example usage
if __name__ == "__main__":
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tour, cost = ao_star_tsp(dist_matrix)
    print(f"\nSolution: Tour: {tour}, Cost: {cost}")
