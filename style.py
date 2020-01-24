from os import system
from termcolor import cprint,colored

COLOR = ['white', 'blue', 'green', 'red', 'cyan']

def clear():
    system('clear')

def color(number):
    if isinstance(number, int):
        if number <= 4:
            return COLOR[number]
        return 'yellow'
    if number == '⚐':
        return 'magenta'
    if number == '*':
        return 'red'
    return 'white'

def printGrid(grid):
    clear()
    columns_name = '  '
    grid_head = '  '
    row_intermediate = '  ╠═════'
    column_numbers = len(grid[0])
    row_numbers = len(grid)

    for i in range(column_numbers - 1):
        row_intermediate += '╬═════'
    for i in range(65, 65 + column_numbers):
        columns_name += f'   {chr(i)}  '
    for i in range(column_numbers):
        if i == 0:
            grid_head += '╔═════'
            continue
        grid_head += '╦═════'
    cprint(columns_name, 'blue')
    cprint(grid_head + '╗', 'yellow')

    for r in range(row_numbers):
        row = f'{colored(r, "blue")} '
        for i in range(column_numbers):
            row += f'{colored("║", "yellow")}  {colored(grid[r][i], color(grid[r][i]))}  '
        print(row + colored('║', 'yellow'))
        if r == row_numbers - 1:
            continue
        cprint(row_intermediate + '╣', 'yellow')
    cprint(grid_head.replace('╦','╩').replace('╔', '╚') + '╝', 'yellow')
