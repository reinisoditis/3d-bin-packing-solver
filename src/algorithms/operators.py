"""
Neighborhood operators for Local Search with 3D placement.
More flexible approach - allows partial repacking failures.
"""

import random
from src.utils.placement import pack_items_in_bin


def swap_items(solution, item1_id, item2_id):
    item1 = solution.get_item_by_id(item1_id)
    item2 = solution.get_item_by_id(item2_id)
    
    if not item1 or not item2:
        return None
    
    if not item1.is_assigned() or not item2.is_assigned():
        return None
    
    if item1.assigned_bin == item2.assigned_bin:
        return None
    
    new_solution = solution.copy()
    new_item1 = new_solution.get_item_by_id(item1_id)
    new_item2 = new_solution.get_item_by_id(item2_id)
    bin1 = new_solution.get_bin_by_id(new_item1.assigned_bin)
    bin2 = new_solution.get_bin_by_id(new_item2.assigned_bin)
    
    items_bin1 = [item for item in bin1.items if item.id != new_item1.id]
    items_bin2 = [item for item in bin2.items if item.id != new_item2.id]
    
    items_bin1.append(new_item2)
    items_bin2.append(new_item1)
    
    bin1.clear()
    bin2.clear()
    
    packed1, unpacked1 = pack_items_in_bin(bin1, items_bin1, sort_items=True)
    packed2, unpacked2 = pack_items_in_bin(bin2, items_bin2, sort_items=True)
    
    if (new_item1 in unpacked2 and new_item2 in unpacked1):
        return None
    
    new_solution.invalidate_fitness()
    return new_solution


def move_item(solution, item_id, target_bin_id):
    item = solution.get_item_by_id(item_id)
    
    if not item or not item.is_assigned():
        return None
    
    if item.assigned_bin == target_bin_id:
        return None
    
    target_bin = solution.get_bin_by_id(target_bin_id)
    if not target_bin:
        return None
    
    new_solution = solution.copy()
    new_item = new_solution.get_item_by_id(item_id)
    old_bin = new_solution.get_bin_by_id(new_item.assigned_bin)
    new_bin = new_solution.get_bin_by_id(target_bin_id)
    
    old_bin_items = [item for item in old_bin.items if item.id != new_item.id]
    new_bin_items = list(new_bin.items)
    new_bin_items.append(new_item)
    
    old_bin.clear()
    new_bin.clear()
    
    packed_old, unpacked_old = pack_items_in_bin(old_bin, old_bin_items, sort_items=True)
    packed_new, unpacked_new = pack_items_in_bin(new_bin, new_bin_items, sort_items=True)
    
    if new_item in unpacked_new:
        return None
    
    new_solution.invalidate_fitness()
    return new_solution


def merge_bins_aggressive(solution, bin1_id, bin2_id):
    bin1 = solution.get_bin_by_id(bin1_id)
    bin2 = solution.get_bin_by_id(bin2_id)
    
    if not bin1 or not bin2 or bin1.id == bin2.id:
        return None
    
    # Don't try if clearly impossible
    total_volume = bin1.get_used_volume() + bin2.get_used_volume()
    if total_volume > bin1.get_volume() * 1.5:  # Allow some overage
        return None
    
    new_solution = solution.copy()
    new_bin1 = new_solution.get_bin_by_id(bin1_id)
    new_bin2 = new_solution.get_bin_by_id(bin2_id)
    
    # Get all items
    all_items = list(new_bin1.items) + list(new_bin2.items)
    
    # Clear both bins
    new_bin1.clear()
    new_bin2.clear()
    
    # Try to pack all into bin1
    packed, unpacked = pack_items_in_bin(new_bin1, all_items, sort_items=True)
    
    # If managed to pack everything - success!
    if not unpacked:
        new_solution.invalidate_fitness()
        return new_solution
    
    # If most items fit (>80%), accept it
    # Unpacked items heavily penalized by fitness
    if len(packed) >= len(all_items) * 0.8:
        new_solution.invalidate_fitness()
        return new_solution
    return None


def consolidate_small_bins(solution):
    used_bins = solution.get_used_bins()
    
    if len(used_bins) < 2:
        return None
    
    # Find bin with lowest utilization
    bins_by_util = sorted(used_bins, key=lambda b: b.get_volume_utilization())
    smallest_bin = bins_by_util[0]
    
    # Don't bother if already well-utilized
    if smallest_bin.get_volume_utilization() > 60:
        return None
    
    new_solution = solution.copy()
    new_smallest = new_solution.get_bin_by_id(smallest_bin.id)
    
    items_to_relocate = list(new_smallest.items)
    new_smallest.clear()
    
    # Try to distribute items to other bins
    for item in items_to_relocate:
        placed = False
        for bin in new_solution.bins:
            if bin.id != new_smallest.id and not bin.is_empty():
                # Try to add item
                test_items = list(bin.items) + [item]
                bin.clear()
                packed, unpacked = pack_items_in_bin(bin, test_items, sort_items=True)
                
                if item in packed:  # Successfully placed
                    placed = True
                    break
        
        # If couldn't place, put back (will be penalized)
        if not placed:
            new_smallest.add_item(item)
    
    # If managed to empty the bin, great!
    if new_smallest.is_empty():
        new_solution.invalidate_fitness()
        return new_solution
    
    # If reduced items significantly, accept
    if len(new_smallest.items) < len(smallest_bin.items) * 0.5:
        new_solution.invalidate_fitness()
        return new_solution
    
    return None


