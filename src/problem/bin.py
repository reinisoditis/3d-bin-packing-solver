"""
Bin class representing a 3D container with full geometric placement.
"""

class Bin:
    def __init__(self, bin_id, length, width, height):
        self.id = bin_id
        self.length = length
        self.width = width
        self.height = height
        self.items = []
        
    def get_volume(self):
        return self.length * self.width * self.height
    
    def get_used_volume(self):
        return sum(item.get_volume() for item in self.items)
    
    def get_remaining_volume(self):
        return self.get_volume() - self.get_used_volume()
    
    def get_volume_utilization(self):
        if self.get_volume() == 0:
            return 0
        return (self.get_used_volume() / self.get_volume()) * 100
    
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            item.assign_to_bin(self.id)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            item.reset()
    
    def clear(self):
        for item in self.items:
            item.reset()
        self.items.clear()
    
    def get_item_count(self):
        return len(self.items)
    
    def is_empty(self):
        return len(self.items) == 0
    
    def check_overlap(self, item1, item2):
        if not item1.is_placed() or not item2.is_placed():
            return False
        
        bounds1 = item1.get_bounds()
        bounds2 = item2.get_bounds()
        
        if not bounds1 or not bounds2:
            return False
        
        (x1_min, y1_min, z1_min), (x1_max, y1_max, z1_max) = bounds1
        (x2_min, y2_min, z2_min), (x2_max, y2_max, z2_max) = bounds2
        
        # Check for overlap in all three dimensions
        # Items overlap if they overlap in ALL dimensions
        x_overlap = x1_min < x2_max and x1_max > x2_min
        y_overlap = y1_min < y2_max and y1_max > y2_min
        z_overlap = z1_min < z2_max and z1_max > z2_min
        
        return x_overlap and y_overlap and z_overlap
    
    def has_overlaps(self):
        for i in range(len(self.items)):
            for j in range(i + 1, len(self.items)):
                if self.check_overlap(self.items[i], self.items[j]):
                    return True
        return False
    
    def is_within_bounds(self, item):
        if not item.is_placed():
            return False
        
        bounds = item.get_bounds()
        if not bounds:
            return False
        
        (x_min, y_min, z_min), (x_max, y_max, z_max) = bounds
        
        return (x_min >= 0 and y_min >= 0 and z_min >= 0 and
                x_max <= self.length and
                y_max <= self.width and
                z_max <= self.height)
    
    def is_valid_placement(self, item):
        if not item.is_placed():
            return False
        
        # Check if within bin boundaries
        if not self.is_within_bounds(item):
            return False
        
        # Check for overlaps with other items
        for other_item in self.items:
            if other_item.id != item.id and self.check_overlap(item, other_item):
                return False
        
        return True
    
    def is_feasible(self):
        # Check if all items are placed with valid positions
        for item in self.items:
            if not item.is_placed():
                return False
            if not self.is_within_bounds(item):
                return False
        
        # Check for overlaps
        if self.has_overlaps():
            return False
        
        return True
    
    def can_fit_item_at_position(self, item, x, y, z, rotation=None):
        # Temporarily set position and rotation
        old_pos = item.position
        old_rot = item.rotation
        
        if rotation is not None:
            item.set_rotation(rotation)
        item.set_position(x, y, z)
        
        # Check if valid
        valid = (self.is_within_bounds(item) and 
                not any(self.check_overlap(item, other) 
                       for other in self.items if other.id != item.id))
        
        # Restore original state
        item.position = old_pos
        item.rotation = old_rot
        
        return valid
    
    def get_occupied_space(self):
        return [item.get_bounds() for item in self.items if item.is_placed()]
    
    def __repr__(self):
        return (f"Bin(id={self.id}, dims=({self.length}x{self.width}x{self.height}), "
                f"items={self.get_item_count()}, util={self.get_volume_utilization():.1f}%)")
    
    def __eq__(self, other):
        if not isinstance(other, Bin):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)