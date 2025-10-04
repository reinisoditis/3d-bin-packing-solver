from src.problem import Solution


def first_fit_decreasing(bin_dimensions, items):
    """
    First Fit Decreasing (FFD) heuristic.
    
    Algorithm:
    1. Sort items by volume in descending order (largest first)
    2. For each item, try to fit it in the first bin where it fits
    3. If it doesn't fit in any bin, create a new bin
    
    Args:
        bin_dimensions: Tuple (length, width, height) for bins
        items: List of Item objects to pack
        
    Returns:
        Solution: Initial solution created by FFD
    """
    # Create solution
    solution = Solution(bin_dimensions, items)
    
    # Sort items by volume (largest first)
    sorted_items = sorted(solution.all_items, 
                         key=lambda x: x.get_volume(), 
                         reverse=True)
    
    # Pack each item
    for item in sorted_items:
        placed = False
        
        # Try to fit in existing bins
        for bin in solution.bins:
            if bin.can_fit_item(item):
                bin.add_item(item)
                placed = True
                break
        
        # If doesn't fit anywhere, create new bin
        if not placed:
            new_bin = solution.add_bin()
            new_bin.add_item(item)
    
    solution.invalidate_fitness()
    return solution