"""
Main entry point for 3D Bin Packing Problem solver.
Uses Local Search optimization algorithm.
"""

from src.problem import Item
from src.utils import first_fit_decreasing
from src.algorithms import LocalSearch
import random


def create_test_instance_small():
    """Create a small challenging test instance - requires multiple bins."""
    items = [
        Item(1, length=8, width=6, height=4),   # Large: 192
        Item(2, length=7, width=5, height=4),   # Large: 140
        Item(3, length=6, width=5, height=3),   # Medium: 90
        Item(4, length=5, width=4, height=3),   # Medium: 60
        Item(5, length=4, width=4, height=3),   # Medium: 48
        Item(6, length=5, width=3, height=2),   # Small: 30
        Item(7, length=4, width=3, height=2),   # Small: 24
        Item(8, length=3, width=3, height=2),   # Small: 18
    ]
    # Total volume: 602, bin volume: 480 → needs at least 2 bins
    bin_dimensions = (10, 8, 6)  # Volume: 480
    return bin_dimensions, items


def create_test_instance_medium():
    """Create a medium challenging test instance."""
    items = [
        Item(1, length=9, width=7, height=5),   # 315
        Item(2, length=8, width=6, height=5),   # 240
        Item(3, length=7, width=6, height=4),   # 168
        Item(4, length=6, width=5, height=4),   # 120
        Item(5, length=6, width=5, height=3),   # 90
        Item(6, length=5, width=4, height=3),   # 60
        Item(7, length=5, width=4, height=2),   # 40
        Item(8, length=4, width=4, height=3),   # 48
        Item(9, length=4, width=3, height=3),   # 36
        Item(10, length=4, width=3, height=2),  # 24
        Item(11, length=3, width=3, height=2),  # 18
        Item(12, length=3, width=2, height=2),  # 12
    ]
    # Total volume: 1171, bin volume: 480 → needs at least 3 bins
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items


def create_test_instance_large():
    """Create a large challenging test instance."""
    items = [
        Item(1, length=9, width=7, height=5),   # 315
        Item(2, length=8, width=7, height=5),   # 280
        Item(3, length=8, width=6, height=5),   # 240
        Item(4, length=7, width=6, height=5),   # 210
        Item(5, length=7, width=6, height=4),   # 168
        Item(6, length=6, width=5, height=4),   # 120
        Item(7, length=6, width=5, height=4),   # 120
        Item(8, length=6, width=5, height=3),   # 90
        Item(9, length=5, width=5, height=3),   # 75
        Item(10, length=5, width=4, height=3),  # 60
        Item(11, length=5, width=4, height=3),  # 60
        Item(12, length=5, width=4, height=2),  # 40
        Item(13, length=4, width=4, height=3),  # 48
        Item(14, length=4, width=4, height=3),  # 48
        Item(15, length=4, width=3, height=3),  # 36
        Item(16, length=4, width=3, height=2),  # 24
        Item(17, length=3, width=3, height=2),  # 18
        Item(18, length=3, width=3, height=2),  # 18
        Item(19, length=3, width=2, height=2),  # 12
        Item(20, length=3, width=2, height=2),  # 12
    ]
    # Total volume: 2014, bin volume: 480 → needs at least 5 bins
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items


def create_random_instance(num_items, bin_dimensions=(10, 8, 6), seed=42):
    """
    Create a random test instance.
    
    Args:
        num_items: Number of items to generate
        bin_dimensions: Bin dimensions
        seed: Random seed for reproducibility
    """
    random.seed(seed)
    items = []
    
    for i in range(1, num_items + 1):
        # Generate random dimensions (30-90% of bin dimensions)
        length = random.randint(int(bin_dimensions[0] * 0.3), int(bin_dimensions[0] * 0.9))
        width = random.randint(int(bin_dimensions[1] * 0.3), int(bin_dimensions[1] * 0.9))
        height = random.randint(int(bin_dimensions[2] * 0.3), int(bin_dimensions[2] * 0.9))
        
        items.append(Item(i, length, width, height))
    
    return bin_dimensions, items


