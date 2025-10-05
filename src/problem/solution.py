"""
Solution class representing a complete bin packing solution.
Simplified version - focuses on item-to-bin assignment.
"""

import copy
from .bin import Bin
from .item import Item


class Solution:
    """
    Represents a complete solution to the 3D bin packing problem.
    Simplified version: tracks which items are assigned to which bins.
    
    A solution consists of:
    - A list of bins (automašīnas) with items assigned to them
    - Each item is assigned to exactly one bin or is unpacked
    
    Attributes:
        bins: List of Bin objects used in this solution
        bin_dimensions: Tuple (length, width, height) for creating new bins
        all_items: List of all items that need to be packed
    """
    
    def __init__(self, bin_dimensions, items):
        """
        Initialize a solution.
        
        Args:
            bin_dimensions: Tuple (length, width, height) for bins
            items: List of Item objects to pack
        """
        self.bin_dimensions = bin_dimensions
        self.all_items = [Item(item.id, item.length, item.width, item.height) 
                          for item in items]
        self.bins = []
        self._fitness = None  # Cache fitness value
        
    def add_bin(self):
        """Create and add a new empty bin to the solution."""
        bin_id = len(self.bins)
        new_bin = Bin(bin_id, *self.bin_dimensions)
        self.bins.append(new_bin)
        return new_bin
    
    def get_item_by_id(self, item_id):
        """
        Get item by its ID.
        
        Args:
            item_id: ID of the item to find
            
        Returns:
            Item object or None if not found
        """
        for item in self.all_items:
            if item.id == item_id:
                return item
        return None
    
    def get_bin_by_id(self, bin_id):
        """
        Get bin by its ID.
        
        Args:
            bin_id: ID of the bin to find
            
        Returns:
            Bin object or None if not found
        """
        for bin in self.bins:
            if bin.id == bin_id:
                return bin
        return None
    
    def get_unpacked_items(self):
        """Get list of items that are not assigned to any bin."""
        return [item for item in self.all_items if not item.is_assigned()]
    
    def get_used_bins(self):
        """Get list of bins that have at least one item."""
        return [bin for bin in self.bins if not bin.is_empty()]
    
    def get_used_bins_count(self):
        """Return the number of bins that have items in them."""
        return len(self.get_used_bins())
    
    def get_total_bins_count(self):
        """Return the total number of bins created."""
        return len(self.bins)
    
    def get_average_utilization(self):
        """Calculate average volume utilization across used bins."""
        used_bins = self.get_used_bins()
        if not used_bins:
            return 0.0
        return sum(b.get_volume_utilization() for b in used_bins) / len(used_bins)
    
    def is_valid(self):
        """
        Check if the solution is valid:
        - All items are packed (assigned to bins)
        - Each bin is feasible (volume and dimension constraints)
        - No item is assigned to multiple bins
        
        Returns:
            bool: True if solution is valid
        """
        # Check if all items are packed
        unpacked = self.get_unpacked_items()
        if unpacked:
            return False
        
        # Check each bin for feasibility
        for bin in self.bins:
            if not bin.is_feasible():
                return False
        
        # Check that no item appears in multiple bins
        all_assigned_items = []
        for bin in self.bins:
            all_assigned_items.extend(bin.items)
        
        if len(all_assigned_items) != len(set(all_assigned_items)):
            return False  # Duplicate assignment
        
        return True
    
    def calculate_fitness(self):
        """
        Calculate the fitness (cost) of this solution.
        Lower is better.
        
        Components:
        1. Number of used bins (primary objective) - weight 1000
        2. Wasted space penalty - weight 10
        3. Variance in bin utilization (balance penalty) - weight 50
        4. Unpacked items penalty - weight 10000
        5. Infeasible bins penalty - weight 5000
        
        Returns:
            float: Fitness score (lower is better)
        """
        fitness = 0
        
        # Primary objective: minimize number of bins
        used_bins = self.get_used_bins_count()
        fitness += used_bins * 1000
        
        # Penalty for wasted space (encourage better packing)
        avg_utilization = self.get_average_utilization()
        fitness += (100 - avg_utilization) * 10
        
        # Penalty for unbalanced packing (variance in utilization)
        used_bin_list = self.get_used_bins()
        if len(used_bin_list) > 1:
            utilizations = [b.get_volume_utilization() for b in used_bin_list]
            mean_util = sum(utilizations) / len(utilizations)
            variance = sum((u - mean_util) ** 2 for u in utilizations) / len(utilizations)
            std_dev = variance ** 0.5
            fitness += std_dev * 50
        
        # Heavy penalty for unpacked items
        unpacked_count = len(self.get_unpacked_items())
        fitness += unpacked_count * 10000
        
        # Penalty for infeasible bins
        for bin in self.bins:
            if not bin.is_feasible():
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
        # Create new solution with copied items (with full state)
        new_items = []
        for item in self.all_items:
            new_item = Item(item.id, item.length, item.width, item.height)
            new_item.rotation = item.rotation
            new_item.position = item.position
            new_item.assigned_bin = item.assigned_bin
            new_items.append(new_item)
        
        new_solution = Solution(self.bin_dimensions, [])
        new_solution.all_items = new_items
        
        # Create mapping from old item IDs to new items
        item_map = {item.id: item for item in new_solution.all_items}
        
        # Copy bins and their assignments
        for old_bin in self.bins:
            new_bin = new_solution.add_bin()
            
            for old_item in old_bin.items:
                new_item = item_map[old_item.id]
                # Don't call add_item as it would change position
                # Just add to list and set assignment
                if new_item not in new_bin.items:
                    new_bin.items.append(new_item)
                    new_item.assigned_bin = new_bin.id
        
        new_solution._fitness = self._fitness
        return new_solution
    
    def get_statistics(self):
        """
        Get statistics about the solution.
        
        Returns:
            dict: Dictionary with various statistics
        """
        unpacked = self.get_unpacked_items()
        return {
            'total_bins': self.get_total_bins_count(),
            'used_bins': self.get_used_bins_count(),
            'avg_utilization': self.get_average_utilization(),
            'unpacked_items': len(unpacked),
            'total_items': len(self.all_items),
            'fitness': self.get_fitness(),
            'is_valid': self.is_valid()
        }
    
    def __repr__(self):
        """String representation of the solution."""
        unpacked = len(self.get_unpacked_items())
        return (f"Solution(bins={self.get_used_bins_count()}/{self.get_total_bins_count()}, "
                f"util={self.get_average_utilization():.1f}%, "
                f"unpacked={unpacked}, "
                f"fitness={self.get_fitness():.1f})")
    
    def __lt__(self, other):
        """Compare solutions by fitness (for sorting)."""
        return self.get_fitness() < other.get_fitness()
    
    def __eq__(self, other):
        """Check if two solutions are equal based on fitness."""
        if not isinstance(other, Solution):
            return False
        return abs(self.get_fitness() - other.get_fitness()) < 0.001