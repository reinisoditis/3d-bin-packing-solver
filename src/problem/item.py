"""
Item class representing a 3D rectangular box to be packed.
Simplified version - focuses on assignment to bins, not exact positions.
"""

class Item:
    """
    Represents a three-dimensional rectangular item.
    
    Attributes:
        id: Unique identifier for the item
        length: Length dimension (x-axis) - garums
        width: Width dimension (y-axis) - platums
        height: Height dimension (z-axis) - augstums
        assigned_bin: Which bin this item is assigned to (None if unassigned)
    """
    
    def __init__(self, item_id, length, width, height):
        self.id = item_id
        self.length = length
        self.width = width
        self.height = height
        self.assigned_bin = None  # Which bin ID this item is assigned to
        
    def get_volume(self):
        """Calculate and return the volume of the item."""
        return self.length * self.width * self.height
    
    def get_dimensions(self):
        """
        Get dimensions as tuple.
        
        Returns:
            tuple: (length, width, height)
        """
        return (self.length, self.width, self.height)
    
    def assign_to_bin(self, bin_id):
        """
        Assign this item to a bin.
        
        Args:
            bin_id: ID of the bin to assign to
        """
        self.assigned_bin = bin_id
    
    def unassign(self):
        """Remove assignment from bin."""
        self.assigned_bin = None
    
    def is_assigned(self):
        """Check if the item has been assigned to a bin."""
        return self.assigned_bin is not None
    
    def fits_in_bin(self, bin_length, bin_width, bin_height):
        """
        Check if item can fit in a bin with given dimensions.
        Checks all possible rotations.
        
        Args:
            bin_length: Bin length
            bin_width: Bin width  
            bin_height: Bin height
            
        Returns:
            bool: True if item fits in at least one orientation
        """
        # Check all 6 possible orientations
        orientations = [
            (self.length, self.width, self.height),
            (self.length, self.height, self.width),
            (self.width, self.length, self.height),
            (self.width, self.height, self.length),
            (self.height, self.length, self.width),
            (self.height, self.width, self.length),
        ]
        
        for l, w, h in orientations:
            if l <= bin_length and w <= bin_width and h <= bin_height:
                return True
        return False
    
    def __repr__(self):
        """String representation of the item."""
        return (f"Item(id={self.id}, dims=({self.length}x{self.width}x{self.height}), "
                f"vol={self.get_volume()}, bin={self.assigned_bin})")
    
    def __eq__(self, other):
        """Check equality based on ID."""
        if not isinstance(other, Item):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Make Item hashable for use in sets and dicts."""
        return hash(self.id)