def solve_instance(bin_dimensions, items, instance_name=""):
    """
    Solve a bin packing instance.
    
    Args:
        bin_dimensions: Tuple (length, width, height)
        items: List of Item objects
        instance_name: Name for this instance
        
    Returns:
        dict: Results dictionary
    """
    print("\n" + "=" * 70)
    if instance_name:
        print(f"Solving: {instance_name}")
        print("=" * 70)
    
    bin_volume = bin_dimensions[0] * bin_dimensions[1] * bin_dimensions[2]
    total_items_volume = sum(item.get_volume() for item in items)
    theoretical_min_bins = (total_items_volume + bin_volume - 1) // bin_volume
    
    print(f"\nProblem details:")
    print(f"  Bin dimensions: {bin_dimensions} (volume: {bin_volume})")
    print(f"  Number of items: {len(items)}")
    print(f"  Total items volume: {total_items_volume}")
    print(f"  Theoretical minimum bins: {theoretical_min_bins}")
    
    # Step 1: Generate initial solution
    print(f"\n{'Step 1:':<10} Generating initial solution (First Fit Decreasing)...")
    initial_solution = first_fit_decreasing(bin_dimensions, items)
    initial_stats = initial_solution.get_statistics()
    
    print(f"{'':>10} Initial solution: {initial_solution}")
    print(f"{'':>10} Bins used: {initial_stats['used_bins']}")
    print(f"{'':>10} Average utilization: {initial_stats['avg_utilization']:.2f}%")
    print(f"{'':>10} Fitness: {initial_stats['fitness']:.2f}")
    
    # Show initial packing
    print(f"\n{'':>10} Initial packing:")
    for bin in initial_solution.get_used_bins():
        item_ids = [item.id for item in bin.items]
        print(f"{'':>12} Bin {bin.id}: {len(bin.items)} items {item_ids}, util={bin.get_volume_utilization():.1f}%")
    
    # Step 2: Optimize with Local Search
    print(f"\n{'Step 2:':<10} Optimizing with Local Search...")
    ls = LocalSearch(max_iterations=100, verbose=False)
    final_solution = ls.solve(initial_solution)
    final_stats = final_solution.get_statistics()
    
    print(f"{'':>10} Final solution: {final_solution}")
    print(f"{'':>10} Bins used: {final_stats['used_bins']}")
    print(f"{'':>10} Average utilization: {final_stats['avg_utilization']:.2f}%")
    print(f"{'':>10} Fitness: {final_stats['fitness']:.2f}")
    
    # Show final packing
    print(f"\n{'':>10} Final packing:")
    for bin in final_solution.get_used_bins():
        item_ids = [item.id for item in bin.items]
        print(f"{'':>12} Bin {bin.id}: {len(bin.items)} items {item_ids}, util={bin.get_volume_utilization():.1f}%")
    
    # Summary
    improvement = initial_stats['fitness'] - final_stats['fitness']
    bins_saved = initial_stats['used_bins'] - final_stats['used_bins']
    
    print(f"\n{'Summary:':<10}")
    print(f"{'':>10} Improvement: {improvement:.2f} ({(improvement/initial_stats['fitness']*100):.1f}%)")
    print(f"{'':>10} Bins saved: {bins_saved}")
    print(f"{'':>10} Valid solution: {final_stats['is_valid']}")
    
    if bins_saved > 0:
        print(f"{'':>10} ✓ Local Search found improvement!")
    else:
        print(f"{'':>10} ○ Local Search reached same optimum as FFD")
    
    return {
        'instance_name': instance_name,
        'num_items': len(items),
        'theoretical_min': theoretical_min_bins,
        'initial_bins': initial_stats['used_bins'],
        'final_bins': final_stats['used_bins'],
        'bins_saved': bins_saved,
        'initial_fitness': initial_stats['fitness'],
        'final_fitness': final_stats['fitness'],
        'improvement': improvement,
        'initial_util': initial_stats['avg_utilization'],
        'final_util': final_stats['avg_utilization']
    }


def main():
    """Main function."""
    print("\n")
    print("*" * 70)
    print("3D BIN PACKING PROBLEM - LOCAL SEARCH SOLVER")
    print("*" * 70)
    
    results = []
    
    # Test 1: Small instance
    bin_dims, items = create_test_instance_small()
    result = solve_instance(bin_dims, items, "Small Instance (8 items)")
    results.append(result)
    
    print("\n")
    
    # Test 2: Medium instance
    bin_dims, items = create_test_instance_medium()
    result = solve_instance(bin_dims, items, "Medium Instance (12 items)")
    results.append(result)
    
    print("\n")
    
    # Test 3: Large instance
    bin_dims, items = create_test_instance_large()
    result = solve_instance(bin_dims, items, "Large Instance (20 items)")
    results.append(result)
    
    print("\n")
    
    # Test 4: Random instance
    bin_dims, items = create_random_instance(15, seed=42)
    result = solve_instance(bin_dims, items, "Random Instance (15 items)")
    results.append(result)
    
    # Final summary table
    print("\n\n")
    print("*" * 70)
    print("SUMMARY OF ALL INSTANCES")
    print("*" * 70)
    print()
    print(f"{'Instance':<25} | {'Items':<6} | {'Min':<5} | {'FFD':<5} | {'LS':<5} | {'Saved':<6} | {'Improve %':<10}")
    print("-" * 70)
    
    for r in results:
        improve_pct = (r['improvement'] / r['initial_fitness'] * 100) if r['initial_fitness'] > 0 else 0
        print(f"{r['instance_name']:<25} | {r['num_items']:<6} | {r['theoretical_min']:<5} | "
              f"{r['initial_bins']:<5} | {r['final_bins']:<5} | {r['bins_saved']:<6} | {improve_pct:<10.2f}")
    
    print()
    print("Legend: Min = Theoretical minimum bins, FFD = First Fit Decreasing, LS = Local Search")
    print()
    print("*" * 70)
    print()


if __name__ == "__main__":
    main()