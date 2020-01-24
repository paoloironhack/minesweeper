import random, time, copy
from termcolor import cprint,colored
import style
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# import stdarray

#place bomb in random places in the grid, if random lands on an previous bomb, it loops again
def placeBomb(grid):
    while True:
        if not grid[random.randint(0, len(grid) - 1)][random.randint(0, len(grid[0]) - 1)] == '*':
            grid[random.randint(0, len(grid) - 1)][random.randint(0, len(grid[0]) - 1)] = '*'
            return

#adds to the grid numbers which represent the number of bombs in adjacent spaces
def updateValues(row_n, col, grid):
    #Row above.
    if row_n - 1 > -1:
        row = grid[row_n - 1]
        if col - 1 > -1:
            if not row[col - 1] == '*':
                row[col - 1] += 1
        if not row[col] == '*':
            row[col] += 1
        if len(grid[0]) > col + 1: 
            if not row[col + 1] == '*':
                row[col + 1] += 1
    #Same row.    
    row = grid[row_n]
    if col - 1 > -1:
        if not row[col - 1] == '*':
            row[col - 1] += 1
    if len(grid[0]) > col + 1:
        if not row[col + 1] == '*':
            row[col + 1] += 1
    #Row below.
    if len(grid) > row_n + 1:
        row = grid[row_n + 1]
        if col - 1 > -1:
            if not row[col - 1] == '*':
                row[col - 1] += 1
        if not row[col] == '*':
            row[col] += 1
        if len(grid[0]) > col + 1:
            if not row[col + 1] == '*':
                row[col + 1] += 1

def checkZeros(shown_grid, solution_grid, row, col):
    oldGrid = copy.deepcopy(shown_grid)

    zeroProcedure(row, col, shown_grid, solution_grid)

    while oldGrid != shown_grid:
        oldGrid = copy.deepcopy(shown_grid)
        for row in range(len(shown_grid)):
            for col in range(len(shown_grid[0])):
                if shown_grid[row][col] == 0:
                    zeroProcedure(row, col, shown_grid, solution_grid)
        if oldGrid == shown_grid:
            return

def zeroProcedure(row_n, col_n, shown_grid, solution_grid):
    #Row above
    if row_n-1 > -1:
        row = shown_grid[row_n-1]
        if col_n-1 > -1: 
            row[col_n-1] = solution_grid[row_n -1 ][col_n -1]
        row[col_n] = solution_grid[row_n - 1][col_n]
        if len(shown_grid[0]) > col_n + 1: 
            row[col_n+1] = solution_grid[row_n - 1][col_n + 1]
    #Same row
    row = shown_grid[row_n]
    if col_n - 1 > -1: 
        row[col_n-1] = solution_grid[row_n][col_n -1]
    if len(shown_grid[0]) > col_n+1: 
        row[col_n+1] = solution_grid[row_n][col_n + 1]
    #Row below
    if len(shown_grid) > row_n+1:
        row = shown_grid[row_n+1]
        if col_n-1 > -1: 
            row[col_n-1] = solution_grid[row_n + 1][col_n - 1]
        row[col_n] = solution_grid[row_n + 1][col_n]
        if len(shown_grid[0]) > col_n+1: 
            row[col_n+1] = solution_grid[row_n + 1][col_n + 1]

def playAgain(start_time):
    print('Time: ' + str(round(time.time() - start_time)) + 's')
    while True:
        playBla = input('Play again? (Y/N): ').lower()
        if playBla == 'y':
            return 1
        if playBla != 'n':
            cprint('Choice not supported, please type (Y/N)!', 'red')
            continue
        cprint('Thank you for playing!', 'yellow')
        quit()

def play(solution_grid, shown_grid, mines):
    start_time = time.time()
    while True:
        style.printGrid(shown_grid)
        row, col = choose(solution_grid, shown_grid)
        
        if solution_grid[row][col] == '*' and shown_grid[row][col] != '⚐':
            style.printGrid(solution_grid)
            print(f"You DEAD {colored('Looser!', 'red', 'on_cyan')}")
            if playAgain(start_time) == 1:
                return 1
        if shown_grid[row][col] != '⚐':
            shown_grid[row][col] = solution_grid[row][col]
        if solution_grid[row][col] == 0 and shown_grid[row][col] != '⚐':
            checkZeros(shown_grid, solution_grid, row, col)

        squaresLeft = 0
        for row in shown_grid:
            squaresLeft += row.count(' ') + row.count('⚐')

        if squaresLeft == mines:
            style.printGrid(solution_grid)
            print('You win!')
            if playAgain(start_time) == 1:
                return 1

def choose(solution_grid, shown_grid):
    letters = [chr(i) for i in range(97, 97 + len(shown_grid[0]))]
    numbers = [str(i) for i in range(len(shown_grid))]

    #Loop in case of invalid entry.
    while True:
        chosen = input('Choose a cell (eg. B2) or place a marker (eg. mB2): ').lower()
        if len(chosen) == 3 and chosen[0] == 'm' and chosen[1] in letters and chosen[2] in numbers:
            if shown_grid[int(chosen[2])][ord(chosen[1])-97] != ' ':
                print('You cannot put a marker on an already shown cell')
                continue
            shown_grid[int(chosen[2])][ord(chosen[1])-97] = '⚐'
            return (int(chosen[2]), ord(chosen[1])-97)
        elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers: 
            return (int(chosen[1]), ord(chosen[0])-97)


def main():
    rows = 10
    columns = 10
    mines = 10
    choice = ''

    style.clear()
    while choice != 'P' and choice != 'I':
        print(f'''Welcome to {colored("MINESWEEPER", "red", "on_cyan")} 1.0!!
Created by {colored('Victor Hugo AIZPURUA', 'red')}
For instructions, type '{colored("I", "blue")}'
To play, type '{colored("P", "green")}'

        ''')

        choice = input("What's your choice?: ").upper()

        if choice == 'I':
            style.clear()
            cprint(open('instructions.txt', 'r').read(), 'blue')
            input('Press [enter] when ready to play. ')            
        elif choice != 'P':
            style.clear()
            continue
        while True:
            solution_grid = [[0 for j in range(rows)] for i in range(columns)]
            for n in range (mines):
                placeBomb(solution_grid)
            for row in range(rows):
                for column in range(columns):
                    if solution_grid[row][column] == '*':
                        updateValues(row, column, solution_grid)
            
            shown_grid = [[' ' for j in range(rows)] for i in range(columns)]
            play(solution_grid, shown_grid, mines)

main()