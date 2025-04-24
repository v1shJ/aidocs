from math import ceil
from collections import defaultdict
import numpy as np

class State:
    def __init__(self, current_city: int, path: list, unvisited: set, cost: float):
        self.current_city = current_city  # Current city in the tour
        self.path = path  # List of cities visited
        self.unvisited = unvisited  # Set of unvisited cities
        self.g = cost  # Cost of path so far
        self.h = 0  # Heuristic estimate
        self.cost = float('inf')  # f = g + h
        self.parent = None
        self.children = []
        self.solved = False
        self.and_node = False

    def __eq__(self, other):
        return (self.current_city, tuple(self.path), frozenset(self.unvisited)) == (other.current_city, tuple(other.path), frozenset(other.unvisited))

    def __hash__(self):
        return hash((self.current_city, tuple(self.path), frozenset(self.unvisited)))

    def __str__(self):
        return f"City: {self.current_city}, Path: {self.path}, Unvisited: {self.unvisited}"

def is_valid(state: State) -> bool:
    """Check if the state is valid."""
    return len(state.path) <= len(state.unvisited) + len(state.path)

def heuristic(state: State, dist_matrix: np.ndarray) -> float:
    """Estimate remaining cost: sum of min edge costs for unvisited cities plus return."""
    if not state.unvisited:
        # Cost to return to start (city 0)
        return dist_matrix[state.current_city, 0]
    # Sum of minimum edge costs from unvisited cities
    min_edge_sum = 0
    for city in state.unvisited:
        min_edge = min(dist_matrix[city, j] for j in range(len(dist_matrix)) if j != city)
        min_edge_sum += min_edge
    # Add cost to return to start from the last city
    if state.unvisited:
        min_edge_sum += min(dist_matrix[state.current_city, 0], min(dist_matrix[j, 0] for j in state.unvisited))
    return min_edge_sum

def get_successors(state: State, dist_matrix: np.ndarray) -> list:
    """Generate valid successor states by adding one unvisited city."""
    successors = []
    for next_city in state.unvisited:
        new_path = state.path + [next_city]
        new_unvisited = state.unvisited - {next_city}
        edge_cost = dist_matrix[state.current_city, next_city]
        new_state = State(next_city, new_path, new_unvisited, state.g + edge_cost)
        if is_valid(new_state):
            new_state.g = state.g + edge_cost
            new_state.h = heuristic(new_state, dist_matrix)
            new_state.cost = new_state.g + new_state.h
            new_state.parent = state
            successors.append(new_state)
    return successors

def ao_star_tsp(dist_matrix: np.ndarray) -> tuple:
    """
    Solve TSP using AO* algorithm adapted from Missionaries and Cannibals.
    
    Args:
        dist_matrix: NxN numpy array of distances between cities.
    
    Returns:
        Tuple of (optimal tour, total cost).
    """
    n = len(dist_matrix)
    if n <= 1:
        return [0], 0.0

    # Initialize root state (start at city 0)
    initial_state = State(current_city=0, path=[0], unvisited=set(range(1, n)), cost=0.0)
    goal_state = State(current_city=0, path=list(range(n)) + [0], unvisited=set(), cost=float('inf'))

    # Use defaultdict for graph
    graph = defaultdict(list)
    open_list = [initial_state]
    closed = set()

    initial_state.h = heuristic(initial_state, dist_matrix)
    initial_state.cost = initial_state.g + initial_state.h
    graph[initial_state] = []

    while open_list:
        # Select state with lowest cost
        current = min(open_list, key=lambda x: x.cost)
        open_list.remove(current)
        closed.add(current)

        # Check if current state is a complete tour
        if not current.unvisited and dist_matrix[current.current_city, 0] < float('inf'):
            # Complete tour by returning to start
            return_cost = dist_matrix[current.current_city, 0]
            total_cost = current.g + return_cost
            new_path = current.path + [0]
            goal_state = State(current_city=0, path=new_path, unvisited=set(), cost=total_cost)
            goal_state.g = total_cost
            goal_state.h = 0
            goal_state.cost = total_cost
            goal_state.solved = True
            goal_state.parent = current
            graph[current].append(goal_state)
            graph[goal_state] = []
            print("Goal found!")
            return new_path, total_cost

        # Generate successors
        successors = get_successors(current, dist_matrix)
        graph[current] = successors

        for succ in successors:
            if succ not in graph:
                graph[succ] = []
                succ.h = heuristic(succ, dist_matrix)
                succ.cost = succ.g + succ.h
                if succ not in closed and succ not in open_list:
                    open_list.append(succ)

        # Update costs and propagate
        while current:
            if current.solved:
                break
            min_cost = float('inf')
            best_successors = []
            for succ in graph[current]:
                if succ.solved:
                    cost = succ.g
                else:
                    cost = succ.cost
                if cost < min_cost:
                    min_cost = cost
                    best_successors = [succ]
                elif cost == min_cost:
                    best_successors.append(succ)
            
            current.cost = current.g + min_cost
            current.solved = any(succ.solved for succ in best_successors)
            current.children = best_successors

            # Propagate to parent
            if current.parent and current in graph[current.parent]:
                parent = current.parent
                parent_cost = parent.g + min(succ.cost for succ in graph[parent])
                if parent_cost < parent.cost:
                    parent.cost = parent_cost
                    if parent not in open_list and parent not in closed:
                        open_list.append(parent)
                    closed.discard(parent)
            current = current.parent

    print("No solution found.")
    return None, float('inf')

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
    tour, cost = ao_star_tsp(dist_matrix)
    print_solution(tour, cost)