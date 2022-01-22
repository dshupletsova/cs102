import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = True) -> Grid:
        grid = []
        if randomize is False:
            for i in range(self.rows):
                col = []
                for j in range(self.cols):
                    col.append(0)
                grid.append(col)
            return grid

        for i in range(self.rows):
            col = []
            for j in range(self.cols):
                col.append(random.choice((0, 1)))
            grid.append(col)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        cells = []
        if col > 0:
            cells.append(self.curr_generation[row][col - 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col - 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col - 1])
        if col < (self.cols - 1):
            cells.append(self.curr_generation[row][col + 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col + 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col + 1])
        if row > 0:
            cells.append(self.curr_generation[row - 1][col])
        if row < (self.rows - 1):
            cells.append(self.curr_generation[row + 1][col])
        return cells

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                if self.curr_generation[i][j] == 0:
                    if sum(neighbours) == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if sum(neighbours) < 2 or sum(neighbours) > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        if self.is_changing and not self.is_max_generations_exceeded:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.save(pathlib.Path("glider-4-steps.txt"))
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f = open(f"{filename}").readlines()
        grid = []
        for line in f:
            grid.append(list(map(int, list(line))))
        life = GameOfLife((len(grid), len(grid[0])))
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        f = open(f"{filename}", "w")
        for line in self.curr_generation:
            f.write("".join(list(map(str, line))))
            f.write("\n")
        f.close()
