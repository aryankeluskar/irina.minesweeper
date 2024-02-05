# code inspired from https://github.com/pedrokkrause/Minesweeper-probability-calculator/tree/main

from random import choice
from copy import deepcopy
import sympy
import itertools
from math import comb
from operator import mul
from functools import reduce

# Generates a random mine board for the game
def genBoard(h, w, nb):
    board = []
    for i in range(h):
        board.append([0] * w)
    possibleCells = []
    for y in range(h):
        for x in range(w):
            possibleCells.append((y, x))
    for i in range(nb):
        c = choice(possibleCells)
        board[c[0]][c[1]] = 1
        possibleCells.remove(c)
    return(board)


# Generates the initial state of what the player can see of the board
def genKnownBoard(h, w):
    board = []
    for i in range(h):
        board.append([None] * w)
    return (board)

# Checks whether some square is inside or not the board
def inside(coords, h, w):
    if 0 <= coords[0] < h and 0 <= coords[1] < w:
        return (True)
    else:
        return (False)

# Returns all the surrounding squares of a given square
def surrounds(coords, board):
    y, x = coords[0], coords[1]
    possibilities = [(y + 1, x), (y + 1, x + 1), (y, x + 1), (y - 1, x), (y - 1, x - 1), (y, x - 1), (y + 1, x - 1),
                     (y - 1, x + 1)]
    surr_sqrs = []
    for sqr in possibilities:
        if inside(sqr, len(board), len(board[0])):
            surr_sqrs.append(sqr)
    return(surr_sqrs)

# Returns the number of mines around a given square
def squareNum(coords, board):
    y, x = coords[0], coords[1]
    possibilities = [(y + 1, x), (y + 1, x + 1), (y, x + 1), (y - 1, x), (y - 1, x - 1), (y, x - 1), (y + 1, x - 1),
                     (y - 1, x + 1)]
    bombcount = 0
    for sqr in possibilities:
        if inside(sqr, len(board), len(board[0])):
            bombcount += board[sqr[0]][sqr[1]]
    return (bombcount)

# In minesweeper, when the player clicks a square with number 0, all surrouding squares are cleared automatically
# This function does that.
def cleanboard(knownBoard,gameBoard,seen):
    # count is the number of squares of number 0 whose surroundings haven't been cleared yet
    count = None
    while count != 0:
        count = 0
        zerosqrs = []
        for y, r in enumerate(knownBoard):
            for x, c in enumerate(r):
                if c == 0 and (y, x) not in seen:
                    for sqr in surrounds((y, x), gameBoard):
                        if gameBoard[sqr[0]][sqr[1]] == 0:
                            sqrNum = squareNum(sqr, gameBoard)
                            if sqrNum == 0:
                                count += 1
                                zerosqrs.append((sqr[0], sqr[1]))
                            else:
                                knownBoard[sqr[0]][sqr[1]] = sqrNum
                    seen.append((y, x))
        for sqr in zerosqrs:
            knownBoard[sqr[0]][sqr[1]] = 0

# Generates all combinations of a list l of symbols with length n
def foo(l,n):
    yield from itertools.product(*([l] * n))

# Breaks down a parametric solution of a linear system into groups
# of parameters that affect each other
def gen_groups(solution,parameters):
    groups = []
    for i in range(len(parameters)):
        groups.append([])
    for i,par in enumerate(parameters):
        groups[i].append(par)
        for eq in solution:
            if eq.coeff(par) != 0:
                for par2 in parameters:
                    if eq.coeff(par2) != 0 and par2!=par and par2 not in groups[i]:
                        groups[i].append(par2)
    for par in parameters:
        hasit = []
        for i,group in enumerate(groups):
            if par in group and group not in hasit:
                hasit.append(group)
        if len(hasit) > 1:
            newgroup = []
            for group in hasit:
                groups.remove(group)
                for par2 in group:
                    if par2 not in newgroup:
                        newgroup.append(par2)
            groups.append(newgroup)
    return(groups)

