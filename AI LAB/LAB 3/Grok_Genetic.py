import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)

# Genetic Algorithm for Knapsack Problem
def genetic_algorithm_knapsack(weights, values, capacity, pop_size=10, num_generations=100):
    num_items = len(weights)
    
    # Initialize random population (binary strings where 1 = item selected, 0 = not selected)
    population = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(pop_size)]
    
    # Main evolution loop
    for generation in range(num_generations):
        # Calculate fitness for each chromosome
        fitness = []
        for chromosome in population:
            total_weight = sum(w * c for w, c in zip(weights, chromosome))
            total_value = sum(v * c for v, c in zip(values, chromosome))
            # Fitness is total value if within capacity, else 0
            fitness.append(total_value if total_weight <= capacity else 0)
        
        # Find the best chromosome for elitism
        best_idx = np.argmax(fitness)
        best_chromosome = population[best_idx]
        
        # Create new population
        new_population = []
        
        # Selection: Roulette wheel selection (proportional to fitness)
        total_fitness = sum(fitness) if sum(fitness) > 0 else 1  # Avoid division by zero
        probabilities = [f / total_fitness for f in fitness]
        
        while len(new_population) < pop_size - 1:  # Leave space for elitism
            # Select two parents
            if total_fitness == 0:  # If all fitnesses are 0, choose randomly
                parent1 = random.choice(population)
                parent2 = random.choice(population)
            else:
                parent1 = random.choices(population, weights=probabilities)[0]
                parent2 = random.choices(population, weights=probabilities)[0]
            
            # Crossover (80% probability)
            if random.random() < 0.8:
                crossover_point = random.randint(1, num_items - 1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
            else:
                child1, child2 = parent1[:], parent2[:]
            
            # Mutation (1% chance per gene)
            for i in range(num_items):
                if random.random() < 0.01:
                    child1[i] = 1 - child1[i]  # Flip bit
                if random.random() < 0.01:
                    child2[i] = 1 - child2[i]
            
            new_population.extend([child1, child2])
        
        # Trim to population size - 1 (to add best chromosome)
        new_population = new_population[:pop_size - 1]
        # Elitism: Add the best chromosome from the previous generation
        new_population.append(best_chromosome)
        population = new_population
    
    # Final fitness calculation to find the best solution
    fitness = []
    for chromosome in population:
        total_weight = sum(w * c for w, c in zip(weights, chromosome))
        total_value = sum(v * c for v, c in zip(values, chromosome))
        fitness.append(total_value if total_weight <= capacity else 0)
    
    best_idx = np.argmax(fitness)
    best_chromosome = population[best_idx]
    total_weight = sum(w * c for w, c in zip(weights, best_chromosome))
    total_value = sum(v * c for v, c in zip(values, best_chromosome))
    
    # Decode selected items
    selected_items = [i for i, val in enumerate(best_chromosome) if val == 1]
    
    return selected_items, total_value, total_weight

# Greedy Heuristic for Knapsack Problem
def greedy_knapsack(weights, values, capacity):
    num_items = len(weights)
    # Calculate value-to-weight ratio for each item
    ratios = [(v / w, w, v, i) for i, (w, v) in enumerate(zip(weights, values))]
    # Sort by ratio in descending order
    ratios.sort(reverse=True)
    
    total_weight = 0
    total_value = 0
    selected_items = []
    
    # Select items greedily
    for ratio, weight, value, idx in ratios:
        if total_weight + weight <= capacity:
            total_weight += weight
            total_value += value
            selected_items.append(idx)
    
    return sorted(selected_items), total_value, total_weight

# Example usage
weights = [2, 3, 4, 5, 6]  # Weights of items
values = [3, 4, 5, 8, 9]   # Values of items
capacity = 10              # Knapsack capacity

# Run Genetic Algorithm
ga_items, ga_value, ga_weight = genetic_algorithm_knapsack(weights, values, capacity)
print("Genetic Algorithm:")
print(f"Selected items (indices): {ga_items}")
print(f"Total value: {ga_value}")
print(f"Total weight: {ga_weight}")

# Run Greedy Heuristic
greedy_items, greedy_value, greedy_weight = greedy_knapsack(weights, values, capacity)
print("\nGreedy Heuristic:")
print(f"Selected items (indices): {greedy_items}")
print(f"Total value: {greedy_value}")
print(f"Total weight: {greedy_weight}")