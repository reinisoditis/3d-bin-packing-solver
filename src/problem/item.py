"""
Item class representing a 3D rectangular box to be packed.
Full 3D version with positions and rotations.
"""

class Item:
    """
    Represents a three-dimensional rectangular item (box/kaste).
    
    Attributes:
        id: Unique identifier for the item
        length: Length dimension (x-axis) - garums
        width: Width dimension (y-axis) - platums
        height: Height dimension (z-axis) - augstums
        position: Current position in bin (x, y, z) or None if not placed
        rotation: Current rotation state (0-5 representing different orientations)
        assigned_bin: Which bin this item is assigned to (None if unassigned)
    """
    
    def __init__(self, item_id, length, width, height):
        """
        Initialize an Item.
        
        Args:
            item_id: Unique identifier (int or string)
            length: Length of the item (float or int)
            width: Width of the item (float or int)
            height: Height of the item (float or int)
        """
        self.id = item_id
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # (x, y, z) tuple when placed
        self.rotation = 0  # 0-5 for different orientations
        self.assigned_bin = None  # Which bin ID this item is assigned to
        
    def get_volume(self):
        """Calculate and return the volume of the item."""
        return self.length * self.width * self.height
    
    def get_dimensions(self):
        """
        Get current dimensions based on rotation.
        
        Returns:
            tuple: (length, width, height) considering current rotation
        """
        # Rotation mapping (6 possible orientations for a rectangular box)
        rotations = [
            (self.length, self.width, self.height),   # 0: original (LWH)
            (self.length, self.height, self.width),   # 1: rotate around x-axis (LHW)
            (self.width, self.length, self.height),   # 2: rotate around z-axis (WLH)
            (self.width, self.height, self.length),   # 3: (WHL)
            (self.height, self.length, self.width),   # 4: (HLW)
            (self.height, self.width, self.length),   # 5: (HWL)
        ]
        return rotations[self.rotation]
    
    def get_original_dimensions(self):
        """Get original dimensions without rotation."""
        return (self.length, self.width, self.height)
    
    def set_position(self, x, y, z):
        """Set the position of the item in a bin."""
        self.position = (x, y, z)
    
    def set_rotation(self, rotation):
        """
        Set the rotation of the item.
        
        Args:
            rotation: Integer 0-5 representing rotation state
        """
        if 0 <= rotation <= 5:
            self.rotation = rotation
        else:
            raise ValueError("Rotation must be between 0 and 5")
    
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
    
    def is_placed(self):
        """Check if the item has been placed with a position."""
        return self.position is not None
    
    def is_assigned(self):
        """Check if the item has been assigned to a bin."""
        return self.assigned_bin is not None
    
    def reset(self):
        """Reset the item's placement, rotation, and assignment."""
        self.position = None
        self.rotation = 0
        self.assigned_bin = None
    
    def get_bounds(self):
        """
        Get the 3D bounds of the item based on current position and rotation.
        
        Returns:
            tuple: ((x_min, y_min, z_min), (x_max, y_max, z_max))
        """
        if not self.is_placed():
            return None
        
        x, y, z = self.position
        l, w, h = self.get_dimensions()
        
        return ((x, y, z), (x + l, y + w, z + h))
    
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
        for rot in range(6):
            temp_rotation = self.rotation
            self.set_rotation(rot)
            dims = self.get_dimensions()
            self.set_rotation(temp_rotation)  # Restore
            
            if (dims[0] <= bin_length and 
                dims[1] <= bin_width and 
                dims[2] <= bin_height):
                return True
        return False
    
    def copy(self):
        """Create a deep copy of this item."""
        new_item = Item(self.id, self.length, self.width, self.height)
        new_item.rotation = self.rotation
        new_item.position = self.position
        new_item.assigned_bin = self.assigned_bin
        return new_item
    
    def __repr__(self):
        """String representation of the item."""
        dims = self.get_dimensions()
        pos_str = f"pos={self.position}" if self.position else "not placed"
        return (f"Item(id={self.id}, dims={dims}, rot={self.rotation}, "
                f"vol={self.get_volume()}, {pos_str})")
    
    def __eq__(self, other):
        """Check equality based on ID."""
        if not isinstance(other, Item):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Make Item hashable for use in sets and dicts."""
        return hash(self.id)