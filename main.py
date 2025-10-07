"""
Main entry point for 3D Bin Packing Problem solver.
Uses Simulated Annealing optimization algorithm with full 3D placement.
"""

from tests.test_instances import TEST_INSTANCES
from src.utils import first_fit_decreasing
from src.algorithms import SimulatedAnnealing
import time


def solve_instance(bin_dimensions, items, instance_name=""):
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
    
    start_time_ffd = time.time()
    initial_solution = first_fit_decreasing(bin_dimensions, items)
    time_ffd = time.time() - start_time_ffd
    
    initial_stats = initial_solution.get_statistics()
    
    print(f"\nInitial Solution (FFD):")
    print(f"  Time: {time_ffd:.3f} seconds")
    print(f"  Bins used: {initial_stats['used_bins']}")
    print(f"  Average utilization: {initial_stats['avg_utilization']:.2f}%")
    print(f"  Fitness: {initial_stats['fitness']:.2f}")
    
    start_time_sa = time.time()
    sa = SimulatedAnnealing(
        initial_temp=1000,
        min_temp=1.0,
        cooling_rate=0.95,
        iterations_per_temp=50,
   )
    final_solution = sa.solve(initial_solution)
    time_sa = time.time() - start_time_sa
    
    final_stats = final_solution.get_statistics()
    
    print(f"\nFinal Solution (SA):")
    print(f"  Time: {time_sa:.3f} seconds")
    print(f"  Bins used: {final_stats['used_bins']}")
    print(f"  Average utilization: {final_stats['avg_utilization']:.2f}%")
    print(f"  Fitness: {final_stats['fitness']:.2f}")
    
    # Summary
    improvement = initial_stats['fitness'] - final_stats['fitness']
    bins_saved = initial_stats['used_bins'] - final_stats['used_bins']
    improvement_pct = (improvement / initial_stats['fitness'] * 100) if initial_stats['fitness'] > 0 else 0
    
    print(f"\nSummary:")
    print(f"  Fitness improvement: {improvement:.2f} ({improvement_pct:.1f}%)")
    print(f"  Bins saved: {bins_saved}")
    print(f"  Total time: {time_ffd + time_sa:.3f} seconds")
    print(f"  Valid solution: {final_stats['is_valid']}")
    
    if improvement_pct > 5:
        print(f"  Result: Significant packing quality improvement")
    elif improvement > 0:
        print(f"  Result: Packing quality improved")
    else:
        print(f"  Result: FFD already found near-optimal packing")
    
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
        'improvement_pct': improvement_pct,
        'initial_util': initial_stats['avg_utilization'],
        'final_util': final_stats['avg_utilization'],
        'time_ffd': time_ffd,
        'time_sa': time_sa,
        'total_time': time_ffd + time_sa
    }


def main():
    """Main function - runs all test instances."""
    print("\n")
    print("*" * 70)
    print("3D BIN PACKING - SIMULATED ANNEALING OPTIMIZATION")
    print("*" * 70)
    print("\nAlgorithm: Simulated Annealing with 3D placement")
    print("Objective: Minimize bins and optimize packing quality")
    print()
    
    results = []
    
    test_keys = ['small', 'medium', 'large', 'xlarge', 'bad_ordering', 'fragmentation', 'rebalance']
    
    for key in test_keys:
        if key not in TEST_INSTANCES:
            continue
            
        instance_info = TEST_INSTANCES[key]
        bin_dims, items = instance_info['generator']()
        result = solve_instance(bin_dims, items, instance_info['name'])
        results.append(result)
    
    print("\n\n")
    print("*" * 70)
    print("SUMMARY OF ALL INSTANCES")
    print("*" * 70)
    print()
    print(f"{'Instance':<30} | {'Items':<6} | {'FFD':<5} | {'SA':<5} | {'Improv %':<9} | {'Time (s)':<9}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['instance_name']:<30} | {r['num_items']:<6} | "
              f"{r['initial_bins']:<5} | {r['final_bins']:<5} | "
              f"{r['improvement_pct']:<9.1f} | {r['total_time']:<9.3f}")

    print()


if __name__ == "__main__":
    main()