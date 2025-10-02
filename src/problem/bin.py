"""
Bin class representing a 3D container (car cargo area / automašīnas kravas kaste).
"""

class Bin:
    """
    Represents a three-dimensional rectangular bin (container/automašīnas kravas kaste).
    
    Attributes:
        id: Unique identifier for the bin
        length: Length dimension (x-axis) - garums
        width: Width dimension (y-axis) - platums  
        height: Height dimension (z-axis) - augstums
        items: List of items currently in this bin
    """
    
    def __init__(self, bin_id, length, width, height):
        self.id = bin_id
        self.length = length
        self.width = width
        self.height = height
        self.items = []
        
    def get_volume(self):
        """Calculate and return the total volume of the bin."""
        return self.length * self.width * self.height
    
    def get_used_volume(self):
        """Calculate the total volume used by items in the bin."""
        return sum(item.get_volume() for item in self.items)
    
    def get_remaining_volume(self):
        """Calculate the remaining available volume."""
        return self.get_volume() - self.get_used_volume()
    
    def get_volume_utilization(self):
        """
        Calculate volume utilization as a percentage.
        
        Returns:
            float: Utilization percentage (0-100)
        """
        if self.get_volume() == 0:
            return 0
        return (self.get_used_volume() / self.get_volume()) * 100
    
    def can_fit_item(self, item):
        """
        Check if an item can potentially fit in the bin (basic check).
        This only checks volume, not actual 3D placement.
        
        Args:
            item: Item object to check
            
        Returns:
            bool: True if item could potentially fit
        """
        # Check volume
        if item.get_volume() > self.get_remaining_volume():
            return False
        
        # Check if any rotation fits within bin dimensions
        for rotation in range(6):
            temp_rotation = item.rotation
            item.set_rotation(rotation)
            dims = item.get_dimensions()
            item.set_rotation(temp_rotation)  # Restore original rotation
            
            if (dims[0] <= self.length and 
                dims[1] <= self.width and 
                dims[2] <= self.height):
                return True
        
        return False
    
    def add_item(self, item):
        """
        Add an item to the bin.
        
        Args:
            item: Item object to add
        """
        if item not in self.items:
            self.items.append(item)
    
    def remove_item(self, item):
        """
        Remove an item from the bin.
        
        Args:
            item: Item object to remove
        """
        if item in self.items:
            self.items.remove(item)
            item.reset()
    
    def clear(self):
        """Remove all items from the bin."""
        for item in self.items:
            item.reset()
        self.items.clear()
    
    def get_item_count(self):
        """Get the number of items in the bin."""
        return len(self.items)
    
    def is_empty(self):
        """Check if the bin is empty."""
        return len(self.items) == 0
    
    def check_overlap(self, item1, item2):
        """
        Check if two items overlap in 3D space.
        
        Args:
            item1: First Item object (must be placed)
            item2: Second Item object (must be placed)
            
        Returns:
            bool: True if items overlap
        """
        if not item1.is_placed() or not item2.is_placed():
            return False
        
        x1, y1, z1 = item1.position
        l1, w1, h1 = item1.get_dimensions()
        
        x2, y2, z2 = item2.position
        l2, w2, h2 = item2.get_dimensions()
        
        # Check for overlap in all three dimensions
        x_overlap = x1 < x2 + l2 and x1 + l1 > x2
        y_overlap = y1 < y2 + w2 and y1 + w1 > y2
        z_overlap = z1 < z2 + h2 and z1 + h1 > z2
        
        return x_overlap and y_overlap and z_overlap
    
    def has_overlaps(self):
        """
        Check if any items in the bin overlap with each other.
        
        Returns:
            bool: True if there are any overlaps
        """
        for i in range(len(self.items)):
            for j in range(i + 1, len(self.items)):
                if self.check_overlap(self.items[i], self.items[j]):
                    return True
        return False
    
    def is_valid_placement(self, item):
        """
        Check if an item's current placement is valid (within bounds and no overlaps).
        
        Args:
            item: Item object to check (must be placed)
            
        Returns:
            bool: True if placement is valid
        """
        if not item.is_placed():
            return False
        
        # Check if within bin boundaries
        x, y, z = item.position
        l, w, h = item.get_dimensions()
        
        if (x < 0 or y < 0 or z < 0 or
            x + l > self.length or
            y + w > self.width or
            z + h > self.height):
            return False
        
        # Check for overlaps with other items
        for other_item in self.items:
            if other_item.id != item.id and self.check_overlap(item, other_item):
                return False
        
        return True
    
    def __repr__(self):
        """String representation of the bin."""
        return (f"Bin(id={self.id}, dims=({self.length}x{self.width}x{self.height}), "
                f"items={self.get_item_count()}, utilization={self.get_volume_utilization():.1f}%)")
    
    def __eq__(self, other):
        """Check equality based on ID."""
        if not isinstance(other, Bin):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Make Bin hashable for use in sets and dicts."""
        return hash(self.id)