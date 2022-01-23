from copy import deepcopy
from random import choice, randint, seed
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    col, x, y = len(grid[0]), coord[0], coord[1]
    num = choice((0, 1))
    if x - 1 != 0 and y + 1 != col - 1 and num == 1 or x - 1 == 0 and y + 1 != col - 1:
        grid[x][y + 1] = " "
    elif x - 1 != 0 and y + 1 != col - 1 and num == 0 or x - 1 != 0 and y + 1 == col - 1:
        grid[x - 1][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True):
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for _, j in enumerate(empty_cells):
        grid = remove_wall(grid, j)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    possibles = []
    exits = []
    for i in range(0, len(grid)):
        possibles.append([0, i])
        possibles.append([i, 0])
        possibles.append([len(grid) - 1, i])
        possibles.append([i, len(grid) - 1])
    for j in range(len(possibles)):
        x, y = possibles[j][0], possibles[j][1]
        if grid[x][y] == "X" and (x, y) not in exits:
            exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    R, C = len(grid), len(grid[0])
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] != k:
                continue
            if x > 0 and grid[x - 1][y] == 0:
                grid[x - 1][y] = k + 1
            if y > 0 and grid[x][y - 1] == 0:
                grid[x][y - 1] = k + 1
            if x < R - 1 and grid[x + 1][y] == 0:
                grid[x + 1][y] = k + 1
            if y < C - 1 and grid[x][y + 1] == 0:
                grid[x][y + 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    xx, yy = exit_coord[0], exit_coord[1]
    short_path = [(x, y)]
    k = int(grid[x][y]) + 1
    while k != 1:
        k -= 1
        if 1 < 0 or grid[x - 1][y] != k - 1:
            if x + 1 < len(grid) and grid[x + 1][y] == k - 1:
                grid[x + 1][y] = k + 1
                x += 1
                short_path.append((x, y))
                continue
            if y - 1 >= 0 and grid[x][y - 1] == k - 1:
                grid[x][y - 1] = k + 1
                y -= 1
                short_path.append((x, y))
                continue
            if y + 1 < len(grid[x]) and grid[x][y + 1] == k - 1:
                grid[x][y + 1] = k + 1
                y += 1
                short_path.append((x, y))
                continue
            continue
        grid[x - 1][y] = k + 1
        x -= 1
        short_path.append((x, y))
    if len(short_path) != grid[xx][yy]:
        grid[short_path[-1][0]][short_path[-1][1]] = " "
        short_path.pop(len(short_path) - 1)
        shortest_path(grid, exit_coord)
    return short_path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == len(grid) - 1)
        or (x == len(grid) - 1 and y == 0)
        or (x == len(grid) - 1 and y == len(grid))
    ):
        return True
    if y == 0 and grid[x][y + 1] == "■":
        return True
    if y == len(grid) - 1 and grid[x][y - 1] == "■":
        return True
    if x == 0 and grid[x + 1][y] == "■":
        return True
    if x == len(grid) - 1 and grid[x - 1][y] == "■":
        return True
    return False


def solve_maze(grid: List[List[Union[str, int]]]):
    """
    :param grid:
    :return:
    """
    coord = get_exits(grid)
    if len(coord) == 1:
        return grid, coord[0]
    if not encircled_exit(grid, coord[0]) and not encircled_exit(grid, coord[1]):
        for x, row in enumerate(grid):
            for y, _ in enumerate(row):
                if grid[x][y] == " ":
                    grid[x][y] = 0
        grid[coord[0][0]][coord[0][1]], grid[coord[1][0]][coord[1][1]] = 1, 0
        k = 1
        while grid[coord[1][0]][coord[1][1]] == 0:
            grid = make_step(grid, k)
            k += 1
        path = shortest_path(grid, coord[1])
        for x, row in enumerate(grid):
            for y, _ in enumerate(row):
                if grid[x][y] != " " and grid[x][y] != "■":
                    grid[x][y] = " "
        return grid, path
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
