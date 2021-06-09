import pytest
from battleships import *
from random import randint as ri

'''
is_sunk
'''
@pytest.mark.parametrize("test_input, expected", [
    # tests to check output is not sensitive to ship orientation
    ((5, 5, True, 4, {(5, 5), (5, 6), (5, 7), (5, 8)}), True),
    ((5, 5, False, 4, {(5, 5), (6, 5), (7, 5), (8, 5)}), True),
    # tests to check output is sensitive to differing lengths of set of hits
    ((2, 3, False, 3, {(2, 3), (3, 3), (4, 3)}), True),
    ((2, 3, False, 3, {(2, 3), (3, 3)}), False),
    # tests to check output is not sensitive to ship placement
    ((3, 2, False, 2, {(3, 2), (4, 2)}), True),
    ((3, 7, False, 2, {(3, 7), (4, 7)}), True),
    ((0, 0, True, 1, {(0, 0)}), True),
    ((0, 6, True, 1, {(0, 6)}), True),
    # tests to check output is False whenever 0 < set of hits < ship length (needs to be at least one hit for function to be called)
    ((2, 7, False, 4, {(2, 7), (4, 7), (5, 7)}), False),
    ((2, 7, False, 4, {(3, 7), (4, 7)}), False),
    ((9, 7, True, 3, {(9, 9)}), False),
    ((9, 7, True, 3, {(9, 8), (9, 9)}), False),
    ((5, 3, True, 2, {(5, 3)}), False),
    ((5, 3, False, 2, {(6, 3)}), False),
])

def test_is_sunk(test_input, expected):
    assert is_sunk(test_input) == expected


'''
ship_type
'''
@pytest.mark.parametrize("test_input, expected", [
    ((9, 9, True, 1, {(9, 9)}), "submarine"),
    ((2, 1, True, 2, {(2, 1), (2, 2)}), "destroyer"),
    ((7, 3, False, 3, {(7, 3), (8, 3), (9, 3)}), "cruiser"),
    ((0, 0, False, 4, {(0, 0), (0, 1), (0, 2), (0, 3)}), "battleship"),
    # tests below to check that output of ship_type is not sensitive to variation in the other parameters
    ((9, 9, False, 1, {(9, 9)}), "submarine"),
    ((2, 8, True, 2, {(2, 8), (2, 9)}), "destroyer"),
    ((7, 3, True, 3, {(7, 3), (7, 4), (7, 5)}), "cruiser"),
    ((4, 4, True, 4, {(4, 4), (4, 5), (4, 6), (4, 7)}), "battleship"),
    ((4, 4, False, 4, {(4, 4), (5, 4), (6, 4), (7, 4)}), "battleship")
])

def test_ship_type(test_input, expected):
    assert ship_type(test_input) == expected


'''
coords
'''
@pytest.mark.parametrize("test_input, expected", [
    ((5, 3, False, 4), {(5, 3), (6, 3), (7, 3), (8, 3)}),
    ((0, 1, True, 3), {(0, 1), (0, 2), (0, 3)}),
    ((4, 2, True, 2), {(4, 2), (4, 3)}),
    ((9, 9, False, 1), {(9, 9)}),
    # tests to check that output is sensitive to ship orientation
    ((2, 4, False, 4), {(2, 4), (3, 4), (4, 4), (5, 4)}),
    ((2, 4, True, 4), {(2, 4), (2, 5), (2, 6), (2, 7)})
])

def test_coords(test_input, expected):
    assert coords(*test_input) == expected


