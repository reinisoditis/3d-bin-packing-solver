"""
Simulated Annealing algorithm for 3D Bin Packing Problem.
"""

import time
import random
import math
from .operators import get_random_neighbor


class SimulatedAnnealing:
    
    def __init__(self, initial_temp=1000, min_temp=0.1, cooling_rate=0.95, iterations_per_temp=100):
        self.initial_temp = initial_temp
        self.min_temp = min_temp
        self.cooling_rate = cooling_rate
        self.iterations_per_temp = iterations_per_temp
        self.history = []
        self.temperature_history = []
        self.acceptance_history = []
        
    def acceptance_probability(self, current_fitness, neighbor_fitness, temperature):
        if neighbor_fitness < current_fitness:
            return 1.0  # Always accept better solutions
        
        if temperature == 0:
            return 0.0  # Never accept worse solutions at T=0
        
        delta = neighbor_fitness - current_fitness
        probability = math.exp(-delta / temperature)
        return probability
    
    def solve(self, initial_solution):
        start_time = time.time()
        
        current_solution = initial_solution.copy()
        best_solution = current_solution.copy()
        
        temperature = self.initial_temp
        iteration = 0
        total_iterations = 0
        
        accepted_moves = 0
        rejected_moves = 0
        
        # Main loop: while temperature above minimum
        while temperature > self.min_temp:
            iteration += 1
            
            # Iterations at this temperature level
            for _ in range(self.iterations_per_temp):
                total_iterations += 1
                
                # Generate random neighbor
                neighbor = get_random_neighbor(current_solution)
                
                if neighbor is None:
                    continue
                
                # Calculate fitness values
                current_fitness = current_solution.get_fitness()
                neighbor_fitness = neighbor.get_fitness()
                
                # Track history
                self.history.append(current_fitness)
                
                # Calculate acceptance probability
                prob = self.acceptance_probability(current_fitness, neighbor_fitness, temperature)
                
                # Accept or reject
                if random.random() < prob:
                    # Accept neighbor
                    current_solution = neighbor
                    accepted_moves += 1
                    
                    # Update best solution if improved
                    if neighbor_fitness < best_solution.get_fitness():
                        best_solution = neighbor.copy()
                else:
                    rejected_moves += 1
            
            # Track temperature and acceptance rate
            self.temperature_history.append(temperature)
            acceptance_rate = accepted_moves / (accepted_moves + rejected_moves) if (accepted_moves + rejected_moves) > 0 else 0
            self.acceptance_history.append(acceptance_rate)
            
            temperature *= self.cooling_rate
            
            accepted_moves = 0
            rejected_moves = 0
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        return best_solution
    
    def get_history(self):
        return self.history
    
    def get_temperature_history(self):
        return self.temperature_history
    
    def get_acceptance_history(self):
        return self.acceptance_history