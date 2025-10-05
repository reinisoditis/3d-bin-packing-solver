"""
Local Search algorithm for 3D Bin Packing Problem.
"""

import time
from .operators import get_all_swap_neighbors, get_all_move_neighbors


class LocalSearch:
    """
    Local Search algorithm implementation.
    
    The algorithm:
    1. Start with an initial solution
    2. Generate all neighbor solutions
    3. If a better neighbor exists, move to it
    4. Repeat until no improvement is found (local optimum)
    
    Attributes:
        max_iterations: Maximum number of iterations
        verbose: Print progress information
    """
    
    def __init__(self, max_iterations=1000, verbose=True):
        """
        Initialize Local Search algorithm.
        
        Args:
            max_iterations: Maximum iterations (default: 1000)
            verbose: Print progress (default: True)
        """
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.history = []  # Track fitness over iterations
        
    def solve(self, initial_solution):
        """
        Run Local Search algorithm.
        
        Args:
            initial_solution: Starting solution
            
        Returns:
            Solution: Best solution found
        """
        start_time = time.time()
        
        current_solution = initial_solution.copy()
        best_solution = current_solution.copy()
        
        if self.verbose:
            print("=" * 70)
            print("Local Search Algorithm")
            print("=" * 70)
            print(f"Initial solution: {current_solution}")
            print(f"Initial fitness: {current_solution.get_fitness():.2f}")
            print()
        
        iteration = 0
        improvements = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # Generate all neighbors
            swap_neighbors = get_all_swap_neighbors(current_solution)
            move_neighbors = get_all_move_neighbors(current_solution)
            from .operators import get_all_rebalance_neighbors
            rebalance_neighbors = get_all_rebalance_neighbors(current_solution)
            all_neighbors = swap_neighbors + move_neighbors + rebalance_neighbors
            
            if not all_neighbors:
                if self.verbose:
                    print(f"Iteration {iteration}: No neighbors generated. Stopping.")
                break
            
            # Find best neighbor
            best_neighbor = min(all_neighbors, key=lambda x: x.get_fitness())
            best_neighbor_fitness = best_neighbor.get_fitness()
            current_fitness = current_solution.get_fitness()
            
            # Track history
            self.history.append(current_fitness)
            
            # If best neighbor is better, move to it
            if best_neighbor_fitness < current_fitness:
                improvement = current_fitness - best_neighbor_fitness
                improvements += 1
                
                current_solution = best_neighbor
                
                # Update best solution
                if best_neighbor_fitness < best_solution.get_fitness():
                    best_solution = best_neighbor.copy()
                
                if self.verbose:
                    print(f"Iteration {iteration}: Improvement found!")
                    print(f"  Current fitness: {current_fitness:.2f} → {best_neighbor_fitness:.2f}")
                    print(f"  Improvement: {improvement:.2f}")
                    print(f"  Neighbors explored: {len(all_neighbors)}")
                    print(f"  Best solution: {best_solution}")
                    print()
            else:
                # No improvement - local optimum reached
                if self.verbose:
                    print(f"Iteration {iteration}: No improvement found (local optimum).")
                    print(f"  Current fitness: {current_fitness:.2f}")
                    print(f"  Best neighbor fitness: {best_neighbor_fitness:.2f}")
                    print(f"  Neighbors explored: {len(all_neighbors)}")
                break
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if self.verbose:
            print()
            print("=" * 70)
            print("Local Search Completed")
            print("=" * 70)
            print(f"Initial fitness: {initial_solution.get_fitness():.2f}")
            print(f"Final fitness: {best_solution.get_fitness():.2f}")
            print(f"Total improvement: {initial_solution.get_fitness() - best_solution.get_fitness():.2f}")
            print(f"Iterations: {iteration}")
            print(f"Improvements found: {improvements}")
            print(f"Time elapsed: {elapsed_time:.2f} seconds")
            print()
            print(f"Best solution: {best_solution}")
            
            stats = best_solution.get_statistics()
            print(f"\nFinal Statistics:")
            print(f"  Bins used: {stats['used_bins']}")
            print(f"  Average utilization: {stats['avg_utilization']:.2f}%")
            print(f"  Unpacked items: {stats['unpacked_items']}")
            print(f"  Is valid: {stats['is_valid']}")
            print("=" * 70)
        
        return best_solution
    
    def get_history(self):
        """
        Get fitness history over iterations.
        
        Returns:
            list: Fitness values at each iteration
        """
        return self.history