'''
is_open_sea
'''
(r, c) = (ri(0, 9), ri(0, 9))
@pytest.mark.parametrize("test_input, expected", [
    #1 - checks that any cell between (0, 0) and (9, 9) is open sea if there are no existent ships
    ((r, c, []), True),
    #2 - checks that adjacency to one OR two ships is disallowed
    ((1, 0, [
        (0, 0, True, 4, set()), 
        (ri(2, 3), 0, False, 3, set())
    ]), False),
    #3 - checks that an existent ship's coords are not considered open sea
    ((9, 9, [
        (9, 6, True, 4, set()),
        (9, 0, True, 3, set()),
        (0, 0, False, 3, set()),
        (6, 9, False, 2, set())
    ]), False),
    #4 - checks that when a sinlge nearby ship that is not adjacent to cell specified by (row, col), the function does not retrun False
    ((6, 9, [
        (1, 3, False, 4, set()), 
        (6, 0, True, 3, set()), 
        (6, 5, True, 3, set()), 
        (8, 3, False, 2, set()),
        (8, 6, False, 2, set()),
        (2, 8, True, 2, set()),
        (3, 6, False, 1, set())
    ]), True),
    # 5 - checks that when multiple nearby ships that are not adjacent to cell specified by (row, col), the function does not return False
    ((3, 6, [
        (2, 1, True, 4, set()),
        (4, 3, False, 3, set()),
        (9, 7, True, 3, set()),
        (2, 8, False, 2, set()),
        (6, 1, False, 2, set()),
        (9, 4, True, 2, set()),
        (7, 7, False, 1, set()),
        (5, 8, True, 1, set()),
        (5, 5, True, 1, set())
    ]), True),
    # 6 - given the same fleet as case #5, shows that a new row, col, adjacent to case #4's row, col, produces different output
    ((3, 7, [
        (2, 1, True, 4, set()),
        (4, 3, False, 3, set()),
        (9, 7, True, 3, set()),
        (2, 8, False, 2, set()),
        (6, 1, False, 2, set()),
        (9, 4, True, 2, set()),
        (7, 7, False, 1, set()),
        (5, 8, True, 1, set()),
        (5, 5, True, 1, set())
    ]), False),
    # 7 - checks that function is sensitive to adjacency with ships across whole horizontal range where x axis has value between 0-9
    ((4, ri(0, 9), [
        (0, 3, False, 4, set()),
        (5, 0, False, 3, set()),
        (1, 6, False, 3, set()),
        (5, 9, False, 2, set())
    ]), False),
    # 8 - checks that function is sensitive to adjacency with ships across whole vertical range where y axis has value between 0-9
    ((ri(0, 9), 4, [
        (8, 5, True, 4, set()),
        (9, 0, True, 3, set()),
        (3, 5, False, 3, set()),
        (0, 3, False, 2, set())
    ]), False),
])

def test_is_open_sea(test_input, expected):
    assert is_open_sea(*test_input) == expected


'''
ok_to_place_ship_at
'''
@pytest.mark.parametrize("test_input, expected", [
    #1 - checks that every coord of a ship must fall within the ocean to be legally placed, irrespective of orientation
    ((7, 7, bool(ri(0, 1)), 4, []), False),
    ((7, 7, bool(ri(0, 1)), 3, []), True),
    ((8, 9, bool(ri(0, 1)), 3, []), False),
    ((8, 8, bool(ri(0, 1)), 2, []), True),
    ((9, 9, bool(ri(0, 1)), 2, []), False),
    #2 - checks that diagonal adjacency to existing ships is disallowed
    ((5, 3, bool(ri(0, 1)), 3, [
        (1, 6, False, 4, set()),
        (8, 4, True, 3, set())
    ]), False),

    ((7, 2, bool(ri(0, 1)), 2, [
        (0, 9, False, 4, set()),
        (6, 7, True, 3, set()),
        (8, 7, True, 3, set()),
        (8, 4, False, 2, set()),
        (9, 0, True, 2, set())
    ]), False),
    #3 - checks that adjacency to any coord of an existing ship is disallowed
    ((ri(0, 3), 1, True, 3, [
        (0, 4, False, 4, set())
    ]), False),

    ((6, ri(2, 4), False, 2, [
        (6, 9, False, 4, set()),
        (0, 6, True, 3, set()),
        (5, 2, True, 3, set())
    ]), False),

    ((6, ri(7, 8), False, 1, [
        (0, 2, True, 4, set()),
        (4, 3, True, 3, set()),
        (1, 8, False, 3, set()),
        (5, 7, True, 2, set()),
        (2, 2, True, 2, set()),
        (7, 3, True, 2, set()),
    ]), False),
    #4 - checks that the function doesn't regard two cells with col numbers 0 and 9, as contiguous; testing cells (2, 0) and (2, 9)
    ((2, 8, True, 2, [
        (0, 6, True, 4, set()),
        (3, 6, False, 3, set()),
        (4, 8, False, 3, set()),
        (2, 0, True, 2, set())
    ]), True),
    #5 - checking the same as case #4 for both the horizontal and vertical axes and again, that the function is sensitive to the lth of proposed ship
    ((9, 9, False, 1, [
        (4, 1, True, 4, set()),
        (0, 0, False, 3, set()),
        (0, 5, True, 3, set()),
        (0, 9, False, 2, set()),
        (9, 0, True, 2, set()),
        (5, 6, True, 2, set()),
    ]), True),
])

