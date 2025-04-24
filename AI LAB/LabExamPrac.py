class BFS:
    def __init__(self, graph):
        self.graph = graph
    
    def bfs(self, start, goal):
        visited = set()
        queue = [(start, [start])]

        while queue:
            current_node, path = queue.pop(0)
            if current_node == goal:
                return path
            visited.add(current_node)
            for neighbor in self.graph.get(current_node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None

    def dfs(self, start, goal):
        visited = set()
        st = [(start, [start])]

        while st:
            current_node, path = st.pop()
            if current_node == goal:
                return path
            visited.add(current_node)
            for neighbor in self.graph.get(current_node, []):
                if neighbor not in visited:
                    st.append((neighbor, path + [neighbor]))
        return None
                  
    
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    bfs = BFS(graph)
    start_node = 'A'
    goal_node = 'E'
    path = bfs.bfs(start_node, goal_node)
    # path = bfs.dfs(start_node, goal_node)
    if path:
        print(f"Path from {start_node} to {goal_node}: {' -> '.join(path)}")
    else:
        print(f"No path found from {start_node} to {goal_node}.")