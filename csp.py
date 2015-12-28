###########################################
# you need to implement five funcitons here
###########################################

import copy
import random

def fileParse(filename):
    """
    This function parses input file and does initial setup
    It returns a 0 initialized sudoku gameState and sudokuConfig
    tuple which has sudoku config info like N, M and K.
    """
    fileHandle = open(filename, 'r')
    rawState = fileHandle.readline().rstrip('\n ;').split(',')
    n = int(rawState[0])
    m = int(rawState[1])
    k = int(rawState[2])

    sudokuConfig = (n,m,k)

    sudoku = [[0 for x in range(n)] for x in range(n)]

    newRawState = []

    for i in range(n):
        rawState = fileHandle.readline().rstrip('\n ;').split(',')
        newRawState.append(rawState)
        for j in range(n):
            if newRawState[i][j] != '-':
                sudoku[i][j] = int(newRawState[i][j])

    return (sudoku, sudokuConfig)

def checkEmptyLocation(gameState, sudokuConfig):
    """
    This function returns the first empty cell row and col number
    """
    for row in range(sudokuConfig[0]):
        for col in range(sudokuConfig[0]):
            if gameState[row][col] == 0:
                return (True, row, col)
    return (False, row, col)

def usedInRow(gameState, sudokuConfig, row, num):
    """
    This function checks if the number is already present in the current row
    """

    for col in range(sudokuConfig[0]):
        if gameState[row][col] == num:
            return True

    return False

def usedInCol(gameState, sudokuConfig, col, num):
    """
    This function checks if the number is already present in the current col
    """

    for row in range(sudokuConfig[0]):
        if gameState[row][col] == num:
            return True

    return False

def usedInBox(gameState, sudokuConfig, boxRow, boxCol, num):
    """
    This function checks if the number is already present in it's current box
    """

    for row in range(sudokuConfig[1]):
        for col in range(sudokuConfig[2]):
            if gameState[row+boxRow][col+boxCol] == num:
                return True

    return False

def isValidMove(gameState, sudokuConfig, row, col, num):
    """
    This function checks if the number in given row and column is a valid move
    based on all above criteria
    """

    if not usedInRow(gameState, sudokuConfig, row, num) and \
        not usedInCol(gameState, sudokuConfig, col, num) and \
        not usedInBox(gameState, sudokuConfig, row - row%sudokuConfig[1], col - col%sudokuConfig[2], num):
        return True

    return False


backtrackChecks = 0
backtrackMRVChecks = 0
backtrackMRV_FWDChecks = 0
backtrackMRV_FWD_CPChecks = 0
minConflictChecks   = 0

def backtrackingRecurse(gameState, sudokuConfig):
    """
    This is recursive function for backtracking.
    It returns True or False depending upon gameState and
    also the final gameState
    """

    empty, row, col = checkEmptyLocation(gameState, sudokuConfig)
    if not empty:
        return (True, gameState)

    global backtrackChecks
    for num in range(1, sudokuConfig[0]+1, 1):
        backtrackChecks += 1
        if isValidMove(gameState, sudokuConfig, row, col, num):
            gameState[row][col] = num
            success , gameState = backtrackingRecurse(gameState, sudokuConfig)
            if success:
                return (True, gameState)

            gameState[row][col] = 0

    return (False, gameState)

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    gameState, sudokuConfig = fileParse(filename)

    gameState = backtrackingRecurse(gameState, sudokuConfig)
    return (gameState, backtrackChecks)

def getMRVLocation(gameState, sudokuConfig):
    """
    This function returns the row and column number of the cell
    which has minimum remaining values.
    """

    constrainedRow = 0
    constrainedCol = 0
    minConstrain = sudokuConfig[0]
    cellAvailable = False

    global backtrackMRVChecks

    for row in range(sudokuConfig[0]):
        for col in range(sudokuConfig[0]):
            if gameState[row][col] == 0:
                cellAvailable = True
                validValue = 0
                for num in range(1, sudokuConfig[0]+1, 1):
                    #backtrackMRVChecks += 1
                    if isValidMove(gameState, sudokuConfig, row, col, num):
                        validValue += 1

                if validValue < minConstrain:
                    minConstrain = validValue
                    constrainedCol = col
                    constrainedRow = row

    if cellAvailable:
        return (cellAvailable, constrainedRow, constrainedCol)

    return (cellAvailable, constrainedRow, constrainedCol)


