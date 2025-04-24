from math import ceil
from collections import defaultdict

class State:
    def __init__(self, m_left, c_left, boat):
        self.m_left = m_left
        self.c_left = c_left
        self.boat = boat  # 0: left bank, 1: right bank
        self.m_right = 3 - m_left
        self.c_right = 3 - c_left
        self.parent = None
        self.children = []
        self.cost = float('inf')  # f = g + h
        self.g = 0  # Cost from root
        self.h = 0  # Heuristic estimate
        self.solved = False
        self.and_node = False

    def __eq__(self, other):
        return (self.m_left, self.c_left, self.boat) == (other.m_left, other.c_left, other.boat)

    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat))

    def __str__(self):
        return f"({self.m_left}, {self.c_left}, {self.boat})"

def is_valid(state):
    """Check if the state is valid (cannibals don't outnumber missionaries)."""
    if state.m_left < 0 or state.c_left < 0 or state.m_right < 0 or state.c_right < 0:
        return False
    if state.m_left > 0 and state.m_left < state.c_left:  # Left bank
        return False
    if state.m_right > 0 and state.m_right < state.c_right:  # Right bank
        return False
    return True

def heuristic(state):
    """Estimate trips needed: ceiling of people on left bank divided by boat capacity (2)."""
    return ceil((state.m_left + state.c_left) / 2)

def get_successors(state):
    """Generate valid successor states based on boat moves."""
    successors = []
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # (missionaries, cannibals)
    if state.boat == 0:  # Boat on left bank
        for m, c in moves:
            if m + c <= 2 and m + c > 0:  # Boat carries 1 or 2 people
                new_state = State(state.m_left - m, state.c_left - c, 1)
                if is_valid(new_state):
                    new_state.g = state.g + 1
                    new_state.h = heuristic(new_state)
                    new_state.cost = new_state.g + new_state.h
                    new_state.parent = state
                    successors.append(new_state)
    else:  # Boat on right bank
        for m, c in moves:
            if m + c <= 2 and m + c > 0:
                new_state = State(state.m_left + m, state.c_left + c, 0)
                if is_valid(new_state):
                    new_state.g = state.g + 1
                    new_state.h = heuristic(new_state)
                    new_state.cost = new_state.g + new_state.h
                    new_state.parent = state
                    successors.append(new_state)
    return successors

def ao_star(initial_state, goal_state):
    """Implement AO* algorithm for Missionaries and Cannibals."""
    graph = {initial_state: []}  # Store AND-OR graph
    open_list = [initial_state]  # Nodes to expand
    closed = set()

    initial_state.h = heuristic(initial_state)
    initial_state.cost = initial_state.g + initial_state.h

    while open_list:
        # Select node with lowest cost
        current = min(open_list, key=lambda x: x.cost)
        open_list.remove(current)
        closed.add(current)

        print(f"Expanding: {current}, Cost: {current.cost} (g={current.g}, h={current.h})")

        if current == goal_state:
            current.solved = True
            print("Goal found!")
            return current, graph

        # Generate successors
        successors = get_successors(current)
        graph[current] = successors

        for succ in successors:
            if succ not in graph:
                graph[succ] = []
                succ.h = heuristic(succ)
                succ.cost = succ.g + succ.h
                if succ not in closed and succ not in open_list:
                    open_list.append(succ)

            # Update if successor is the goal
            if succ == goal_state:
                succ.solved = True
                succ.cost = succ.g

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
    return None, graph

def print_solution(node):
    """Print the solution path from initial to goal state."""
    path = []
    current = node
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    print("\nSolution Path:")
    for i, state in enumerate(path):
        print(f"Step {i}: {state}")
        print(f"Left Bank: {state.m_left}M, {state.c_left}C | Right Bank: {state.m_right}M, {state.c_right}C | Boat: {'Right' if state.boat else 'Left'}")
        print()

# Example usage
if __name__ == "__main__":
    initial_state = State(3, 3, 0)  # 3 missionaries, 3 cannibals, boat on left
    goal_state = State(0, 0, 1)     # All on right bank
    result, graph = ao_star(initial_state, goal_state)
    if result:
        print_solution(result)