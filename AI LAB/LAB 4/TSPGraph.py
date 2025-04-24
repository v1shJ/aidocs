import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set(style="whitegrid")  # Clean style with grid
except ImportError:
    plt.style.use('ggplot')
    print("Seaborn not installed. Falling back to 'ggplot' style.")

# Define the 10 cities with (x, y) coordinates
cities = [
    (1, 1),  # City 0: Bottom-left
    (3, 5),  # City 1: Mid-left, higher
    (5, 8),  # City 2: Mid-center, top
    (7, 6),  # City 3: Mid-right, high
    (9, 3),  # City 4: Right, mid
    (8, 1),  # City 5: Right, low
    (6, 3),  # City 6: Mid-right, low
    (4, 2),  # City 7: Mid-center, low
    (2, 4),  # City 8: Mid-left, mid
    (1, 7)   # City 9: Left, high
]

# Calculate Euclidean distance between two cities
def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

# Compute total tour distance
def tour_length(tour):
    total = 0
    for i in range(len(tour)):
        total += distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total

# Sample tour (sequential: 0-1-2-3-4-5-6-7-8-9-0)
tour = list(range(len(cities)))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
tour_length_value = tour_length(tour)

# Extract x and y coordinates
x_coords = [cities[i][0] for i in tour] + [cities[tour[0]][0]]  # Close the loop
y_coords = [cities[i][1] for i in tour] + [cities[tour[0]][1]]  # Close the loop

# Create the plot
plt.figure(figsize=(10, 8))

# Plot the tour path (green line, no arrows)
plt.plot(x_coords, y_coords, 'g-', label="Tour Path", linewidth=2, alpha=0.7)

# Add distance labels between consecutive cities
for i in range(len(tour)):
    city1 = cities[tour[i]]
    city2 = cities[tour[(i + 1) % len(tour)]]
    dist = distance(city1, city2)
    # Calculate midpoint for label placement
    mid_x = (city1[0] + city2[0]) / 2
    mid_y = (city1[1] + city2[1]) / 2
    # Adjust label position slightly to avoid overlap
    offset_x = 0.2 if city1[0] < city2[0] else -0.2
    offset_y = 0.2 if city1[1] < city2[1] else -0.2
    plt.text(mid_x + offset_x, mid_y + offset_y, f"{dist:.2f}", fontsize=8, color='blue')

# Plot cities as red markers
plt.scatter(x_coords[:-1], y_coords[:-1], c='red', s=100, label="Cities", zorder=5)

# Annotate each city with its index
for i, (x, y) in enumerate(cities):
    offset_x = 0.3 if x < 5 else -0.5
    offset_y = 0.3 if y < 5 else -0.5
    plt.text(x + offset_x, y + offset_y, f"City {chr(65+i)}", fontsize=10, fontweight='bold')

# Customize the plot
plt.title(f"TSP City Graph (10 Cities)\nTour Distance: {tour_length_value:.2f}", fontsize=14, pad=20)
plt.xlabel("X Coordinate", fontsize=12)
plt.ylabel("Y Coordinate", fontsize=12)
plt.legend(loc="upper right")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig("tsp_city_graph_distances.png", format="png", dpi=300)
plt.close()

print("Graph with distances saved as 'tsp_city_graph_distances.png' in your current directory.")