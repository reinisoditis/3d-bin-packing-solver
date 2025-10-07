"""
Item class representing a 3D rectangular box to be packed.
Full 3D version with positions and rotations.
"""

class Item:
    def __init__(self, item_id, length, width, height):
        self.id = item_id
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # (x, y, z) tuple when placed
        self.rotation = 0  # 0-5 for different orientations
        self.assigned_bin = None  # Which bin ID this item is assigned to
        
    def get_volume(self):
        return self.length * self.width * self.height
    
    def get_dimensions(self):
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
        return (self.length, self.width, self.height)
    
    def set_position(self, x, y, z):
        self.position = (x, y, z)
    
    def set_rotation(self, rotation):
        if 0 <= rotation <= 5:
            self.rotation = rotation
        else:
            raise ValueError("Rotation must be between 0 and 5")
    
    def assign_to_bin(self, bin_id):
        self.assigned_bin = bin_id
    
    def unassign(self):
        self.assigned_bin = None
    
    def is_placed(self):
        return self.position is not None
    
    def is_assigned(self):
        return self.assigned_bin is not None
    
    def reset(self):
        self.position = None
        self.rotation = 0
        self.assigned_bin = None
    
    def get_bounds(self):
        if not self.is_placed():
            return None
        
        x, y, z = self.position
        l, w, h = self.get_dimensions()
        
        return ((x, y, z), (x + l, y + w, z + h))
    
    def fits_in_bin(self, bin_length, bin_width, bin_height):
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
        new_item = Item(self.id, self.length, self.width, self.height)
        new_item.rotation = self.rotation
        new_item.position = self.position
        new_item.assigned_bin = self.assigned_bin
        return new_item
    
    def __repr__(self):
        dims = self.get_dimensions()
        pos_str = f"pos={self.position}" if self.position else "not placed"
        return (f"Item(id={self.id}, dims={dims}, rot={self.rotation}, "
                f"vol={self.get_volume()}, {pos_str})")
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)