"""
Solution class representing a complete bin packing solution.
Simplified version - focuses on item-to-bin assignment.
"""

from .bin import Bin
from .item import Item


class Solution:
    def __init__(self, bin_dimensions, items):
        self.bin_dimensions = bin_dimensions
        self.all_items = [Item(item.id, item.length, item.width, item.height) 
                          for item in items]
        self.bins = []
        self._fitness = None  # Cache fitness value
        
    def add_bin(self):
        bin_id = len(self.bins)
        new_bin = Bin(bin_id, *self.bin_dimensions)
        self.bins.append(new_bin)
        return new_bin
    
    def get_item_by_id(self, item_id):
        for item in self.all_items:
            if item.id == item_id:
                return item
        return None
    
    def get_bin_by_id(self, bin_id):
        for bin in self.bins:
            if bin.id == bin_id:
                return bin
        return None
    
    def get_unpacked_items(self):
        return [item for item in self.all_items if not item.is_assigned()]
    
    def get_used_bins(self):
        return [bin for bin in self.bins if not bin.is_empty()]
    
    def get_used_bins_count(self):
        return len(self.get_used_bins())
    
    def get_total_bins_count(self):
        return len(self.bins)
    
    def get_average_utilization(self):
        used_bins = self.get_used_bins()
        if not used_bins:
            return 0.0
        return sum(b.get_volume_utilization() for b in used_bins) / len(used_bins)
    
    def is_valid(self):
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
        if self._fitness is None:
            return self.calculate_fitness()
        return self._fitness
    
    def invalidate_fitness(self):
        self._fitness = None
    
    def copy(self):
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