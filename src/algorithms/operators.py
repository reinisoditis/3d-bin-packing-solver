"""
Neighborhood operators for Local Search.
These operators generate neighbor solutions from a current solution.
"""

import random


def swap_items(solution, item1_id, item2_id):
    """
    Swap two items between their bins.
    
    Args:
        solution: Current solution
        item1_id: ID of first item
        item2_id: ID of second item
        
    Returns:
        Solution: New solution with items swapped (or None if not possible)
    """
    # Get items
    item1 = solution.get_item_by_id(item1_id)
    item2 = solution.get_item_by_id(item2_id)
    
    if not item1 or not item2:
        return None
    
    # Both items must be assigned
    if not item1.is_assigned() or not item2.is_assigned():
        return None
    
    # Items must be in different bins
    if item1.assigned_bin == item2.assigned_bin:
        return None
    
    # Create copy of solution
    new_solution = solution.copy()
    
    # Get items and bins in new solution
    new_item1 = new_solution.get_item_by_id(item1_id)
    new_item2 = new_solution.get_item_by_id(item2_id)
    bin1 = new_solution.get_bin_by_id(new_item1.assigned_bin)
    bin2 = new_solution.get_bin_by_id(new_item2.assigned_bin)
    
    # Remove items from their bins
    bin1.remove_item(new_item1)
    bin2.remove_item(new_item2)
    
    # Add items to opposite bins
    bin1.add_item(new_item2)
    bin2.add_item(new_item1)
    
    new_solution.invalidate_fitness()
    return new_solution


def move_item(solution, item_id, target_bin_id):
    """
    Move an item to a different bin.
    
    Args:
        solution: Current solution
        item_id: ID of item to move
        target_bin_id: ID of target bin
        
    Returns:
        Solution: New solution with item moved (or None if not possible)
    """
    # Get item
    item = solution.get_item_by_id(item_id)
    
    if not item or not item.is_assigned():
        return None
    
    # Can't move to same bin
    if item.assigned_bin == target_bin_id:
        return None
    
    # Get target bin
    target_bin = solution.get_bin_by_id(target_bin_id)
    if not target_bin:
        return None
    
    # Create copy of solution
    new_solution = solution.copy()
    
    # Get item and bins in new solution
    new_item = new_solution.get_item_by_id(item_id)
    old_bin = new_solution.get_bin_by_id(new_item.assigned_bin)
    new_bin = new_solution.get_bin_by_id(target_bin_id)
    
    # Remove from old bin and add to new bin
    old_bin.remove_item(new_item)
    new_bin.add_item(new_item)
    
    new_solution.invalidate_fitness()
    return new_solution


def get_random_swap_neighbor(solution):
    """
    Generate a random neighbor by swapping two items.
    
    Args:
        solution: Current solution
        
    Returns:
        Solution: Neighbor solution or None if no swap possible
    """
    # Get all assigned items
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    if len(assigned_items) < 2:
        return None
    
    # Try multiple random swaps
    max_attempts = 50
    for _ in range(max_attempts):
        # Pick two random items
        item1, item2 = random.sample(assigned_items, 2)
        
        # Must be in different bins
        if item1.assigned_bin != item2.assigned_bin:
            neighbor = swap_items(solution, item1.id, item2.id)
            if neighbor:
                return neighbor
    
    return None


def get_random_move_neighbor(solution):
    """
    Generate a random neighbor by moving an item to another bin.
    
    Args:
        solution: Current solution
        
    Returns:
        Solution: Neighbor solution or None if no move possible
    """
    # Get all assigned items
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    if not assigned_items or len(solution.bins) < 2:
        return None
    
    # Try multiple random moves
    max_attempts = 50
    for _ in range(max_attempts):
        # Pick random item
        item = random.choice(assigned_items)
        
        # Pick random target bin (different from current)
        other_bins = [b for b in solution.bins if b.id != item.assigned_bin]
        if not other_bins:
            continue
        
        target_bin = random.choice(other_bins)
        
        neighbor = move_item(solution, item.id, target_bin.id)
        if neighbor:
            return neighbor
    
    return None


def get_all_swap_neighbors(solution):
    """
    Generate all possible swap neighbors.
    
    Args:
        solution: Current solution
        
    Returns:
        list: List of all valid neighbor solutions from swaps
    """
    neighbors = []
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    # Try all pairs of items
    for i in range(len(assigned_items)):
        for j in range(i + 1, len(assigned_items)):
            item1 = assigned_items[i]
            item2 = assigned_items[j]
            
            # Must be in different bins
            if item1.assigned_bin != item2.assigned_bin:
                neighbor = swap_items(solution, item1.id, item2.id)
                if neighbor:
                    neighbors.append(neighbor)
    
    return neighbors


def get_all_move_neighbors(solution):
    """
    Generate all possible move neighbors.
    
    Args:
        solution: Current solution
        
    Returns:
        list: List of all valid neighbor solutions from moves
    """
    neighbors = []
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    # Try moving each item to each other bin
    for item in assigned_items:
        for bin in solution.bins:
            if bin.id != item.assigned_bin:
                neighbor = move_item(solution, item.id, bin.id)
                if neighbor:
                    neighbors.append(neighbor)
    
    return neighbors


def get_random_neighbor(solution):
    """
    Generate a random neighbor using either swap or move (50/50 chance).
    
    Args:
        solution: Current solution
        
    Returns:
        Solution: Random neighbor solution
    """
    if random.random() < 0.5:
        neighbor = get_random_swap_neighbor(solution)
        if neighbor:
            return neighbor
    
    return get_random_move_neighbor(solution)