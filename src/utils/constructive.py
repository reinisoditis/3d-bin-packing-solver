"""
Constructive heuristic for generating initial solutions with 3D placement.
"""

from src.problem import Solution, Bin
from .placement import find_best_position_for_item


def first_fit_decreasing(bin_dimensions, items):
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
            # Try to find a valid position for this item
            result = find_best_position_for_item(bin, item)
            
            if result:
                x, y, z, rotation = result
                # Place the item
                item.set_rotation(rotation)
                item.set_position(x, y, z)
                bin.add_item(item)
                placed = True
                break
        
        # If doesn't fit anywhere, create new bin
        if not placed:
            new_bin = solution.add_bin()
            result = find_best_position_for_item(new_bin, item)
            
            if result:
                x, y, z, rotation = result
                item.set_rotation(rotation)
                item.set_position(x, y, z)
                new_bin.add_item(item)
            else:
                print(f"WARNING: Item {item.id} doesn't fit in bin!")
    
    solution.invalidate_fitness()
    return solution