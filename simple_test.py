"""
Test script for simplified 3D Bin Packing classes.
Focus on item-to-bin assignment without exact positions.
"""

from src.problem import Item, Bin, Solution

def test_simplified_version():
    print("=" * 60)
    print("Testing Simplified 3D Bin Packing Classes")
    print("=" * 60)
    
    # Test 1: Create items (kastes)
    print("\n1. Creating items (kastes):")
    items = [
        Item(1, length=3, width=2, height=2),  # Volume: 12
        Item(2, length=4, width=3, height=2),  # Volume: 24
        Item(3, length=2, width=2, height=2),  # Volume: 8
        Item(4, length=5, width=2, height=1),  # Volume: 10
    ]
    
    for item in items:
        print(f"   {item}")
    
    total_volume = sum(item.get_volume() for item in items)
    print(f"   Total items volume: {total_volume}")
    
    # Test 2: Create bin (automašīna)
    print("\n2. Creating bin (automašīna):")
    bin_dims = (10, 8, 6)  # Volume: 480
    car = Bin(0, *bin_dims)
    print(f"   {car}")
    print(f"   Bin volume: {car.get_volume()}")
    
    # Test 3: Assign items to bin
    print("\n3. Assigning items to bin:")
    car.add_item(items[0])
    car.add_item(items[1])
    car.add_item(items[2])
    
    print(f"   {car}")
    print(f"   Used volume: {car.get_used_volume()}")
    print(f"   Remaining volume: {car.get_remaining_volume()}")
    print(f"   Utilization: {car.get_volume_utilization():.2f}%")
    print(f"   Is feasible: {car.is_feasible()}")
    
    # Test 4: Check item assignment
    print("\n4. Checking item assignments:")
    for item in items:
        print(f"   Item {item.id}: assigned={item.is_assigned()}, bin={item.assigned_bin}")
    
    # Test 5: Create solution
    print("\n5. Creating solution:")
    solution = Solution(bin_dims, items)
    
    # Add first bin with some items
    bin1 = solution.add_bin()
    bin1.add_item(solution.get_item_by_id(1))
    bin1.add_item(solution.get_item_by_id(2))
    
    # Add second bin with remaining items
    bin2 = solution.add_bin()
    bin2.add_item(solution.get_item_by_id(3))
    bin2.add_item(solution.get_item_by_id(4))
    
    print(f"   {solution}")
    
    # Test 6: Solution statistics
    print("\n6. Solution statistics:")
    stats = solution.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test 7: Test can_fit_item
    print("\n7. Testing can_fit_item:")
    small_bin = Bin(99, length=3, width=3, height=3)
    large_item = Item(99, length=5, width=5, height=5)
    fitting_item = Item(100, length=2, width=2, height=2)
    
    print(f"   Large item fits in small bin: {small_bin.can_fit_item(large_item)}")
    print(f"   Fitting item fits in small bin: {small_bin.can_fit_item(fitting_item)}")
    
    # Test 8: Test solution copy
    print("\n8. Testing solution copy:")
    solution_copy = solution.copy()
    print(f"   Original: {solution}")
    print(f"   Copy: {solution_copy}")
    print(f"   Are same object: {solution is solution_copy}")
    print(f"   Have same fitness: {solution.get_fitness() == solution_copy.get_fitness()}")
    
    # Test 9: Test item removal
    print("\n9. Testing item removal:")
    print(f"   Before removal: {bin1}")
    item_to_remove = solution.get_item_by_id(2)
    bin1.remove_item(item_to_remove)
    print(f"   After removal: {bin1}")
    print(f"   Item {item_to_remove.id} assigned: {item_to_remove.is_assigned()}")
    
    # Test 10: Test unpacked items
    print("\n10. Testing unpacked items:")
    solution2 = Solution(bin_dims, items[:2])  # Only 2 items
    bin_new = solution2.add_bin()
    bin_new.add_item(solution2.get_item_by_id(1))
    # Item 2 is not assigned
    
    unpacked = solution2.get_unpacked_items()
    print(f"   Unpacked items count: {len(unpacked)}")
    print(f"   Unpacked items: {[item.id for item in unpacked]}")
    print(f"   Solution is valid: {solution2.is_valid()}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_simplified_version()