"""
Solution class representing a complete bin packing solution.
"""

import copy
from .bin import Bin
from .item import Item


class Solution:
    """
    Represents a complete solution to the 3D bin packing problem.
    
    A solution consists of:
    - A list of bins with items packed in them
    - Assignment of all items to bins
    - Fitness/cost value
    
    Attributes:
        bins: List of Bin objects used in this solution
        bin_dimensions: Tuple (length, width, height) for creating new bins
        all_items: List of all items that need to be packed
        unpacked_items: List of items not yet packed
    """
    
    def __init__(self, bin_dimensions, items):
        self.bin_dimensions = bin_dimensions
        self.all_items = items.copy()
        self.bins = []
        self.unpacked_items = items.copy()
        self._fitness = None  # Cache fitness value
        
    def add_bin(self):
        """Create and add a new empty bin to the solution."""
        bin_id = len(self.bins)
        new_bin = Bin(bin_id, *self.bin_dimensions)
        self.bins.append(new_bin)
        return new_bin
    
    def get_used_bins_count(self):
        """Return the number of bins that have items in them."""
        return sum(1 for bin in self.bins if not bin.is_empty())
    
    def get_total_bins_count(self):
        """Return the total number of bins created."""
        return len(self.bins)
    
    def get_average_utilization(self):
        """Calculate average volume utilization across used bins."""
        used_bins = [b for b in self.bins if not b.is_empty()]
        if not used_bins:
            return 0.0
        return sum(b.get_volume_utilization() for b in used_bins) / len(used_bins)
    
    def is_valid(self):
        """
        Check if the solution is valid:
        - All items are packed (no unpacked items)
        - No overlaps in any bin
        - All items are within bin boundaries
        
        Returns:
            bool: True if solution is valid
        """
        # Check if all items are packed
        if self.unpacked_items:
            return False
        
        # Check each bin for validity
        for bin in self.bins:
            if bin.has_overlaps():
                return False
            for item in bin.items:
                if not bin.is_valid_placement(item):
                    return False
        
        return True
    
    def calculate_fitness(self):
        """
        Calculate the fitness (cost) of this solution.
        Lower is better.
        
        Components:
        1. Number of used bins (primary objective)
        2. Wasted space penalty
        3. Unpacked items penalty (very high)
        4. Constraint violations penalty
        
        Returns:
            float: Fitness value (lower is better)
        """
        fitness = 0
        
        # Primary objective: minimize number of bins
        used_bins = self.get_used_bins_count()
        fitness += used_bins * 1000
        
        # Penalty for wasted space (encourage better packing)
        avg_utilization = self.get_average_utilization()
        fitness += (100 - avg_utilization) * 10
        
        # Heavy penalty for unpacked items
        fitness += len(self.unpacked_items) * 10000
        
        # Penalty for constraint violations
        for bin in self.bins:
            # Penalty for overlaps
            if bin.has_overlaps():
                fitness += 5000
            
            # Penalty for invalid placements
            for item in bin.items:
                if not bin.is_valid_placement(item):
                    fitness += 5000
        
        self._fitness = fitness
        return fitness
    
    def get_fitness(self):
        """
        Get cached fitness value or calculate if not cached.
        
        Returns:
            float: Fitness value
        """
        if self._fitness is None:
            return self.calculate_fitness()
        return self._fitness
    
    def invalidate_fitness(self):
        """Invalidate cached fitness value (call after modifications)."""
        self._fitness = None
    
    def copy(self):
        """
        Create a deep copy of this solution.
        
        Returns:
            Solution: A new independent copy
        """
        new_solution = Solution(self.bin_dimensions, self.all_items)
        
        # Deep copy bins and items
        item_map = {}  # Map old item IDs to new item objects
        
        for old_bin in self.bins:
            new_bin = new_solution.add_bin()
            
            for old_item in old_bin.items:
                # Create new item with same properties
                new_item = Item(old_item.id, old_item.length, 
                               old_item.width, old_item.height)
                new_item.rotation = old_item.rotation
                if old_item.position:
                    new_item.position = old_item.position
                
                new_bin.add_item(new_item)
                item_map[old_item.id] = new_item
        
        # Update unpacked items
        new_solution.unpacked_items = []
        for old_item in self.unpacked_items:
            if old_item.id not in item_map:
                new_item = Item(old_item.id, old_item.length,
                               old_item.width, old_item.height)
                new_solution.unpacked_items.append(new_item)
                item_map[old_item.id] = new_item
        
        new_solution._fitness = self._fitness
        return new_solution
    
    def get_statistics(self):
        """
        Get statistics about the solution.
        
        Returns:
            dict: Dictionary with various statistics
        """
        return {
            'total_bins': self.get_total_bins_count(),
            'used_bins': self.get_used_bins_count(),
            'avg_utilization': self.get_average_utilization(),
            'unpacked_items': len(self.unpacked_items),
            'total_items': len(self.all_items),
            'fitness': self.get_fitness(),
            'is_valid': self.is_valid()
        }
    
    def __repr__(self):
        """String representation of the solution."""
        return (f"Solution(bins={self.get_used_bins_count()}/{self.get_total_bins_count()}, "
                f"utilization={self.get_average_utilization():.1f}%, "
                f"unpacked={len(self.unpacked_items)}, "
                f"fitness={self.get_fitness():.1f})")
    
    def __lt__(self, other):
        """Compare solutions by fitness (for sorting)."""
        return self.get_fitness() < other.get_fitness()
    
    def __eq__(self, other):
        """Check if two solutions are equal based on fitness."""
        if not isinstance(other, Solution):
            return False
        return abs(self.get_fitness() - other.get_fitness()) < 0.001