# The function that returns a board with the probability of each border square having a mine
def calcprobs(board,rem_mines):
    newboard = genKnownBoard(len(board), len(board[0]))
    prev = None
    # Basic rules (For example, "if the number of unknown surrounding squares is equal to the number of the square, then all of them have mines")
    while prev != newboard:
        prev = deepcopy(newboard)
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if type(cell) == int:
                    if cell > 0:
                        sur_sqrs = surrounds((y, x), board)
                        none_sqrs = [x for x in sur_sqrs if board[x[0]][x[1]] == None or board[x[0]][x[1]] == '🚩']
                        sqrs100 = [x for x in none_sqrs if newboard[x[0]][x[1]] == 1.0 or board[x[0]][x[1]] == '🚩']
                        sqrs0 = [x for x in none_sqrs if newboard[x[0]][x[1]] == 0.0]
                        if len(none_sqrs) == cell:
                            for sqr in none_sqrs:
                                newboard[sqr[0]][sqr[1]] = 1.0
                        elif len(sqrs100) == cell:
                            for sqr in [x for x in sur_sqrs if x not in sqrs100]:
                                newboard[sqr[0]][sqr[1]] = 0.0
                        elif len(none_sqrs) - len(sqrs0) == cell:
                            for sqr in [x for x in none_sqrs if x not in sqrs0]:
                                newboard[sqr[0]][sqr[1]] = 1.0

    # Uses groups and set ideas to determine which squares must have mines or not. Watch this video for better understanding: https://youtu.be/8j7bkNXNx4M
    border_sqrs = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if type(cell) == int:
                if cell > 0 and None in [board[sqr[0]][sqr[1]] for sqr in surrounds((y, x), board)]:
                    border_sqrs.append((y, x))
    for sqr in border_sqrs:
        sur_borders = [x for x in surrounds((sqr[0], sqr[1]), board) if x in border_sqrs]
        sur_unknown = [x for x in surrounds((sqr[0], sqr[1]), board) if
                       board[x[0]][x[1]] == None and type(board[x[0]][x[1]]) != float]
        sqr_val = board[sqr[0]][sqr[1]] - len([x for x in surrounds((sqr[0], sqr[1]), board) if
                                               board[x[0]][x[1]] == '🚩' or (
                                                           type(board[x[0]][x[1]]) == float and board[x[0]][
                                                       x[1]] == 1.0)])
        for adj_sqr in sur_borders:
            adjsur_unknown = [x for x in surrounds((adj_sqr[0], adj_sqr[1]), board) if
                              board[x[0]][x[1]] == None and type(board[x[0]][x[1]]) != float]
            adjsqr_val = board[adj_sqr[0]][adj_sqr[1]] - len([x for x in surrounds((adj_sqr[0], adj_sqr[1]), board) if
                                                              board[x[0]][x[1]] == '🚩' or (
                                                                          type(board[x[0]][x[1]]) == float and
                                                                          board[x[0]][x[1]] == 1.0)])
            only_adjsur = [x for x in adjsur_unknown if x not in sur_unknown]
            only_sur = [x for x in sur_unknown if x not in adjsur_unknown]
            if adjsqr_val - sqr_val == len(only_adjsur):
                for sqr2 in only_adjsur:
                    newboard[sqr2[0]][sqr2[1]] = 1.0
                for sqr2 in only_sur:
                    newboard[sqr2[0]][sqr2[1]] = 0.0

    # This section generates, solves and determines all the possible solutions for the minesweeper linear system of equations

    # Gets all border squares which still are not known to be mines or not
    border_sqrs = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if type(cell) == int:
                if cell > 0:
                    border_sqrs += [x for x in surrounds((y, x), board) if
                                    board[x[0]][x[1]] == None and type(newboard[x[0]][x[1]])!=float]
    newborders_sqrs = []
    for x in border_sqrs:
        if x not in newborders_sqrs:
            newborders_sqrs.append(x)
    border_sqrs = newborders_sqrs

    # The squares that are not a border square and are not a cleared square
    unbordered_sqrs = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == None and ((y,x) not in border_sqrs) and type(newboard[y][x])!=float:
                unbordered_sqrs.append((y,x))

    # Gets the equation for each number square
    equation_matrix = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if type(cell) == int:
                if cell > 0:
                    equation = [0] * (len(border_sqrs) + 1)
                    for sqr in [x for x in surrounds((y, x), board) if board[x[0]][x[1]] == None and type(newboard[x[0]][x[1]])!=float]:
                        equation[border_sqrs.index(sqr)] = 1
                    equation[-1] = cell - len([x for x in surrounds((y,x),board) if board[x[0]][x[1]] == '🚩' or newboard[x[0]][x[1]] == 1.0])
                    equation_matrix.append(equation)

    # Proceeds with solving the linear system if there are unknown squares probabilities at all
    if len(border_sqrs) > 0:
        # Names each border square with a1, a2, ...
        symbolstr = ''
        for i in range(len(border_sqrs)):
            symbolstr += f'a{i}, '
        symbolstr = symbolstr[:-2]
        variables = sympy.symbols(symbolstr)

        # Solves the system
        solution = sympy.linsolve(sympy.Matrix(equation_matrix),variables).args[0]

        # Determines what are the parameters of the solution
        parameters = []
        for i in range(len(border_sqrs)):
            if solution.args[i] == variables[i]:
                parameters.append(variables[i])
        print("Number of parameters", len(parameters))

        # The terms of each expression in the solution which are constants (For example, if an expression is a1+a2-2, then -2 is  the constant)
        constants = solution.subs(list(zip(parameters, [0] * len(parameters))))

        # Separates the solution in groups that are independent between each other
        groups = gen_groups(solution,parameters)

        # Gets the equations that belong to each group. An additional group is created to put the expressions which ONLY have constants
        eq_groups = []
        for i in range(len(groups)+1):
            eq_groups.append([])
        eq_groups_num = []  # This is the number of the group that each expression in the solution belongs
        for i,eq in enumerate(solution):
            num = None
            for j,group in enumerate(groups):
                for par in group:
                    if eq.coeff(par) != 0:
                        eq_groups[j].append(eq)
                        num = j
                        break
                    elif eq==constants[i]:
                        num = len(groups)
                        eq_groups[num].append(eq)
                        break
                else:
                    continue
                break
            eq_groups_num.append(num)

        # Sorts the border_sqrs and solution lists such that the first part correponds to the first group, the 2nd to the 2nd and so on
        border_sqrs = [x for _, x in sorted(zip(eq_groups_num, border_sqrs), key=lambda pair: pair[0])]
        solution = [x for _, x in sorted(zip(eq_groups_num, solution), key=lambda pair: pair[0])]

        groups = groups + [[]] # Adds an additional group that contains the parameters for the expressions that only have constants, which is an empty group
        alleq_groups = []  # Contains every possible solution for each group
        for i,eqgroup in enumerate(eq_groups):
            f = sympy.lambdify(groups[i], eqgroup)
            local_possible_solutions = []
            for possibility in foo([0, 1], len(groups[i])):
                localsolution = f(*possibility)
                valid = True
                for x in localsolution:
                    # Each square either has or doesn't have a mine
                    if x != 1 and x != 0:
                        valid = False
                        break
                if valid:
                    local_possible_solutions.append(localsolution)
            alleq_groups.append(local_possible_solutions)

        # It doesn't continue if there are too many parameters, because it could take a lot of time
        # The number of maximum parameters can be changing depending on the speed of the computer
        if len(parameters) < 35:
            # The number of mines that already have been found by the previous two methods
            alreadyFoundMines = 0
            for y,row in enumerate(newboard):
                for x,cell in enumerate(row):
                    if cell == 1.0 and board[y][x]!='🚩':
                        alreadyFoundMines += 1

            numberOfPossibilities = {}                  # A dictionary to reuse some big values already calculated with comb()
            problist = [0]*len(border_sqrs)             # The probabilities of each respective border square having a mine
            unbordered_prob = 0                         # The probability of each unbordered square having a mine
            total = 0                                   # Total number of possible states of mines
            num_possibilities = 0                       # counts the number of possible states of the bordered squares

            # Generates every possible combination of all the possible solutions for each group
            for c in itertools.product(*[list(range(len(x))) for x in alleq_groups]):
                result = []
                for x in [alleq_groups[i][j] for i, j in enumerate(c)]:
                    result = result + x   # Because the border squares were sorted based on the group number, the group possible solutions can just be summed to the list

                val = sum(result)
                if val <= rem_mines - alreadyFoundMines:  # The number of mines in the current possible solution can't be bigger than the number of remaining mines
                    if val not in numberOfPossibilities:
                        numberOfPossibilities[val] = comb(len(unbordered_sqrs), rem_mines - val - alreadyFoundMines)
                    total += numberOfPossibilities[val]
                    unbordered_prob += (rem_mines - val - alreadyFoundMines)
                    num_possibilities += 1
                    for i, x in enumerate(result):
                        problist[i] += x * numberOfPossibilities[val]

            problist = [x/total for x in problist]
            if len(unbordered_sqrs) > 0:
                unbordered_prob /= num_possibilities*len(unbordered_sqrs)
            # Substitutes each found probability to the probability board
            for i,sqr in enumerate(border_sqrs):
                newboard[sqr[0]][sqr[1]] = problist[i]
            for i,sqr in enumerate(unbordered_sqrs):
                newboard[sqr[0]][sqr[1]] = unbordered_prob
        else:
            # In case there were too many parameters, at least some squares are definitely mines because the
            # solution of the linear system gave that they are constants 1 or 0
            for i in range(len(border_sqrs)):
                if solution.args[i] == sympy.core.numbers.Zero:
                    newboard[border_sqrs[i][0]][border_sqrs[i][1]] = 0.0
                elif solution.args[i] == sympy.core.numbers.One:
                    newboard[border_sqrs[i][0]][border_sqrs[i][1]] = 1.0
            print("The probability calculations were not completed because there were too many parameters")
    else:
        print("The linear system method wasn't needed")
    return(newboard)