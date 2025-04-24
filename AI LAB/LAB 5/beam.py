import random

def manhattan_distance(state, goal):
    distance = 0
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            value = state[i][j]
            if state[i][j] != goal[i][j]:
                misplaced += 1
            for x in range(3):
                for y in range(3):
                    if goal[x][y] == value:
                        distance += abs(i - x) + abs(j - y)
    return distance + misplaced  # Weighted combination

def find_blank(state):
    """Find the position of the blank tile (0)."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1

def get_neighbors(state):
    """Generate all possible next states by moving the blank tile."""
    neighbors = []
    blank_i, blank_j = find_blank(state)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    for di, dj in actions:
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row[:] for row in state]  # Deep copy
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            neighbors.append(new_state)
    
    return neighbors

def local_beam_search(initial_state, goal_state, k, max_iterations=1000):
    
    """Perform Local Beam Search to solve the 8-puzzle."""
    beam = [(manhattan_distance(initial_state, goal_state), initial_state)]
    visited = {tuple(map(tuple, initial_state))}
    iterations = 0
    best_state = initial_state
    best_distance = manhattan_distance(initial_state, goal_state)
    best_iteration = 0
    
    print("Initial state:")
    for row in initial_state:
        print(row)
    print(f"Initial Manhattan distance: {best_distance}\n")
    
    while beam and iterations < max_iterations:
        iterations += 1
        next_beam = []
        
        # Generate neighbors for each state in the beam
        for _, state in beam:
            if state == goal_state:
                print("Goal found!")
                for row in state:
                    print(row)
                print(f"Iterations: {iterations}")
                return state, iterations
            
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                neighbor_tuple = tuple(map(tuple, neighbor))
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    distance = manhattan_distance(neighbor, goal_state)
                    next_beam.append((distance, neighbor))
                    if distance < best_distance:
                        best_distance = distance
                        best_state = neighbor
                        best_iteration = iterations
        
        # Select top k states
        def custom_key(item):
            distance, state = item
            misplaced = sum(1 for i in range(3) for j in range(3) if state[i][j] != goal_state[i][j] and state[i][j] != 0)
            return (distance, misplaced)  # Break ties by misplaced tiles

        next_beam.sort()
        beam = next_beam[:k]
        
        print(f"Iteration {iterations}:")
        for distance, state in beam[:min(3, len(beam))]:  # Print top 3 for brevity
            print(f"State (distance={distance}):")
            for row in state:
                print(row)
        
        if not beam:
            print("No more states to explore.")
            break
    
    print("Goal not found.")
    print(f"Best state found (Iteration {best_iteration}):")
    for row in best_state:
        print(row)
    print(f"Best Manhattan distance: {best_distance}")
    return None, iterations

# Example usage with customizable k
if __name__ == "__main__":
    initial_state = [
        [3, 4, 6],
        [1, 0, 8],
        [2, 5, 7]
    ]
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    # Prompt user for beam width
    while True:
        try:
            k = int(input("Enter beam width (k): "))
            if k > 0:
                break
            else:
                print("Beam width must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")
    
    print(f"Running Local Beam Search with k={k}")
    result, iterations = local_beam_search(initial_state, goal_state, k)