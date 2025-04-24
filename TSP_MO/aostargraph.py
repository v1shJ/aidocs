from collections import defaultdict

def ao_star(graph, costs, is_and_node, start_node, goal_nodes, max_iterations=50):
    """Solve an And/Or graph using AO* search."""
    # Initialize open set with start node
    open_set = {start_node: (0, None)}  # node: (cost, parent)
    best_cost = float('inf')
    best_solution = None

    print(f"Starting AO* from node: {start_node}")

    for iteration in range(max_iterations):
        if not open_set:
            break

        # Select node to expand (lowest cost)
        current_node = min(open_set, key=lambda x: open_set[x][0])
        current_cost, _ = open_set[current_node]
        del open_set[current_node]

        # If goal node, update best solution
        if current_node in goal_nodes:
            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = current_node
                print(f"Iteration {iteration + 1}: Goal found: {current_node}, Cost: {current_cost}")
            continue

        # Expand node
        successors = graph[current_node]
        for succ in successors:
            succ_cost = costs.get((current_node, succ), 1)  # Default cost 1
            total_cost = current_cost + succ_cost
            open_set[succ] = (total_cost, current_node)

        # Backpropagate costs
        while current_node:
            if current_node not in open_set:
                break
            cost, parent = open_set[current_node]
            successors = graph[current_node]
            if not successors:
                continue

            if is_and_node[current_node]:  # AND node: sum of all successor costs
                succ_costs = [
                    open_set.get(s, (float('inf'), None))[0]
                    for s in successors
                    if s in open_set or s in goal_nodes
                ]
                if len(succ_costs) == len(successors):
                    new_cost = current_cost + sum(succ_costs)
                    open_set[current_node] = (new_cost, parent)
            else:  # OR node: minimum successor cost
                succ_costs = [
                    open_set.get(s, (float('inf'), None))[0]
                    for s in successors
                    if s in open_set or s in goal_nodes
                ]
                if succ_costs:
                    new_cost = current_cost + min(succ_costs)
                    open_set[current_node] = (new_cost, parent)

            current_node = parent

    print(f"Final solution: {best_solution}, Cost: {best_cost}")
    return best_solution, best_cost

# Example usage
if __name__ == "__main__":
    # Define the And/Or graph
    graph = defaultdict(list, {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [],
        'E': [],
        'F': ['H', 'I'],
        'G': [],
        'H': [],
        'I': []
    })

    # Define edge costs
    costs = {
        ('A', 'B'): 2, ('A', 'C'): 3,
        ('B', 'D'): 4, ('B', 'E'): 5,
        ('C', 'F'): 2, ('C', 'G'): 6,
        ('F', 'H'): 1, ('F', 'I'): 2
    }

    # Define AND nodes (others are OR nodes)
    is_and_node = defaultdict(bool, {'F': True})

    # Define goal nodes
    goal_nodes = {'D', 'E', 'G', 'H', 'I'}

    # Run AO* search
    solution, cost = ao_star(graph, costs, is_and_node, 'A', goal_nodes)
    print(f"Solution node: {solution}, Total cost: {cost}")