def test_ok_to_place_ship_at(test_input, expected):
    assert ok_to_place_ship_at(*test_input) == expected


'''
place_ship_at
'''
@pytest.mark.parametrize("test_input, expected", [
    #1
    ((0, 0, True, 4, []), [(0, 0, True, 4, set())]),
    #2
    ((9, 0, True, 2, [
        (0, 9, False, 4, set()),
        (9, 7, True, 3, set()),
        (0, 0, True, 3, set())
    ]), [
        (0, 9, False, 4, set()),
        (9, 7, True, 3, set()),
        (0, 0, True, 3, set()),
        (9, 0, True, 2, set())
    ]),
    #3
    ((3, 9, False, 2, [
        (0, 5, False, 4, set()),
        (1, 7, True, 3, set()),
        (4, 7, False, 3, set()),
        (6, 9, False, 2, set()),
        (3, 0, False, 2, set())
    ]), [
        (0, 5, False, 4, set()),
        (1, 7, True, 3, set()),
        (4, 7, False, 3, set()),
        (6, 9, False, 2, set()),
        (3, 0, False, 2, set()),
        (3, 9, False, 2, set())
    ]),
    #4
    ((4, 7, False, 1, [
        (4, 1, True, 4, set()), 
        (7, 3, False, 3, set()), 
        (2, 9, False, 3, set()), 
        (8, 7, True, 2, set()), 
        (6, 6, True, 2, set()), 
        (8, 5, False, 2, set()), 
        (7, 1, True, 1, set()), 
        (1, 6, True, 1, set()), 
    ]), [
        (4, 1, True, 4, set()), 
        (7, 3, False, 3, set()), 
        (2, 9, False, 3, set()), 
        (8, 7, True, 2, set()), 
        (6, 6, True, 2, set()), 
        (8, 5, False, 2, set()), 
        (7, 1, True, 1, set()), 
        (1, 6, True, 1, set()),
        (4, 7, False, 1, set()) 
    ]),
    #5
    ((0, 6, True, 1, [
        (1, 9, False, 4, set()),
        (4, 4, True, 3, set()),
        (6, 6, False, 3, set()),
        (7, 3, False, 2, set()),
        (6, 9, False, 2, set()),
        (5, 0, True, 2, set()),
        (2, 6, False, 1, set()),
        (2, 1, True, 1, set()),
        (8, 1, True, 1, set())
    ]), [
        (1, 9, False, 4, set()),
        (4, 4, True, 3, set()),
        (6, 6, False, 3, set()),
        (7, 3, False, 2, set()),
        (6, 9, False, 2, set()),
        (5, 0, True, 2, set()),
        (2, 6, False, 1, set()),
        (2, 1, True, 1, set()),
        (8, 1, True, 1, set()),
        (0, 6, True, 1, set())
    ])
])

def test_place_ship_at(test_input, expected):
    assert place_ship_at(*test_input) == expected


