"""
Fitness and evaluation functions for 3D bin packing solutions.
"""

def evaluate_solution(solution):
    """
    This is the main objective function that combines:
    1. Primary goal: Minimize number of bins used
    2. Secondary goal: Maximize space utilization
    3. Constraint penalties: Unpacked items, overlaps, invalid placements
    """
    return solution.calculate_fitness()