def backtrackingMRVRecurse(gameState, sudokuConfig):
    """
    This is recursive backtracking MRV function. Basically while doing backtracking, we choose
    the cell which has minimum remaining value.
    """

    empty, row, col = getMRVLocation(gameState, sudokuConfig)
    if not empty:
        return (True, gameState)

    global backtrackMRVChecks
    for num in range(1, sudokuConfig[0]+1, 1):
        backtrackMRVChecks += 1
        if isValidMove(gameState, sudokuConfig, row, col, num):
            gameState[row][col] = num
            success , gameState = backtrackingMRVRecurse(gameState, sudokuConfig)
            if success:
                return (True, gameState)

            gameState[row][col] = 0

    return (False, gameState)

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    gameState, sudokuConfig = fileParse(filename)

    gameState = backtrackingMRVRecurse(gameState, sudokuConfig)
    return (gameState, backtrackMRVChecks)


def MRV_FWDLocation(gameState, sudokuConfig):
    """
    This function returns the row and column number of the cell
    which has minimum remaining values.
    """

    constrainedRow = 0
    constrainedCol = 0
    minConstrain = sudokuConfig[0]
    cellAvailable = False

    global backtrackMRV_FWDChecks

    for row in range(sudokuConfig[0]):
        for col in range(sudokuConfig[0]):
            if gameState[row][col] == 0:
                cellAvailable = True
                validValue = 0
                for num in range(1, sudokuConfig[0]+1, 1):
                    #backtrackMRV_FWDChecks += 1
                    if isValidMove(gameState, sudokuConfig, row, col, num):
                        validValue += 1

                if validValue < minConstrain:
                    minConstrain = validValue
                    constrainedCol = col
                    constrainedRow = row

    if cellAvailable:
        return (cellAvailable, constrainedRow, constrainedCol)

    return (cellAvailable, constrainedRow, constrainedCol)

def backtrackingMRV_FWDRecurse(gameState, sudokuConfig, toExclude):
    """
    Here, we exclude the member from the domain of checks in the recurrence tree.
    For eg:- if i,j in the game is 4 is valid move, then in subsequence recurrence, we exclude 4
    from the domain of assigned possible numbers because those are not possible in the given row and column.

    """

    empty, row, col = MRV_FWDLocation(gameState, sudokuConfig)
    if not empty:
        return (True, gameState)

    global backtrackMRV_FWDChecks
    for num in range(1, sudokuConfig[0] + 1, 1):
        if num == toExclude:
            continue
        backtrackMRV_FWDChecks += 1
        if isValidMove(gameState, sudokuConfig, row, col, num):
            gameState[row][col] = num
            success , gameState = backtrackingMRV_FWDRecurse(gameState, sudokuConfig, num)
            if success:
                return (True, gameState)

            gameState[row][col] = 0

    return (False, gameState)


def MRV_FWD_CPLocation(gameState, sudokuConfig):
    """
    This function returns the row and column number of the cell
    which has minimum remaining values.
    """

    constrainedRow = 0
    constrainedCol = 0
    minConstrain = sudokuConfig[0]
    cellAvailable = False

    global backtrackMRV_FWD_CPChecks

    for row in range(sudokuConfig[0]):
        for col in range(sudokuConfig[0]):
            if gameState[row][col] == 0:
                cellAvailable = True
                validValue = 0
                for num in range(1, sudokuConfig[0]+1, 1):
                    backtrackMRV_FWD_CPChecks += 1
                    if isValidMove(gameState, sudokuConfig, row, col, num):
                        validValue += 1

                if validValue < minConstrain:
                    minConstrain = validValue
                    constrainedCol = col
                    constrainedRow = row

    if cellAvailable:
        return (cellAvailable, constrainedRow, constrainedCol)

    return (cellAvailable, constrainedRow, constrainedCol)