'''
check_if_hits
'''
@pytest.mark.parametrize("test_input, expected", [
    #1 - checks that cells adjacent to ships are not picked up as hits
    ((4, 8, [
        (5, 0, True, 4, set()),
        (3, 7, False, 3, set()),
        (1, 1, True, 3, set()), 
        (6, 5, False, 2, set()),
        (7, 7, True, 2, set()),
        (1, 5, True, 2, set()),
        (9, 4, False, 1, set()),
        (3, 3, True, 1, set()),
        (5, 9, False, 1, set()),
        (7, 0, True, 1, set())
    ]), False),

    ((1, 1, [
        (7, 2, True, 4, set()),
        (4, 9, False, 3, set()),
        (5, 0, False, 3, set()),
        (3, 2, False, 2, {(3, 2)}),
        (5, 7, False, 2, set()),
        (3, 4, False, 2, set()),
        (9, 6, True, 1, set()),
        (1, 5, True, 1, set()),
        (0, 2, True, 1, {(0, 2)}),
        (2, 9, False, 1, set())
    ]), False),
    #2 - checks that cells already hit are not picked up as hits
    ((3, 5, [
        (0, 1, True, 4, set()),
        (2, 0, True, 3, set()),
        (0, 1, True, 4, set()),
        (2, 5, False, 3, {(2, 5), (3, 5), (4, 5)}),
        (0, 8, True, 2, set()),
        (8, 8, True, 2, set()),
        (6, 4, False, 2, {(6, 4), (6, 5)}),
        (3, 9, True, 1, set()),
        (6, 2, True, 1, set()),
        (9, 6, False, 1, set())
    ]), False),

    ((4, 4, [
        (4, 3, True, 4, {(4, 3), (4, 4)}),
        (9, 0, True, 3, {(9, 0), (9, 1), (9, 2)}),
        (6, 6, True, 3, set()),
        (4, 1, False, 2, set()),
        (9, 7, True, 2, {(9, 7), (9, 8)}),
        (0, 2, False, 2, set()),
        (8, 5, True, 1, {(8, 5)}),
        (2, 8, True, 1, set()),
        (4, 9, False, 1, {(4, 9)}),
        (2, 0, False, 1, {(2, 0)})
    ]), False),
    #3 - checks that cells at the extremes end of the grid range are still picked up as hits if within a ship's coords
    ((9, 9, [
        (6, 0, False, 4, {(6, 0), (7, 0), (8, 0), (9, 0)}),
        (6, 3, False, 3, set()),
        (1, 5, False, 3, {(1, 5), (2, 5), (3, 5)}),
        (3, 8, False, 2, set()),
        (8, 9, False, 2, {(8, 9)}),
        (6, 6, True, 2, set()),
        (1, 1, True, 1, {(1, 1)}),
        (1, 8, True, 1, {(1, 8)}),
        (1, 3, True, 1, set()),
        (8, 7, False, 1, set())
    ]), True),

    ((0, 0, [
        (2, 2, False, 4, set()),
        (6, 7, False, 3, set()),
        (3, 4, True, 3, set()),
        (0, 0, False, 2, {(1, 0)}),
        (7, 0, True, 2, set()),
        (7, 4, False, 2, set()),
        (6, 9, False, 1, set()),
        (0, 7, False, 1, set()),
        (2, 8, True, 1, set()),
        (9, 9, False, 1, set())
    ]), True),
    #4 - checks that the function will not add a sequentially consecutive cell to set of hits, if the shot doesn't coincide with the ship's coords
    ((9, 8, [
        (9, 4, True, 4, {(9, 5), (9, 6), (9, 7)}),
        (5, 6, False, 3, {(5, 6), (6, 6), (7, 6)}),
        (3, 0, True, 3, {(3, 0), (3, 1), (3, 2)}),
        (2, 7, False, 2, {(2, 7), (3, 7)}),
        (9, 0, True, 2, {(9, 0), (9, 1)}),
        (0, 2, False, 2, {(0, 2), (1, 2)}),
        (0, 9, False, 1, {(0, 9)}),
        (7, 9, True, 1, {(7, 9)}),
        (6, 4, True, 1, {(6, 4)}),
        (3, 4, False, 1, {(3, 4)})
    ]), False),
    #5 - checks that when given almost identical input as case #4, will instead return True if the shot coincides with a ship and isn't yet in its set of hits
    ((9, 8, [
        (9, 5, True, 4, {(9, 5), (9, 6), (9, 7)}),
        (5, 6, False, 3, {(5, 6), (6, 6), (7, 6)}),
        (3, 0, True, 3, {(3, 0), (3, 1), (3, 2)}),
        (2, 7, False, 2, {(2, 7), (3, 7)}),
        (9, 0, True, 2, {(9, 0), (9, 1)}),
        (0, 2, False, 2, {(0, 2), (1, 2)}),
        (0, 9, False, 1, {(0, 9)}),
        (7, 9, True, 1, {(7, 9)}),
        (6, 4, True, 1, {(6, 4)}),
        (3, 4, False, 1, {(3, 4)})
    ]), True),

    
])

def test_check_if_hits(test_input, expected):
    assert check_if_hits(*test_input) == expected


