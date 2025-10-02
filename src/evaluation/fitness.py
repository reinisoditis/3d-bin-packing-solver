"""
Fitness and evaluation functions for 3D bin packing solutions.
"""


def evaluate_solution(solution):
    """
    Evaluate a solution and return its fitness score.
    Lower score is better.
    
    This is the main objective function that combines:
    1. Primary goal: Minimize number of bins used
    2. Secondary goal: Maximize space utilization
    3. Constraint penalties: Unpacked items, overlaps, invalid placements
    
    Args:
        solution: Solution object to evaluate
        
    Returns:
        float: Fitness score (lower is better)
    """
    return solution.calculate_fitness()


def compare_solutions(solution1, solution2):
    """
    Compare two solutions.
    
    Args:
        solution1: First Solution object
        solution2: Second Solution object
        
    Returns:
        int: -1 if solution1 is better, 1 if solution2 is better, 0 if equal
    """
    fitness1 = solution1.get_fitness()
    fitness2 = solution2.get_fitness()
    
    if fitness1 < fitness2:
        return -1
    elif fitness1 > fitness2:
        return 1
    else:
        return 0


def is_feasible(solution):
    """
    Check if a solution is feasible (satisfies all constraints).
    
    Args:
        solution: Solution object to check
        
    Returns:
        bool: True if solution is feasible
    """
    return solution.is_valid()


def get_constraint_violations(solution):
    """
    Get detailed information about constraint violations.
    
    Args:
        solution: Solution object to analyze
        
    Returns:
        dict: Dictionary with violation counts
    """
    violations = {
        'unpacked_items': len(solution.unpacked_items),
        'overlaps': 0,
        'out_of_bounds': 0,
        'total_violations': 0
    }
    
    for bin in solution.bins:
        if bin.has_overlaps():
            violations['overlaps'] += 1
        
        for item in bin.items:
            if not bin.is_valid_placement(item):
                violations['out_of_bounds'] += 1
    
    violations['total_violations'] = (
        violations['unpacked_items'] + 
        violations['overlaps'] + 
        violations['out_of_bounds']
    )
    
    return violations