def backtrackingMRV_FWD_CPRecurse(gameState, sudokuConfig, toExclude):
    """
    Here, we exclude the member from the domain of checks in the recurrence tree.
    For eg:- if i,j in the game is 4 is valid move, then in subsequence recurrence, we exclude 4
    from the domain of assigned possible numbers because those are not possible in the given row and column.

    WHile doing this we also need to make sure that the remaining nodes have a working domain to take values from

    """

    empty, row, col = MRV_FWD_CPLocation(gameState, sudokuConfig)
    if not empty:
        return (True, gameState)

    exclusion = []
    exclusion.append(toExclude)

    global backtrackMRV_FWD_CPChecks

    for num in range(1, sudokuConfig[0] + 1, 1):
        backtrackMRV_FWD_CPChecks += (len(exclusion) + 1)
        for i in range(len(exclusion)):
            if (num == exclusion[i]):
                backtrackMRV_FWD_CPChecks += 1
                continue

        if isValidMove(gameState, sudokuConfig, row, col, num):
            gameState[row][col] = num
            success , gameState = backtrackingMRV_FWDRecurse(gameState, sudokuConfig, num)
            if success:
                return (True, gameState)

            gameState[row][col] = 0

    return (False, gameState)

def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    gameState, sudokuConfig = fileParse(filename)

    gameState = backtrackingMRV_FWD_CPRecurse(gameState, sudokuConfig, 0)
    return (gameState, backtrackMRV_FWDChecks)

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    gameState, sudokuConfig = fileParse(filename)

    gameState = backtrackingMRV_FWD_CPRecurse(gameState, sudokuConfig, 0)
    return (gameState, backtrackMRV_FWD_CPChecks)


def numConflicts(gameState, sudokuConfig, x, y):

    val = gameState[x][y]

    result = []
    for i in range(1, sudokuConfig[0]):
        if (i != y and gameState[x][i] == val):
            result.append([True])

    for i in range(1, sudokuConfig[0]):
        if (i != x and gameState[i][y] == val):
            result.append([True])

    return len(result)

def checkCompleted(gameState, sudokuConfig):
    isCompleted = True

    for i in range(sudokuConfig[0]):
        for j in range(sudokuConfig[0]):
            if gameState[i][j] == 0:
                isCompleted = False

    return isCompleted

def MinConflictFinder(gameState, sudokuConfig):
    """
    Here, we exclude the member from the domain of checks in the recurrence tree.
    For eg:- if i,j in the game is 4 is valid move, then in subsequence recurrence, we exclude 4
    from the domain of assigned possible numbers because those are not possible in the given row and column.

    """

    oldGameState = copy.deepcopy(gameState)
    global minConflictChecks

    iter = 0

    while (iter < 10000):

        if True == checkCompleted(gameState, sudokuConfig):
            return (True, gameState)

        row = random.randint(0, sudokuConfig[0] - 1)
        col = random.randint(0, sudokuConfig[0] - 1)

        if gameState[row][col] != 0 :
            continue

        conflicts = [0] * 13

        minConflictChecks += 1
        for num in range(1, sudokuConfig[0] + 1, 1):
            newGameState = copy.deepcopy(gameState)
            newGameState[row][col] = num
            conflicts[num] = numConflicts(newGameState, sudokuConfig, row, col)

        minConflictNum = 0;
        for i in range(1, sudokuConfig[0] + 1, 1):
            if (conflicts[minConflictNum] > conflicts[i]):
                minConflictNum = i

        gameState[row][col] = minConflictNum

        iter += 1
    return (False, gameState)

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    gameState, sudokuConfig = fileParse(filename)

    gameState = MinConflictFinder(gameState, sudokuConfig)
    return (gameState, minConflictChecks)