"""
Main entry point for 3D Bin Packing Problem solver.
Uses Local Search optimization algorithm with full 3D placement.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_instances import TEST_INSTANCES
from src.utils import first_fit_decreasing
from src.algorithms import LocalSearch


def solve_instance(bin_dimensions, items, instance_name=""):
    """
    Solve a bin packing instance with full 3D placement.
    
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
    
    # Step 1: Generate initial solution with 3D placement
    print(f"\n{'Step 1:':<10} Generating initial solution (FFD with 3D placement)...")
    initial_solution = first_fit_decreasing(bin_dimensions, items)
    initial_stats = initial_solution.get_statistics()
    
    print(f"{'':>10} Initial solution: {initial_solution}")
    print(f"{'':>10} Bins used: {initial_stats['used_bins']}")
    print(f"{'':>10} Average utilization: {initial_stats['avg_utilization']:.2f}%")
    print(f"{'':>10} Fitness: {initial_stats['fitness']:.2f}")
    
    # Show initial packing details
    print(f"\n{'':>10} Initial packing:")
    for bin in initial_solution.get_used_bins():
        item_ids = [item.id for item in bin.items]
        print(f"{'':>12} Bin {bin.id}: {len(bin.items)} items {item_ids}, util={bin.get_volume_utilization():.1f}%")
        # Show if any items are rotated
        rotated = [f"item{item.id}(rot{item.rotation})" for item in bin.items if item.rotation != 0]
        if rotated:
            print(f"{'':>15} Rotated items: {rotated}")
    
    # Step 2: Optimize with Local Search
    print(f"\n{'Step 2:':<10} Optimizing with Local Search (with 3D repacking)...")
    ls = LocalSearch(max_iterations=50, verbose=False)
    final_solution = ls.solve(initial_solution)
    final_stats = final_solution.get_statistics()
    
    print(f"{'':>10} Final solution: {final_solution}")
    print(f"{'':>10} Bins used: {final_stats['used_bins']}")
    print(f"{'':>10} Average utilization: {final_stats['avg_utilization']:.2f}%")
    print(f"{'':>10} Fitness: {final_stats['fitness']:.2f}")
    
    # Show final packing details
    print(f"\n{'':>10} Final packing:")
    for bin in final_solution.get_used_bins():
        item_ids = [item.id for item in bin.items]
        print(f"{'':>12} Bin {bin.id}: {len(bin.items)} items {item_ids}, util={bin.get_volume_utilization():.1f}%")
        # Show rotated items
        rotated = [f"item{item.id}(rot{item.rotation})" for item in bin.items if item.rotation != 0]
        if rotated:
            print(f"{'':>15} Rotated items: {rotated}")
    
    # Summary
    improvement = initial_stats['fitness'] - final_stats['fitness']
    bins_saved = initial_stats['used_bins'] - final_stats['used_bins']
    
    print(f"\n{'Summary:':<10}")
    print(f"{'':>10} Improvement: {improvement:.2f} ({(improvement/initial_stats['fitness']*100):.1f}%)")
    print(f"{'':>10} Bins saved: {bins_saved}")
    print(f"{'':>10} Valid solution: {final_stats['is_valid']}")
    
    if bins_saved > 0:
        print(f"{'':>10} SUCCESS: Local Search reduced bin count!")
    elif improvement > 0:
        print(f"{'':>10} SUCCESS: Local Search improved packing quality!")
    else:
        print(f"{'':>10} INFO: FFD already found good solution")
    
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
    """Main function - runs all test instances."""
    print("\n")
    print("*" * 70)
    print("3D BIN PACKING PROBLEM - LOCAL SEARCH WITH FULL 3D PLACEMENT")
    print("*" * 70)
    
    results = []
    
    # Run all predefined test instances
    for key in ['small', 'medium', 'large']:
        instance_info = TEST_INSTANCES[key]
        bin_dims, items = instance_info['generator']()
        result = solve_instance(bin_dims, items, instance_info['name'])
        results.append(result)
        print("\n")
    
    # Final summary table
    print("\n")
    print("*" * 70)
    print("SUMMARY OF ALL INSTANCES")
    print("*" * 70)
    print()
    print(f"{'Instance':<30} | {'Items':<6} | {'Min':<5} | {'FFD':<5} | {'LS':<5} | {'Saved':<6} | {'Improve %':<10}")
    print("-" * 70)
    
    for r in results:
        improve_pct = (r['improvement'] / r['initial_fitness'] * 100) if r['initial_fitness'] > 0 else 0
        print(f"{r['instance_name']:<30} | {r['num_items']:<6} | {r['theoretical_min']:<5} | "
              f"{r['initial_bins']:<5} | {r['final_bins']:<5} | {r['bins_saved']:<6} | {improve_pct:<10.2f}")
    
    print()
    print("Legend: Min = Theoretical minimum bins, FFD = First Fit Decreasing")
    print("        LS = Local Search with 3D repacking")
    print()
    print("*" * 70)
    print()


if __name__ == "__main__":
    main()