assignments = []

def cross(a, b):
    return [s+t for s in a for t in b]

def get_common_structure():
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)

    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    return boxes, unitlist, units, peers, rows, cols

boxes, unitlist, units, peers, rows, cols = get_common_structure()


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(a, b):
      return [s+t for s in a for t in b]

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    rows = 'ABCDEFGHI'
    cols = '123456789'

    for k in values.keys():
        # has to be length 2 to be a twin
        if len(values[k]) == 2:

            # all column boxes
            columns_to_search = cross(k[0], cols)
            # columns to search
            columns_to_search.remove(k)

            for peer in columns_to_search:
                # if a naked twin
                if values[peer] == values[k]:
                    # remove the twin
                    columns_to_search.remove(peer)
                    # for each non-twin in column
                    for non_twin in columns_to_search:
                        # for each value 
                        for value_to_remove in values[k]:
                            # remove the value from non_twin
                            values = assign_value( values, non_twin, values[non_twin].replace(value_to_remove,'') )
                        

            # all row boxes 
            rows_to_search = cross( rows, k[1] )
            # rows to search
            rows_to_search.remove(k)
            for peer in rows_to_search:
                # if naked twin
                if values[peer] == values[k]:
                    # remove the twin
                    rows_to_search.remove(peer)
                    # for each non-twin in row
                    for non_twin in rows_to_search:
                        # for each value 
                        for value_to_remove in values[k]:
                            # remove the value from non_twin
                            values = assign_value( values, non_twin, values[non_twin].replace(value_to_remove,'') )
            
    # diagonals
    diagonal_one = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    diagonal_two = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']
    diagonals = [diagonal_one, diagonal_two]

    #strategy 1) eliminate single values from peers
    #for each diagonal
    for diagonal in diagonals:
        # iterate over the boxes...
        for k in diagonal:
            # has to be length 2 to be a twin
            if len(values[k]) == 2:
                # all column boxes
                values_to_search = diagonal
                values_to_search.remove(k)

                for peer in values_to_search:
                    # if a naked twin
                    if values[peer] == values[k]:
                        # remove the twin
                        values_to_search.remove(peer)
                        # for each non-twin in column
                        for non_twin in values_to_search:
                            # for each value 
                            for value_to_remove in values[k]:
                                # remove the value from non_twin
                                values = assign_value( values, non_twin, values[non_twin].replace(value_to_remove,'') )
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    grid_dict = {}
    for idx,a in enumerate(grid):
        grid_dict[boxes[idx]]= a if ('.' not in a) else '123456789'
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # iterate over the boxes...
    for k in values.keys():
        # when the box only has one value...
        if len(values[k]) == 1:
            # find the box's peers...
            for peer in peers[k]:
                # remove the box's value...
                values = assign_value( values, peer, values[peer].replace(values[k],'') )
    return values



def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            # if only one possibility...
            if len(dplaces) == 1:
                # assign using provided method
                values= assign_value( values, dplaces[0], digit )
    return values

def check_diags(values):
    diagonal_one = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    diagonal_two = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']
    rev_multidict = {}
    for key, value in dict((k, values[k]) for k in diagonal_one):
        rev_multidict.setdefault(value, set()).add(key)

    if (values['F6'] == values['H8']):
        return False

    if [key for key, values2 in rev_multidict.items() if len(values2) > 1]:
        print('too many values')
        return False

    rev_multidict = {}
    for key, value in dict((k, values[k]) for k in diagonal_two):
        rev_multidict.setdefault(value, set()).add(key)
    if [key for key, values2 in rev_multidict.items() if len(values2) > 1]:
        print('too many values')
        return False

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
    
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        
        # Use the Only Choice Strategy
        values = only_choice(values)

        # keep the utility of the functions through separation, solve the diagonal puzzle
        values = diagonal_solve(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = check_diags(values)
    if values == False:
        return False ## Failed earlier
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False ## Failed earlier
    # Return false if the diagonal rules are violated
    
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def diagonal_solve(values):
    diagonal_one = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    diagonal_two = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']
    diagonals = [diagonal_one, diagonal_two]

    #strategy 1) eliminate single values from peers
    #for each diagonal
    for diagonal in diagonals:
        # iterate over the boxes...
        for k in diagonal:
            # when the box only has one value...
            if len(values[k]) == 1:
                # find the box's peers...
                diag_peers = diagonal
                # ...by removing k from the list of diagonals
                diag_peers.remove(k)
                # and adding the normal peers
                #for p in peers[k]:
                #    diag_peers.append(p)
                # iterate over the peers
                for peer in diag_peers:
                    # remove the box's value...
                    values = assign_value( values, peer, values[peer].replace(values[k],'') )

    # strategy 2) only choice
    # for each diagonal
    for diagonal in diagonals:
        # iterate over the possible digits...
        for digit in '123456789':
                dplaces = [box for box in diagonal if digit in values[box]]
                # if only one possibility...
                if len(dplaces) == 1:
                    # assign using provided method
                    values= assign_value( values, dplaces[0], digit )
    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    dict_grid = grid_values(grid)
    result = reduce_puzzle(dict_grid)

    if all(len(result[s]) == 1 for s in boxes): 
        return result ## Solved!
    else:
        print('Using depth first search since no simple rule solution exists.')
        return search(result)


if __name__ == '__main__':    
    naked_twins_test = {"G7": "1234568", "G6": "9", "G5": "35678", "G4": "23678", "G3":
"245678", "G2": "123568", "G1": "1234678", "G9": "12345678", "G8":
"1234567", "C9": "13456", "C8": "13456", "C3": "4678", "C2": "68",
"C1": "4678", "C7": "13456", "C6": "368", "C5": "2", "A4": "5", "A9":
"2346", "A8": "2346", "F1": "123689", "F2": "7", "F3": "25689", "F4":
"23468", "F5": "1345689", "F6": "23568", "F7": "1234568", "F8":
"1234569", "F9": "1234568", "B4": "46", "B5": "46", "B6": "1", "B7":
"7", "E9": "12345678", "B1": "5", "B2": "2", "B3": "3", "C4": "9",
"B8": "8", "B9": "9", "I9": "1235678", "I8": "123567", "I1": "123678",
"I3": "25678", "I2": "123568", "I5": "35678", "I4": "23678", "I7":
"9", "I6": "4", "A1": "2468", "A3": "1", "A2": "9", "A5": "3468",
"E8": "12345679", "A7": "2346", "A6": "7", "E5": "13456789", "E4":
"234678", "E7": "1234568", "E6": "23568", "E1": "123689", "E3":
"25689", "E2": "123568", "H8": "234567", "H9": "2345678", "H2":
"23568", "H3": "2456789", "H1": "2346789", "H6": "23568", "H7":
"234568", "H4": "1", "H5": "35678", "D8": "1235679", "D9": "1235678",
"D6": "23568", "D7": "123568", "D4": "23678", "D5": "1356789", "D2":
"4", "D3": "25689", "D1": "123689"}
    #results = reduce_puzzle(naked_twins_test)
    #display(results)
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    diag_sudoku_grid = '.8..794...........3..5..9........1..........2..........72......8.1.....7...4.7.1.'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
