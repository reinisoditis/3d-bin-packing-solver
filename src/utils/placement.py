"""
Placement strategies for 3D bin packing.
These algorithms determine WHERE to place items in bins.
"""


def find_best_position_for_item(bin, item):
    best_position = None
    best_height = float('inf')
    
    # Try all 6 rotations
    for rotation in range(6):
        result = find_position_with_rotation(bin, item, rotation)
        if result:
            x, y, z = result
            # Prefer lower positions (bottom-first strategy)
            if z < best_height:
                best_height = z
                best_position = (x, y, z, rotation)
    
    return best_position


def find_position_with_rotation(bin, item, rotation):
     # Set rotation temporarily
    old_rotation = item.rotation
    item.set_rotation(rotation)
    item_dims = item.get_dimensions()
    
    # Generate candidate positions (corner points)
    candidates = generate_corner_points(bin, item_dims)
    
    # Try each candidate position
    for x, y, z in candidates:
        if bin.can_fit_item_at_position(item, x, y, z, rotation):
            # Found valid position
            item.set_rotation(old_rotation)  # Restore
            return (x, y, z)
    
    # No valid position found
    item.set_rotation(old_rotation)  # Restore
    return None


def generate_corner_points(bin, item_dims):
    item_l, item_w, item_h = item_dims
    
    # Start with origin point
    candidates = [(0, 0, 0)]
    
    # If bin is empty, only origin is valid
    if bin.is_empty():
        return candidates
    
    # Generate corner points based on existing items
    for placed_item in bin.items:
        if not placed_item.is_placed():
            continue
            
        bounds = placed_item.get_bounds()
        if not bounds:
            continue
            
        (x_min, y_min, z_min), (x_max, y_max, z_max) = bounds
        
        # Generate potential positions around this item
        # Right side (x-direction)
        candidates.append((x_max, y_min, z_min))
        # Back side (y-direction)
        candidates.append((x_min, y_max, z_min))
        # Top side (z-direction)
        candidates.append((x_min, y_min, z_max))
        
        # Corner points
        candidates.append((x_max, y_max, z_min))
        candidates.append((x_max, y_min, z_max))
        candidates.append((x_min, y_max, z_max))
        candidates.append((x_max, y_max, z_max))
    
    # Remove duplicates
    candidates = list(set(candidates))
    
    # Filter out positions where item would exceed bin bounds
    valid_candidates = []
    for x, y, z in candidates:
        if (x + item_l <= bin.length and
            y + item_w <= bin.width and
            z + item_h <= bin.height):
            valid_candidates.append((x, y, z))
    
    # Sort by priority: bottom-left-back
    # Priority: z (height) first, then x (length), then y (width)
    valid_candidates.sort(key=lambda pos: (pos[2], pos[0], pos[1]))
    
    return valid_candidates


def pack_items_in_bin(bin, items, sort_items=True):
    # Sort items by volume (largest first) if requested
    items_to_pack = sorted(items, key=lambda x: x.get_volume(), reverse=True) if sort_items else items.copy()
    
    packed = []
    unpacked = []
    
    for item in items_to_pack:
        # Find best position for this item
        result = find_best_position_for_item(bin, item)
        
        if result:
            x, y, z, rotation = result
            # Place the item
            item.set_rotation(rotation)
            item.set_position(x, y, z)
            bin.add_item(item)
            packed.append(item)
        else:
            # Could not place item
            unpacked.append(item)
    
    return packed, unpacked