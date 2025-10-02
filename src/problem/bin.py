"""
Bin class representing a 3D container.
Simplified version - tracks assigned items without exact positions.
"""

class Bin:
    """
    Represents a three-dimensional rectangular bin.
    
    Attributes:
        id: Unique identifier for the bin
        length: Length dimension (x-axis) - garums
        width: Width dimension (y-axis) - platums  
        height: Height dimension (z-axis) - augstums
        items: List of items currently assigned to this bin
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
        Check if an item can potentially fit in the bin.
        Simple check: volume + dimensions feasibility.
        
        Args:
            item: Item object to check
            
        Returns:
            bool: True if item could potentially fit
        """
        # Check if enough volume remains
        if item.get_volume() > self.get_remaining_volume():
            return False
        
        # Check if item dimensions allow it to fit (any rotation)
        if not item.fits_in_bin(self.length, self.width, self.height):
            return False
        
        return True
    
    def add_item(self, item):
        """
        Add an item to the bin.
        
        Args:
            item: Item object to add
        """
        if item not in self.items:
            self.items.append(item)
            item.assign_to_bin(self.id)
    
    def remove_item(self, item):
        """
        Remove an item from the bin.
        
        Args:
            item: Item object to remove
        """
        if item in self.items:
            self.items.remove(item)
            item.unassign()
    
    def clear(self):
        """Remove all items from the bin."""
        for item in self.items:
            item.unassign()
        self.items.clear()
    
    def get_item_count(self):
        """Get the number of items in the bin."""
        return len(self.items)
    
    def is_empty(self):
        """Check if the bin is empty."""
        return len(self.items) == 0
    
    def is_feasible(self):
        """
        Check if the current bin packing is feasible.
        In simplified version: check if total volume doesn't exceed capacity
        and all items can theoretically fit dimension-wise.
        
        Returns:
            bool: True if bin packing is feasible
        """
        # Check volume constraint
        if self.get_used_volume() > self.get_volume():
            return False
        
        # Check if each item can fit dimension-wise
        for item in self.items:
            if not item.fits_in_bin(self.length, self.width, self.height):
                return False
        
        return True
    
    def get_largest_item_volume(self):
        """Get the volume of the largest item in this bin."""
        if not self.items:
            return 0
        return max(item.get_volume() for item in self.items)
    
    def __repr__(self):
        """String representation of the bin."""
        return (f"Bin(id={self.id}, dims=({self.length}x{self.width}x{self.height}), "
                f"items={self.get_item_count()}, util={self.get_volume_utilization():.1f}%)")
    
    def __eq__(self, other):
        """Check equality based on ID."""
        if not isinstance(other, Bin):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Make Bin hashable for use in sets and dicts."""
        return hash(self.id)