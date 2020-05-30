from rs import tGrid
import os
class sudokuSolver:
    def __init__(self, grid):
        #checks if the grid is indeed a grid, and if it is long enough,
        #if conditions not met, it will return an error.
        if type(grid)=='list':
            self.grid=grid
            self.original=grid
        else:
            self.grid=self.stringToGrid(grid)
            self.original=self.stringToGrid(grid)

        self.stack=[]
        self.solveSudoku()
    # loops through each cell to get next one
    def getGrid(self):
        return self.grid
    def getOrigin(self):
        return self.original
    def printGrid(self):
        for x in self.grid:
            print(x)
    #if the input is not in grid format, this converts it
    def stringToGrid(self, str):
        out = []
        k = 0
        for i in range(0, 9):
            out.append([])
            for j in range(0, 9):
                out[i].append(int(str[k]))
                k += 1
        return out

    def nextCell(self, i, j):
        # first loop checks for the next cell with the given
        for x in range(i, 9):
            for y in range(j, 9):
                if self.grid[x][y] == 0:
                    return x, y
        # if the first loops don't return a value, check the whole thing for a cell
        for x in range(0, 9):
            for y in range(0, 9):
                if self.grid[x][y] == 0:
                    return x, y
        # returns a null value if the whole sheet is full
        return -1, -1

    # checks that the number n is unique with respect to its row
    def rowOk(self, n, i):
        self.stack.append((n, 'row', i))
        for x in range(9):
            if n == self.grid[i][x]:
                return False
        return True

    # checks that the number n is unique with respect to its column
    def colOk(self, n, j):
        self.stack.append((n, 'col', j))
        for x in range(9):
            if n == self.grid[x][j]:
                return False
        return True

    # checks that n is unique with respect to its section
    # section being the 3x3 sub-box it is located in
    def sectionOk(self, i, j, n):
        # using floor division, the top-left number of each 3x3 is found
        topX, topY = 3 * (i // 3), 3 * (j // 3)
        for x in range(topX, topX + 3):
            for y in range(topY, topY + 3):
                if self.grid[x][y] == n:
                    return False
        return True
        print('Checking section starting at(%d,%d)...\n' % (topX, topY))

    # if n is unique to its row, column and 3x3, then it is a valid number
    def isValid(self, i, j, n):
        if self.rowOk(n, i):
            if self.colOk(n, j):
                if self.sectionOk(i, j, n):
                    print('%d at %d, %d is valid!\n' % (n, i, j))
                    return True

        else:
            print('%d at %d, %d is invalid!\n' % (n, i, j))
            return False

    # manipulates the grid recursively until it is finished - until all spots are filled
    # doesn't return grid when it is done, but over time manipulates grid.
    def solveSudoku(self, i=0, j=0):
        # ensures all spots are filled
        i, j = self.nextCell(i, j)
        if i == -1:
            return True
        # tries each number to see if it is valid, if it is valid, it keeps it, if it isn't
        # it loops over again with the next number
        for n in range(1, 10):
            if self.isValid(i, j, n):
                self.grid[i][j] = n
                if self.solveSudoku(i, j):
                    return True
                self.grid[i][j] = 0
        return False

    def saveAnswers(self):
        fName = 'SudokuAnswers.txt'
        path = os.getcwd()
        file = path + r'\\' + fName
        if fName in os.listdir(path):
            fhand = open(file, 'a')
        else:
            fhand = open(file, 'x')
        for x in range(len(self.grid)):
            fhand.write("%s   ->   %s\n" % (self.original[x],self.grid[x]))
        fhand.write('\n\n\n')
        print("Answer also saved to: %s in %s" % (os.path.basename(os.path.normpath(path)), fName))
        fhand.close()








def runIt():
    oneMore=True
    while oneMore:
        grid = input("Enter the Sudoku board as one long number (use zeros in place of blanks), then hit enter...\n\n ->")
        if len(grid)==81:
            temp=sudokuSolver(grid)
            for x in temp.getGrid():
                print(x)
            temp.saveAnswers()


        else:
            if len(grid)>81:
                print("You entered too many digits, you gave %d when it should be 81\n .... \n"%len(grid))
                print("Please try again\n")
            else:
                print("You did not enter enough digits, you gave %d when it should be 81\n .... \n" % len(grid))
                print("Please try again\n")
        if input('\nClick \"ENTER\" to continue again\n\n'):
            pass

runIt()