class FirstImprovementLocalSearch:
    """
    First Improvement Local Search variant.
    
    Instead of exploring all neighbors and choosing the best,
    this variant moves to the first neighbor that improves the solution.
    This is faster but may find worse local optima.
    """
    
    def __init__(self, max_iterations=1000, verbose=True):
        """
        Initialize First Improvement Local Search.
        
        Args:
            max_iterations: Maximum iterations (default: 1000)
            verbose: Print progress (default: True)
        """
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.history = []
        
    def solve(self, initial_solution):
        """
        Run First Improvement Local Search.
        
        Args:
            initial_solution: Starting solution
            
        Returns:
            Solution: Best solution found
        """
        start_time = time.time()
        
        current_solution = initial_solution.copy()
        best_solution = current_solution.copy()
        
        if self.verbose:
            print("=" * 70)
            print("First Improvement Local Search Algorithm")
            print("=" * 70)
            print(f"Initial solution: {current_solution}")
            print(f"Initial fitness: {current_solution.get_fitness():.2f}")
            print()
        
        iteration = 0
        improvements = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            current_fitness = current_solution.get_fitness()
            
            # Track history
            self.history.append(current_fitness)
            
            # Generate neighbors and check each one
            swap_neighbors = get_all_swap_neighbors(current_solution)
            move_neighbors = get_all_move_neighbors(current_solution)
            all_neighbors = swap_neighbors + move_neighbors
            
            if not all_neighbors:
                if self.verbose:
                    print(f"Iteration {iteration}: No neighbors generated. Stopping.")
                break
            
            # Find first improving neighbor
            improvement_found = False
            for neighbor in all_neighbors:
                neighbor_fitness = neighbor.get_fitness()
                
                if neighbor_fitness < current_fitness:
                    # Found improvement - move immediately
                    improvement = current_fitness - neighbor_fitness
                    improvements += 1
                    improvement_found = True
                    
                    current_solution = neighbor
                    
                    # Update best solution
                    if neighbor_fitness < best_solution.get_fitness():
                        best_solution = neighbor.copy()
                    
                    if self.verbose:
                        print(f"Iteration {iteration}: First improvement found!")
                        print(f"  Current fitness: {current_fitness:.2f} → {neighbor_fitness:.2f}")
                        print(f"  Improvement: {improvement:.2f}")
                        print(f"  Best solution: {best_solution}")
                        print()
                    
                    break
            
            if not improvement_found:
                # No improvement - local optimum reached
                if self.verbose:
                    print(f"Iteration {iteration}: No improvement found (local optimum).")
                    print(f"  Current fitness: {current_fitness:.2f}")
                    print(f"  Neighbors explored: {len(all_neighbors)}")
                break
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if self.verbose:
            print()
            print("=" * 70)
            print("First Improvement Local Search Completed")
            print("=" * 70)
            print(f"Initial fitness: {initial_solution.get_fitness():.2f}")
            print(f"Final fitness: {best_solution.get_fitness():.2f}")
            print(f"Total improvement: {initial_solution.get_fitness() - best_solution.get_fitness():.2f}")
            print(f"Iterations: {iteration}")
            print(f"Improvements found: {improvements}")
            print(f"Time elapsed: {elapsed_time:.2f} seconds")
            print()
            print(f"Best solution: {best_solution}")
            
            stats = best_solution.get_statistics()
            print(f"\nFinal Statistics:")
            print(f"  Bins used: {stats['used_bins']}")
            print(f"  Average utilization: {stats['avg_utilization']:.2f}%")
            print(f"  Unpacked items: {stats['unpacked_items']}")
            print(f"  Is valid: {stats['is_valid']}")
            print("=" * 70)
        
        return best_solution
    
    def get_history(self):
        """Get fitness history."""
        return self.history