def get_random_merge_neighbor(solution):
    if len(solution.bins) < 2:
        return None
    
    for _ in range(10):
        bin1, bin2 = random.sample(solution.bins, 2)
        neighbor = merge_bins_aggressive(solution, bin1.id, bin2.id)
        if neighbor:
            return neighbor
    
    return None


def get_random_consolidate_neighbor(solution):
    return consolidate_small_bins(solution)


def rebalance_bins(solution, bin1_id, bin2_id):
    bin1 = solution.get_bin_by_id(bin1_id)
    bin2 = solution.get_bin_by_id(bin2_id)
    
    if not bin1 or not bin2:
        return None
    
    util1 = bin1.get_volume_utilization()
    util2 = bin2.get_volume_utilization()
    
    if abs(util1 - util2) < 20:
        return None
    
    new_solution = solution.copy()
    new_bin1 = new_solution.get_bin_by_id(bin1_id)
    new_bin2 = new_solution.get_bin_by_id(bin2_id)
    
    all_items = list(new_bin1.items) + list(new_bin2.items)
    
    new_bin1.clear()
    new_bin2.clear()
    
    packed1, unpacked1 = pack_items_in_bin(new_bin1, all_items, sort_items=True)
    
    if unpacked1:
        packed2, unpacked2 = pack_items_in_bin(new_bin2, unpacked1, sort_items=True)
    
    new_solution.invalidate_fitness()
    return new_solution


def get_random_swap_neighbor(solution):
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    if len(assigned_items) < 2:
        return None
    
    max_attempts = 50
    for _ in range(max_attempts):
        item1, item2 = random.sample(assigned_items, 2)
        
        if item1.assigned_bin != item2.assigned_bin:
            neighbor = swap_items(solution, item1.id, item2.id)
            if neighbor:
                return neighbor
    
    return None


def get_random_move_neighbor(solution):
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    if not assigned_items or len(solution.bins) < 2:
        return None
    
    max_attempts = 50
    for _ in range(max_attempts):
        item = random.choice(assigned_items)
        other_bins = [b for b in solution.bins if b.id != item.assigned_bin]
        if not other_bins:
            continue
        
        target_bin = random.choice(other_bins)
        neighbor = move_item(solution, item.id, target_bin.id)
        if neighbor:
            return neighbor
    
    return None


def get_random_rebalance_neighbor(solution):
    if len(solution.bins) < 2:
        return None
    
    bin1, bin2 = random.sample(solution.bins, 2)
    return rebalance_bins(solution, bin1.id, bin2.id)


def get_all_swap_neighbors(solution):
    neighbors = []
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    for i in range(len(assigned_items)):
        for j in range(i + 1, len(assigned_items)):
            item1 = assigned_items[i]
            item2 = assigned_items[j]
            
            if item1.assigned_bin != item2.assigned_bin:
                neighbor = swap_items(solution, item1.id, item2.id)
                if neighbor:
                    neighbors.append(neighbor)
    
    return neighbors


def get_all_move_neighbors(solution):
    neighbors = []
    assigned_items = [item for item in solution.all_items if item.is_assigned()]
    
    for item in assigned_items:
        for bin in solution.bins:
            if bin.id != item.assigned_bin:
                neighbor = move_item(solution, item.id, bin.id)
                if neighbor:
                    neighbors.append(neighbor)
    
    return neighbors


def get_all_rebalance_neighbors(solution):
    neighbors = []
    
    for i in range(len(solution.bins)):
        for j in range(i + 1, len(solution.bins)):
            neighbor = rebalance_bins(solution, i, j)
            if neighbor:
                neighbors.append(neighbor)
    
    return neighbors


def get_random_neighbor(solution):
    choice = random.random()
    
    if choice < 0.25:  # 25% merge - IMPORTANT for bin reduction!
        neighbor = get_random_merge_neighbor(solution)
        if neighbor:
            return neighbor
    elif choice < 0.40:  # 15% consolidate
        neighbor = get_random_consolidate_neighbor(solution)
        if neighbor:
            return neighbor
    elif choice < 0.60:  # 20% swap
        neighbor = get_random_swap_neighbor(solution)
        if neighbor:
            return neighbor
    elif choice < 0.80:  # 20% move
        neighbor = get_random_move_neighbor(solution)
        if neighbor:
            return neighbor
    
    # 20% rebalance
    return get_random_rebalance_neighbor(solution)