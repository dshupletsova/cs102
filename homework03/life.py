import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for i in range(self.cols)] for i in range(self.rows)]
        else:
            grid = [[0 for i in range(self.cols)] for i in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell):
        new_list = []
        y, x = cell[0], cell[1]
        if 0 < y:
            new_list.append(self.grid[y - 1][x])
        if y < self.cell_height - 1:
            new_list.append(self.grid[y + 1][x])
        if x > 0:
            new_list.append(self.grid[y][x - 1])
        if x < self.cell_width - 1:
            new_list.append(self.grid[y][x + 1])
        if y > 0 and x > 0:
            new_list.append(self.grid[y - 1][x - 1])
        if y > 0 and x < self.cell_width - 1:
            new_list.append(self.grid[y - 1][x + 1])
        if y < self.cell_height - 1 and x > 0:
            new_list.append(self.grid[y + 1][x - 1])
        if y < self.cell_height - 1 and x < self.cell_width - 1:
            new_list.append(self.grid[y + 1][x + 1])
        return new_list

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = self.get_neighbours((i, j))
                if self.grid[i][j] == 0:
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
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        if self.prev_generation != self.curr_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename) as inp:
            grid = [[int(cell) for cell in row.strip()] for row in inp]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as outp:
            for i in self.curr_generation:
                stroka = ""
                for j in i:
                    stroka += str(j)
                outp.write(stroka + "\n")
