def gbfs(start, goal):
    graph = {
        'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
        'Zerind': [('Arad', 75), ('Oradea', 71)],
        'Oradea': [('Zerind', 71), ('Sibiu', 151)],
        'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
        'Timisoara': [('Arad', 118), ('Lugoj', 111)],
        'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
        'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
        'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
        'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
        'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
        'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
        'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
        'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
        'Giurgiu': [('Bucharest', 90)],
        'Urziceni': [('Bucharest', 85), ('Vaslui', 142), ('Hirsova', 98)],
        'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
        'Eforie': [('Hirsova', 86)],
        'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
        'Iasi': [('Vaslui', 92), ('Neamt', 87)],
        'Neamt': [('Iasi', 87)]
    }

    # Heuristic: Straight-line distance to Bucharest (in km)
    heuristic = {
        'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
        'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
        'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
        'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
    }
    heuristic = {
        'Arad': 71, 'Bucharest': 450, 'Craiova': 300, 'Drobeta': 250, 'Eforie': 500,
        'Fagaras': 200, 'Giurgiu': 460, 'Hirsova': 470, 'Iasi': 350, 'Lugoj': 150,
        'Mehadia': 200, 'Neamt': 300, 'Oradea': 0, 'Pitesti': 350, 'Rimnicu Vilcea': 250,
        'Sibiu': 151, 'Timisoara': 100, 'Urziceni': 400, 'Vaslui': 380, 'Zerind': 10
    }

    visited = set()
    path = [start]
    distance = 0
    current = start

    while current != goal:
        visited.add(current)
        neighbors = [(neighbor, cost) for neighbor, cost in graph[current] if neighbor not in visited]
        if not neighbors:
            print(current)
            return 0, []
        
        # Sort neighbors by heuristic value
        next_node, cost = min(neighbors, key=lambda x: heuristic[x[0]])
        path.append(next_node)
        distance += cost
        current = next_node

    return distance, path

if __name__ == "__main__":
    start_city = 'Arad'
    goal_city = 'Oradea'
    distance, path = gbfs(start_city, goal_city)
    if distance:
        print(path)
    else:
        print("No path found.")