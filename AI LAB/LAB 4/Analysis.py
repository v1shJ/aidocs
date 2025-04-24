import csv
import matplotlib.pyplot as plt

# Read results from CSV
def read_results(filename="hill_climbing_results.csv"):
    hc_data = []
    shc_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            algorithm, start_x, opt_x, max_fx = row
            if algorithm == "Hill Climbing":
                hc_data.append((float(start_x), float(opt_x), float(max_fx)))
            else:
                shc_data.append((float(start_x), float(opt_x), float(max_fx)))
    return hc_data, shc_data

# Compare results
def compare_results(hc_data, shc_data):
    # Compute statistics
    def stats(data, label):
        opt_xs = [d[1] for d in data]
        max_fxs = [d[2] for d in data]
        avg_opt_x = sum(opt_xs) / len(opt_xs)
        avg_max_fx = sum(max_fxs) / len(max_fxs)
        success_rate = sum(1 for fx in max_fxs if fx >= max(max_fxs) - 0.05) / len(max_fxs) * 100
        print(f"{label}:")
        print(f"  Avg Optimal x: {avg_opt_x:.4f}")
        print(f"  Avg Max f(x): {avg_max_fx:.4f}")
        print(f"  Success Rate: {success_rate:.2f}%")
        return avg_max_fx, success_rate

    print("\nComparison of Results:")
    hc_avg_max, hc_success = stats(hc_data, "Hill Climbing")
    shc_avg_max, shc_success = stats(shc_data, "Stochastic Hill Climbing")

    # Determine which is better
    if hc_avg_max > shc_avg_max:
        print("\nHill Climbing performed better in terms of average maximum f(x).")
    else:
        print("\nStochastic Hill Climbing performed better in terms of average maximum f(x).")

    # Visualize results
    plt.figure(figsize=(10, 6))
    plt.hist([d[2] for d in hc_data], bins=20, alpha=0.5, label="Hill Climbing", color="blue")
    plt.hist([d[2] for d in shc_data], bins=20, alpha=0.5, label="Stochastic Hill Climbing", color="orange")
    plt.axvline(16, color="red", linestyle="--", label="True Maximum (16)")
    plt.xlabel("Maximum f(x)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Maximum f(x) Values")
    plt.legend()
    plt.grid(True)
    plt.show()

# Main execution
if __name__ == "__main__":
    hc_data, shc_data = read_results()
    compare_results(hc_data, shc_data)