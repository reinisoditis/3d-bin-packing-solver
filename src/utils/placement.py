"""
Placement strategies for 3D bin packing.
These algorithms determine WHERE to place items in bins.
"""


def find_best_position_for_item(bin, item):
    """
    Find the best position to place an item in a bin.
    Uses Bottom-Left-Back strategy with all rotation attempts.
    
    Args:
        bin: Bin object to place item in
        item: Item object to place
        
    Returns:
        tuple: (x, y, z, rotation) if position found, None otherwise
    """
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
    """
    Find a valid position for an item with a specific rotation.
    Uses Bottom-Left-Back (BLB) heuristic.
    
    Args:
        bin: Bin object
        item: Item object
        rotation: Rotation to try (0-5)
        
    Returns:
        tuple: (x, y, z) if found, None otherwise
    """
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
    """
    Generate corner points (candidate positions) for placing an item.
    
    Corner points are positions where at least one corner of the item
    touches either a bin wall or another item's surface.
    
    Args:
        bin: Bin object
        item_dims: Dimensions of item to place (l, w, h)
        
    Returns:
        list: List of (x, y, z) candidate positions, sorted by priority
    """
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
    """
    Pack multiple items into a bin using placement heuristic.
    
    Args:
        bin: Bin object to pack into
        items: List of Item objects to pack
        sort_items: Whether to sort items by volume first (default: True)
        
    Returns:
        tuple: (packed_items, unpacked_items)
    """
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


def repack_bin(bin, items=None):
    """
    Repack a bin from scratch (useful for optimization).
    
    Args:
        bin: Bin object to repack
        items: List of items to pack (if None, uses bin's current items)
        
    Returns:
        tuple: (packed_items, unpacked_items)
    """
    if items is None:
        items = bin.items.copy()
    
    # Clear bin
    bin.clear()
    
    # Pack items
    return pack_items_in_bin(bin, items, sort_items=True)