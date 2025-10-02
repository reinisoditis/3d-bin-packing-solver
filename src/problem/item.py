"""
Item class representing a 3D rectangular box to be packed.
"""

class Item:
    """
    Represents a three-dimensional rectangular item (box).
    
    Attributes:
        id: Unique identifier for the item
        length: Length dimension (x-axis) - garums
        width: Width dimension (y-axis) - platums
        height: Height dimension (z-axis) - augstums
        position: Current position in bin (x, y, z) or None if not placed
        rotation: Current rotation state (0-5 representing different orientations)
    """
    
    def __init__(self, item_id, length, width, height):
        self.id = item_id
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # (x, y, z) tuple when placed
        self.rotation = 0  # 0-5 for different orientations
        
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
            (self.length, self.width, self.height),   # 0: original
            (self.length, self.height, self.width),   # 1: rotate around x
            (self.width, self.length, self.height),   # 2: rotate around z
            (self.width, self.height, self.length),   # 3: rotate around y
            (self.height, self.length, self.width),   # 4: another rotation
            (self.height, self.width, self.length),   # 5: another rotation
        ]
        return rotations[self.rotation]
    
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
    
    def is_placed(self):
        """Check if the item has been placed in a bin."""
        return self.position is not None
    
    def reset(self):
        """Reset the item's placement and rotation."""
        self.position = None
        self.rotation = 0
    
    def __repr__(self):
        """String representation of the item."""
        dims = self.get_dimensions()
        return (f"Item(id={self.id}, dims=({dims[0]}x{dims[1]}x{dims[2]}), "
                f"volume={self.get_volume()}, placed={self.is_placed()})")
    
    def __eq__(self, other):
        """Check equality based on ID."""
        if not isinstance(other, Item):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Make Item hashable for use in sets and dicts."""
        return hash(self.id)