'''
hit
'''
@pytest.mark.parametrize("test_input, expected", [
    #1
    ((6, 9, [
        (3, 9, False, 4, {(3, 9), (4, 9), (5, 9)}),
        (7, 2, True, 3, set()),
        (1, 4, False, 3, set()),
        (1, 0, False, 2, set()),
        (5, 6, True, 2, set()),
        (9, 3, True, 2, set()),
        (9, 0, False, 1, set()),
        (4, 0, True, 1, set()),
        (8, 8, True, 1, set()),
        (2, 6, False, 1, set())
    ]), ([
        (3, 9, False, 4, {(3, 9), (4, 9), (5, 9), (6, 9)}),
        (7, 2, True, 3, set()),
        (1, 4, False, 3, set()),
        (1, 0, False, 2, set()),
        (5, 6, True, 2, set()),
        (9, 3, True, 2, set()),
        (9, 0, False, 1, set()),
        (4, 0, True, 1, set()),
        (8, 8, True, 1, set()),
        (2, 6, False, 1, set())
    ], (3, 9, False, 4, {(3, 9), (4, 9), (5, 9), (6, 9)}))),
    #2
    ((8, 8, [
        (1, 8, False, 4, set()),
        (6, 8, False, 3, set()),
        (7, 2, True, 3, set()),
        (1, 0, False, 2, set()),
        (4, 0, False, 2, set()),
        (9, 3, True, 2, set()),
        (5, 5, True, 1, set()),
        (0, 5, False, 1, set()),
        (3, 5, True, 1, set()),
        (1, 3, False, 1, set())
    ]), ([
        (1, 8, False, 4, set()),
        (6, 8, False, 3, {(8, 8)}),
        (7, 2, True, 3, set()),
        (1, 0, False, 2, set()),
        (4, 0, False, 2, set()),
        (9, 3, True, 2, set()),
        (5, 5, True, 1, set()),
        (0, 5, False, 1, set()),
        (3, 5, True, 1, set()),
        (1, 3, False, 1, set())
    ], (6, 8, False, 3, {(8, 8)}))),
    #3
    ((3, 3, [
        (7, 3, True, 4, {(7, 3), (7, 4), (7, 5), (7, 6)}),
        (5, 6, True, 3, {(5, 6), (5, 7), (5, 8)}),
        (9, 5, True, 3, {(9, 5), (9, 6), (9, 7)}),
        (0, 1, False, 2, {(0, 1), (1, 1)}),
        (3, 2, True, 2, {(3, 2)}),
        (5, 1, True, 2, {(5, 1), (5, 2)}),
        (9, 1, True, 1, {(9, 1)}),
        (0, 4, True, 1, {(0, 4)}),
        (0, 8, False, 1, {(0, 8)}),
        (2, 9, False, 1, {(2, 9)})
    ]), ([
        (7, 3, True, 4, {(7, 3), (7, 4), (7, 5), (7, 6)}),
        (5, 6, True, 3, {(5, 6), (5, 7), (5, 8)}),
        (9, 5, True, 3, {(9, 5), (9, 6), (9, 7)}),
        (0, 1, False, 2, {(0, 1), (1, 1)}),
        (3, 2, True, 2, {(3, 2), (3, 3)}),
        (5, 1, True, 2, {(5, 1), (5, 2)}),
        (9, 1, True, 1, {(9, 1)}),
        (0, 4, True, 1, {(0, 4)}),
        (0, 8, False, 1, {(0, 8)}),
        (2, 9, False, 1, {(2, 9)})
    ], (3, 2, True, 2, {(3, 2), (3, 3)}))),
    #4
    ((3, 7, [
        (0, 7, False, 4, set()),
        (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}),
        (4, 2, False, 3, {(4, 2), (5, 2), (6, 2)}),
        (0, 9, False, 2, {(0, 9), (1, 9)}),
        (6, 6, False, 2, {(6, 6), (7, 6)}),
        (4, 0, False, 2, {(4, 0), (5, 0)}),
        (9, 4, True, 1, {(9, 4)}),
        (8, 0, True, 1, {(8, 0)}),
        (7, 8, False, 1, {(7, 8)}),
        (9, 8, True, 1, {(9, 8)})
    ]), ([
        (0, 7, False, 4, {(3, 7)}),
        (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}),
        (4, 2, False, 3, {(4, 2), (5, 2), (6, 2)}),
        (0, 9, False, 2, {(0, 9), (1, 9)}),
        (6, 6, False, 2, {(6, 6), (7, 6)}),
        (4, 0, False, 2, {(4, 0), (5, 0)}),
        (9, 4, True, 1, {(9, 4)}),
        (8, 0, True, 1, {(8, 0)}),
        (7, 8, False, 1, {(7, 8)}),
        (9, 8, True, 1, {(9, 8)})
    ], (0, 7, False, 4, {(3, 7)}))),
    #5
    ((7, 9, [
        (0, 2, True, 4, set()),
        (2, 3, True, 3, set()),
        (3, 0, False, 3, set()),
        (7, 6, True, 2, {(7, 6), (7, 7)}),
        (8, 4, False, 2, set()),
        (0, 7, True, 2, set()),
        (3, 9, False, 1, {(3, 9)}),
        (9, 7, True, 1, set()),
        (7, 0, False, 1, {(7, 0)}),
        (7, 9, True, 1, set())
    ]), ([
        (0, 2, True, 4, set()),
        (2, 3, True, 3, set()),
        (3, 0, False, 3, set()),
        (7, 6, True, 2, {(7, 6), (7, 7)}),
        (8, 4, False, 2, set()),
        (0, 7, True, 2, set()),
        (3, 9, False, 1, {(3, 9)}),
        (9, 7, True, 1, set()),
        (7, 0, False, 1, {(7, 0)}),
        (7, 9, True, 1, {(7, 9)})
    ], (7, 9, True, 1, {(7, 9)})))
])

