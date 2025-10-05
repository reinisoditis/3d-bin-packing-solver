"""
Test instances for 3D Bin Packing Problem.
Contains predefined small, medium, and large test cases.
"""
from src.problem import Item


def create_small_instance():
    """
    Small test instance - 8 items, requires at least 2 bins.
    Total volume: 602, bin volume: 480
    """
    items = [
        Item(1, length=8, width=6, height=4),   # 192
        Item(2, length=7, width=5, height=4),   # 140
        Item(3, length=6, width=5, height=3),   # 90
        Item(4, length=5, width=4, height=3),   # 60
        Item(5, length=4, width=4, height=3),   # 48
        Item(6, length=5, width=3, height=2),   # 30
        Item(7, length=4, width=3, height=2),   # 24
        Item(8, length=3, width=3, height=2),   # 18
    ]
    bin_dimensions = (10, 8, 6)  # Volume: 480
    return bin_dimensions, items


def create_medium_instance():
    """
    Medium test instance - 12 items, requires at least 3 bins.
    Total volume: 1171, bin volume: 480
    """
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
    bin_dimensions = (10, 8, 6)  # Volume: 480
    return bin_dimensions, items


def create_large_instance():
    """
    Large test instance - 15 items, requires at least 4 bins.
    Total volume: 1910, bin volume: 480
    """
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
    ]
    bin_dimensions = (10, 8, 6)  # Volume: 480
    return bin_dimensions, items

TEST_INSTANCES = {
    'small': {
        'name': 'Small Instance (8 items)',
        'generator': create_small_instance,
        'description': '8 items, theoretical min: 2 bins'
    },
    'medium': {
        'name': 'Medium Instance (12 items)',
        'generator': create_medium_instance,
        'description': '12 items, theoretical min: 3 bins'
    },
    'large': {
        'name': 'Large Instance (15 items)',
        'generator': create_large_instance,
        'description': '15 items, theoretical min: 4 bins'
    }
}
