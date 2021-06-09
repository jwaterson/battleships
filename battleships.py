from random import randint as ri
import sys, re

def is_sunk(ship):
        '''
        returns Boolean value, which is True if ship is sunk and False otherwise
        '''
        return len(ship[4]) == ship[3]

def ship_type(ship):
        '''
        returns one of the strings "battleship", "cruiser", "destroyer", or "submarine" 
        identifying the type of ship
        '''
        return {
            1: "submarine",
            2: "destroyer",
            3: "cruiser",
            4: "battleship"
        }.get(ship[3])

def coords(row, col, hor, lth):
    '''
    given the first four elements of a ship, returns a
    set of tuples containing the coordinates the ship occupies.
    '''
    occupies = []
    for i in range(lth):
        occupies.append([row, col])
        # increments value of the element of the most recently appended sublist, of index 'hor', by i
        occupies[i][hor] += i

    return {tuple(i) for i in occupies}

def is_open_sea(row, col, flt):
    '''
    checks if the square given by row and col neither contains 
    nor is adjacent (horizontally, vertically, or diagonally) to some ship in flt. 
    Returns Boolean True if so and False otherwise
    '''
    r, c = (range(row - 1, row + 2), range(col - 1, col + 2)) # ranges that must be vacant for the function to return True
    for k in flt:
        # checks if either r or c match, or are adjacent to, coordinates of existing ships
        if any([i in r and j in c for i, j in coords(*k[:4])]):
            return False

    return True

def ok_to_place_ship_at(row, col, hor, lth, flt):
    '''
    checks if addition of a ship, specified by row, col, hor, and lth 
    to the flt results in a legal arrangement. If so, the function returns Boolean True 
    and it returns False otherwise. This function makes use of the function is_open_sea
    '''
    b = range(0, 10)
    # checks that each coordinate that the proposed ship would occupy, falls within both the ocean and open sea
    return all([is_open_sea(r, c, flt) and r in b and c in b for (r, c) in coords(row, col, hor, lth)])

def place_ship_at(row, col, hor, lth, flt):
    '''
    returns a new fleet that is the result of adding a ship, specified by row, col, hor, and lth
    to flt. It may be assumed that the resulting arrangement of the new fleet is legal
    '''
    return flt + [(row, col, hor, lth, set())]

def randomly_place_all_ships():
    '''
    returns a fleet (flt) that is a result of a random legal arrangement of the 10 ships in the ocean. 
    This function makes use of the functions ok_to_place_ship_at and place_ship_at
    '''
    flt = []
    # legal returns the row (r), col (c) and hor (h) arguments of a single legally placed ship, using recursion if necessary
    legal = lambda r, c, h: [r, c, h] if ok_to_place_ship_at(r, c, h, j, flt) else legal(ri(0, 9), ri(0, 9), bool(ri(0, 1)))
    for i, j in enumerate(range(4, 0, -1)): # where i represents number of ships with j length
        for _ in range(i + 1):
            flt = place_ship_at(*legal(ri(0, 9), ri(0, 9), bool(ri(0, 1))), j, flt)

    return flt            

def check_if_hits(row, col, flt):
    '''
    returns Boolean value, which is True if the shot of the human player at the square 
    represented by row and col hits any of the ships of flt, and False otherwise
    '''
    # checks whether the shot given by row and col both hits a ship and is already in any ship's set of hits
    return any([(row, col) in coords(*i[:4]) and not (row, col) in i[4] for i in flt])

def hit(row, col, flt):
    '''
    returns a tuple (flt1, ship) where ship is the ship from the fleet, flt, that receives a hit 
    by the shot at the square represented by row and col, and flt1 is the fleet resulting from 
    this hit. It may be assumed that shooting at the square row, col results in of some ship in flt
    '''
    for i in flt:
        if (row, col) in coords(*i[:4]): # checks if the row and col values coincide with any coords of ships in flt
            i[4].add((row, col))
            return flt, i

def are_unsunk_ships_left(flt):
    '''
    returns Boolean value, which is True if there are ships in the fleet 
    that are still not sunk, and False otherwise
    '''
    return not all([is_sunk(i) for i in flt])

def main():
    '''
    Prompts the user to call out rows and columns of shots and outputs the computer's responses iteratively until the game stops.
    When game is over, outputs the number of shots required. 
    '''
    fleet = randomly_place_all_ships()
    run = True
    shots = 0
    while run:
        inp = input("Enter row (0-9) and column (0-9) to shoot, separated by a single space, or 'quit' to exit the game: ")
        if re.match(r"^[0-9] [0-9]$", inp): # makes sure input is two single digit numbers separated by a single space
            row, col = map(int, inp.split())    
            shots += 1
            if check_if_hits(row, col, fleet):
                (fleet, ship_hit) = hit(row, col, fleet)
                print("You sank a " + ship_type(ship_hit) + "!") if is_sunk(ship_hit) else print("You have a hit!")
            else:
                print("You missed!")
                
        elif inp == "quit":
            return
        else:
            print("That's not a valid input!")
        
        if not are_unsunk_ships_left(fleet): 
            run = False
            
    print(f"Game over! You required {shots} shots.")

if __name__ == '__main__':
   main()
   sys.exit()