import random
import math
import csv

# Define the objective function
def function(x):
    return -(x - 4) ** 2 + 16

# Standard Hill Climbing
def hill_climbing(start_x, step_size, max_iterations):
    x = start_x
    best_value = function(x)

    for _ in range(max_iterations):
        new_x = x + (step_size if random.choice([True, False]) else -step_size)
        if new_x < 0 or new_x > 8:  # Bounds check
            continue
        new_value = function(new_x)
        if new_value > best_value:
            x = new_x
            best_value = new_value
        else:
            break
    return x, best_value

# Stochastic Hill Climbing
def stochastic_hill_climbing(start_x, step_size, max_iterations):
    x = start_x
    best_value = function(x)
    T = 1.0  # Temperature parameter

    for _ in range(max_iterations):
        new_x = x + (step_size if random.choice([True, False]) else -step_size)
        if new_x < 0 or new_x > 8:  # Bounds check
            continue
        new_value = function(new_x)
        delta = new_value - best_value
        if delta > 0 or random.random() < math.exp(delta / T):
            x = new_x
            best_value = new_value
    return x, best_value

# Run experiments and collect results
def run_experiments(num_runs, step_size, max_iterations):
    hc_results = []
    shc_results = []

    for _ in range(num_runs):
        # Hill Climbing
        start_x = random.uniform(0, 8)
        hc_x, hc_value = hill_climbing(start_x, step_size, max_iterations)
        hc_results.append((start_x, hc_x, hc_value))

        # Stochastic Hill Climbing
        start_x = random.uniform(0, 8)
        shc_x, shc_value = stochastic_hill_climbing(start_x, step_size, max_iterations)
        shc_results.append((start_x, shc_x, shc_value))

    return hc_results, shc_results

# Compute statistics
def compute_stats(results, label):
    optimal_xs = [r[1] for r in results]
    max_values = [r[2] for r in results]
    avg_x = sum(optimal_xs) / len(optimal_xs)
    avg_max = sum(max_values) / len(max_values)
    success_rate = sum(1 for v in max_values if v > 15.99) / len(max_values) * 100  # Within 0.01 of 16

    print(f"\n{label}:")
    print(f"Average Optimal x: {avg_x:.4f}")
    print(f"Average Maximum f(x): {avg_max:.4f}")
    print(f"Success Rate (f(x) > 15.99): {success_rate:.2f}%")
    return avg_x, avg_max, success_rate

# Save results to CSV
def save_results(hc_results, shc_results, filename="hill_climbing_results.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Start X", "Optimal X", "Max f(x)"])
        for start_x, opt_x, max_fx in hc_results:
            writer.writerow(["Hill Climbing", start_x, opt_x, max_fx])
        for start_x, opt_x, max_fx in shc_results:
            writer.writerow(["Stochastic Hill Climbing", start_x, opt_x, max_fx])

# Main execution
if __name__ == "__main__":
    step_size = 0.05
    max_iterations = 5000
    num_runs = 50

    # Run experiments
    hc_results, shc_results = run_experiments(num_runs, step_size, max_iterations)

    # Compute and print statistics
    hc_stats = compute_stats(hc_results, "Hill Climbing")
    shc_stats = compute_stats(shc_results, "Stochastic Hill Climbing")

    # Save results to CSV
    save_results(hc_results, shc_results)
    print(f"\nResults saved to 'hill_climbing_results.csv'")