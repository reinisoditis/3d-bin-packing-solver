from src.problem import Item

def create_bad_ordering_instance():
    items = [
        Item(1, length=9, width=8, height=2),   # 144
        Item(2, length=9, width=7, height=2),   # 126
        Item(3, length=8, width=7, height=2),   # 112
        Item(4, length=5, width=4, height=5),   # 100
        Item(5, length=4, width=4, height=6),   # 96
        Item(6, length=5, width=3, height=6),   # 90
        Item(7, length=4, width=4, height=4),   # 64
        Item(8, length=5, width=3, height=4),   # 60
        Item(9, length=3, width=3, height=2),   # 18
        Item(10, length=3, width=2, height=2),  # 12
    ]
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items


def create_fragmentation_instance():
    items = [
        Item(1, length=6, width=5, height=4),   # 120
        Item(2, length=5, width=6, height=4),   # 120
        Item(3, length=6, width=4, height=5),   # 120
        Item(4, length=5, width=5, height=5),   # 125
        Item(5, length=6, width=6, height=3),   # 108
        Item(6, length=5, width=5, height=4),   # 100
        Item(7, length=6, width=5, height=3),   # 90
        Item(8, length=5, width=4, height=4),   # 80
        Item(9, length=4, width=4, height=5),   # 80
        Item(10, length=5, width=5, height=3),  # 75
        Item(11, length=4, width=4, height=4),  # 64
        Item(12, length=4, width=3, height=4),  # 48
    ]
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items


def create_rebalance_instance():
    items = [
        # Large items
        Item(1, length=9, width=7, height=5),   # 315
        Item(2, length=8, width=7, height=5),   # 280
        Item(3, length=4, width=4, height=3),   # 48
        Item(4, length=4, width=3, height=3),   # 36
        Item(5, length=3, width=3, height=3),   # 27
        Item(6, length=3, width=3, height=2),   # 18
        Item(7, length=3, width=2, height=2),   # 12
        Item(8, length=2, width=2, height=2),   # 8
        Item(9, length=2, width=2, height=2),   # 8
        Item(10, length=2, width=2, height=2),  # 8
        Item(11, length=2, width=2, height=2),  # 8
        Item(12, length=2, width=2, height=2),  # 8
    ]
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items

def create_small_instance():
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

def create_xlarge_instance():
    items = [
        # Large items (8 items)
        Item(1, length=9, width=7, height=5),   # 315
        Item(2, length=8, width=7, height=5),   # 280
        Item(3, length=8, width=6, height=5),   # 240
        Item(4, length=7, width=6, height=5),   # 210
        Item(5, length=9, width=6, height=4),   # 216
        Item(6, length=8, width=6, height=4),   # 192
        Item(7, length=7, width=6, height=4),   # 168
        Item(8, length=7, width=5, height=4),   # 140
        
        # Medium items (12 items)
        Item(9, length=6, width=5, height=4),   # 120
        Item(10, length=6, width=5, height=4),  # 120
        Item(11, length=6, width=5, height=3),  # 90
        Item(12, length=6, width=4, height=3),  # 72
        Item(13, length=5, width=5, height=3),  # 75
        Item(14, length=5, width=5, height=3),  # 75
        Item(15, length=5, width=4, height=3),  # 60
        Item(16, length=5, width=4, height=3),  # 60
        Item(17, length=5, width=4, height=2),  # 40
        Item(18, length=5, width=3, height=3),  # 45
        Item(19, length=4, width=4, height=4),  # 64
        Item(20, length=4, width=4, height=3),  # 48
        
        # Small items (10 items)
        Item(21, length=4, width=3, height=3),  # 36
        Item(22, length=4, width=3, height=2),  # 24
        Item(23, length=3, width=3, height=3),  # 27
        Item(24, length=3, width=3, height=3),  # 27
        Item(25, length=3, width=3, height=2),  # 18
        Item(26, length=3, width=3, height=2),  # 18
        Item(27, length=3, width=2, height=2),  # 12
        Item(28, length=3, width=2, height=2),  # 12
        Item(29, length=2, width=2, height=2),  # 8
        Item(30, length=2, width=2, height=2),  # 8
    ]
    bin_dimensions = (10, 8, 6)
    return bin_dimensions, items

TEST_INSTANCES = {
    'small': {
        'name': 'Test case 8 items',
        'generator': create_small_instance,
        'description': '8 items, theoretical min: 2 bins'
    },
    'medium': {
        'name': 'Test case 12 items',
        'generator': create_medium_instance,
        'description': '12 items, theoretical min: 3 bins'
    },
    'large': {
        'name': 'Test case 15 items',
        'generator': create_large_instance,
        'description': '15 items, theoretical min: 4 bins'
    },
    'xlarge': {
        'name': 'Test case 30 items',
        'generator': create_xlarge_instance,
        'description': '30 items, theoretical min: 8 bins'
    },
    'bad_ordering': {
        'name': 'Bad Ordering Instance',
        'generator': create_bad_ordering_instance,
        'description': 'Challenging instance where FFD ordering leads to suboptimal packing.'
    },
    'fragmentation': {
        'name': 'Fragmentation Instance',
        'generator': create_fragmentation_instance,
        'description': 'Many similarly-sized items create fragmentation.'
    },
    'rebalance': {
        'name': 'Rebalance Instance',
        'generator': create_rebalance_instance,
        'description': 'Instance with extreme size variation - good for testing rebalance.'
    },
}