def test_hit(test_input, expected):
    assert hit(*test_input) == expected


'''
are_unsunk_ships_left
'''
@pytest.mark.parametrize("test_input, expected", [
    #1 - checks that a fleet of ships each with maximum hits, is considered sunk
    (([
        (8, 2, True, 4, {(8, 2), (8, 3), (8, 4), (8, 5)}), 
        (6, 0, False, 3, {(6, 0), (7, 0), (8, 0)}), 
        (0, 3, False, 3, {(0, 3), (1, 3), (2, 3)}), 
        (2, 9, False, 2, {(2, 9), (3, 9)}),
        (5, 1, True, 2, {(5, 1), (5, 2)}),
        (0, 1, False, 2, {(0, 1), (1, 1)}),
        (8, 1, False, 1, {(8, 1)}),
        (5, 5, True, 1, {(5, 5)}),
        (8, 5, False, 1, {(8, 5)}),
        (9, 3, True, 1, {(9, 3)})
    ]), False),
    #2 - checks that a fleet of ships with no hits, is not considered sunk 
    (([
        (5, 8, False, 4, set()), 
        (2, 7, True, 3, set()), 
        (2, 4, False, 3, set()), 
        (6, 5, True, 2, set()), 
        (8, 1, False, 2, set()), 
        (6, 3, False, 2, set()), 
        (0, 9, False, 1, set()), 
        (9, 4, False, 1, set()), 
        (4, 6, True, 1, set()), 
        (0, 0, True, 1, set())
    ]), True),
    #3 - checks that when each ship uniformly still requires one hit, they are not considered sunk
    (([
        (4, 1, True, 4, {(4, 1), (4, 2), (4, 3)}),
        (0, 2, False, 3, {(0, 2), (1, 2)}),
        (7, 5, False, 3, {(7, 5), (9, 5)}),
        (9, 8, True, 2, {(9, 8)}),
        (6, 7, False, 2, {(7, 7)}),
        (6, 0, True, 2, {(6, 0)}),
        (5, 9, True, 1, set()),
        (7, 3, False, 1, set()),
        (1, 5, True, 1, set()),
        (8, 1, True, 1, set())
    ]), True),
    #4 - checks that a single unsunk ship left returns True
    (([
        (5, 8, False, 4, {(5, 8), (6, 8), (7, 8), (8, 8)}), 
        (1, 6, False, 3, {(1, 6), (2, 6), (3, 6)}), 
        (0, 3, False, 3, {(0, 3), (1, 3), (2, 3)}), 
        (2, 9, False, 2, {(2, 9), (3, 9)}),
        (5, 1, True, 2, {(5, 1), (5, 2)}),
        (0, 1, False, 2, {(0, 1), (1, 1)}),
        (8, 1, False, 1, set()),
        (5, 5, True, 1, {(5, 5)}),
        (8, 5, False, 1, {(8, 5)}),
        (9, 3, True, 1, {(9, 3)})
    ]), True),
    #5 - checks that given same fleet as case #4, but with a hit on the last unsunk sub, returns False
    (([
        (5, 8, False, 4, {(5, 8), (6, 8), (7, 8), (8, 8)}), 
        (1, 6, False, 3, {(1, 6), (2, 6), (3, 6)}), 
        (0, 3, False, 3, {(0, 3), (1, 3), (2, 3)}), 
        (2, 9, False, 2, {(2, 9), (3, 9)}),
        (5, 1, True, 2, {(5, 1), (5, 2)}),
        (0, 1, False, 2, {(0, 1), (1, 1)}),
        (8, 1, False, 1, {(8, 1)}),
        (5, 5, True, 1, {(5, 5)}),
        (8, 5, False, 1, {(8, 5)}),
        (9, 3, True, 1, {(9, 3)})
    ]), False),
])

def test_are_unsunk_ships_left(test_input, expected):
    assert are_unsunk_ships_left(test_input) == expected
