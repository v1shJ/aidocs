import random
import math
import matplotlib.pyplot as plt
import seaborn as sns

# Define 5 cities with (x, y) coordinates
# cities = [
#     (1, 1),  # City 0: Bottom-left
#     (3, 5),  # City 1: Mid-left, higher
#     (5, 8),  # City 2: Mid-center, top
#     (7, 3),  # City 3: Mid-right, mid
#     (2, 4)   # City 4: Mid-left, mid
# ]
cities = [
    (1, 1), 
    (3, 5), 
    (5, 8), 
    (7, 6), 
    (9, 3), 
    (8, 1), 
    (6, 3), 
    (4, 2), 
    (2, 4), 
    (1, 7)  
]

# Calculate Euclidean distance between two cities
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# Compute total tour distance
def tour_length(tour):
    total = 0
    for i in range(len(tour)):
        total += distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total

# Generate a neighbor by swapping two cities
def get_neighbor(tour):
    new_tour = tour.copy()
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

# Standard Hill Climbing for TSP
def hill_climbing(max_iterations):
    tour = list(range(len(cities)))  # Initial tour: [0, 1, 2, 3, 4]
    random.shuffle(tour)
    best_tour = tour
    best_distance = tour_length(tour)

    for _ in range(max_iterations):
        neighbor = get_neighbor(best_tour)
        neighbor_distance = tour_length(neighbor)
        if neighbor_distance < best_distance:
            best_tour = neighbor
            best_distance = neighbor_distance
        else:
            break  # Stop if no improvement
    return best_tour, best_distance

# Stochastic Hill Climbing for TSP
def stochastic_hill_climbing(max_iterations, T=1.0):
    tour = list(range(len(cities)))  # Initial tour: [0, 1, 2, 3, 4]
    random.shuffle(tour)
    best_tour = tour
    best_distance = tour_length(tour)

    for _ in range(max_iterations):
        neighbor = get_neighbor(best_tour)
        neighbor_distance = tour_length(neighbor)
        delta = neighbor_distance - best_distance  # Positive if worse
        if delta < 0 or random.random() < math.exp(-delta / T):
            best_tour = neighbor
            best_distance = neighbor_distance
    return best_tour, best_distance

# Run multiple experiments
def run_experiments(num_runs, max_iterations):
    hc_results = []
    shc_results = []

    for _ in range(num_runs):
        hc_tour, hc_dist = hill_climbing(max_iterations)
        hc_results.append((hc_tour, hc_dist))
        shc_tour, shc_dist = stochastic_hill_climbing(max_iterations)
        shc_results.append((shc_tour, shc_dist))

    return hc_results, shc_results

# Compute statistics and find the best tour
def compute_stats(results, label):
    distances = [r[1] for r in results]
    avg_distance = sum(distances) / len(distances)
    best_distance = min(distances)
    success_rate = sum(1 for d in distances if d <= best_distance + 0.1) / len(distances) * 100

    # Find the best tour (the one with the minimum distance)
    best_tour = None
    for tour, dist in results:
        if dist == best_distance:
            best_tour = tour
            break

    print(f"\n{label}:")
    print(f"Average Tour Distance: {avg_distance:.4f}")
    print(f"Best Tour Distance: {best_distance:.4f}")
    print(f"Success Rate (within 0.1 of best): {success_rate:.2f}%")
    return distances, best_distance, best_tour

# Plot comparison graphs
def plot_comparison(hc_distances, shc_distances, hc_best_tour, shc_best_tour, best_distance):
    # Plot 1: Histogram of tour distances
    plt.figure(figsize=(10, 6))
    plt.hist(hc_distances, bins=10, alpha=0.5, label="Hill Climbing", color="blue")
    plt.hist(shc_distances, bins=10, alpha=0.5, label="Stochastic Hill Climbing", color="orange")
    plt.axvline(best_distance, color="red", linestyle="--", label=f"Best Distance ({best_distance:.2f})")
    plt.xlabel("Tour Distance")
    plt.ylabel("Frequency")
    plt.title(f"Comparison of HC and SHC for TSP ({len(cities)} Cities) - Histogram")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("tsp_histogram_5_cities.png", format="png", dpi=300)
    plt.close()

    # Plot 2: Boxplot of tour distances
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=[hc_distances, shc_distances], palette=["blue", "orange"])
    plt.xticks([0, 1], ["Hill Climbing", "Stochastic Hill Climbing"])
    plt.ylabel("Tour Distance")
    plt.title(f"Comparison of HC and SHC for TSP ({len(cities)} Cities) - Boxplot")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("tsp_boxplot_5_cities.png", format="png", dpi=300)
    plt.close()

    print("Plots saved as 'tsp_histogram_5_cities.png' and 'tsp_boxplot_5_cities.png' in your current directory.")

# Main execution
if __name__ == "__main__":
    max_iterations = 1000
    num_runs = 20
    print(f"Running {num_runs} runs of Hill Climbing and Stochastic Hill Climbing with {max_iterations} iterations on {len(cities)} cities...")
    hc_results, shc_results = run_experiments(num_runs, max_iterations)
    hc_distances, hc_best_dist, hc_best_tour = compute_stats(hc_results, "Hill Climbing")
    shc_distances, shc_best_dist, shc_best_tour = compute_stats(shc_results, "Stochastic Hill Climbing")

    # Print the best tours
    print("\nBest Tours:")
    print(f"HC Best Tour: {hc_best_tour}, Distance: {hc_best_dist:.4f}")
    print(f"SHC Best Tour: {shc_best_tour}, Distance: {shc_best_dist:.4f}")

    # Plot the comparison
    best_distance = min(hc_best_dist, shc_best_dist)
    plot_comparison(hc_distances, shc_distances, hc_best_tour, shc_best_tour, best_distance)