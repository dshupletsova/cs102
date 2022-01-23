import copy
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
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = True) -> Grid:
        grid = []
        if randomize is False:
            for _ in range(self.rows):
                col = []
                for _ in range(self.cols):
                    col.append(0)
                grid.append(col)
            return grid

        for _ in range(self.rows):
            col = []
            for _ in range(self.cols):
                col.append(random.choice((0, 1)))
            grid.append(col)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        nbours = []
        x, y = cell[0], cell[1]

        if x - 1 >= 0:
            if y - 1 >= 0:
                nbours.append(self.curr_generation[x - 1][y - 1])
            nbours.append(self.curr_generation[x - 1][y])
            if self.rows > y + 1:
                nbours.append(self.curr_generation[x - 1][y + 1])
        if 0 <= y - 1:
            nbours.append(self.curr_generation[x][y - 1])
        if self.rows > y + 1:
            nbours.append(self.curr_generation[x][y + 1])
        if self.cols > x + 1:
            if 0 <= y - 1:
                nbours.append(self.curr_generation[x + 1][y - 1])
            nbours.append(self.curr_generation[x + 1][y])
            if self.rows > y + 1:
                nbours.append(self.curr_generation[x + 1][y + 1])
        return nbours

    def get_next_generation(self) -> Grid:
        grid = []
        for y in range(0, self.cols):
            row = []
            for x in range(0, self.rows):
                if sum(self.get_neighbours((y, x))) != 3 and (
                    self.curr_generation[y][x] != 1 or sum(self.get_neighbours((y, x))) != 2
                ):
                    row.append(0)
                else:
                    row.append(1)
            grid.append(row)
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.prev_generation = copy.deepcopy(self.curr_generation)
        nextgen = self.get_next_generation()
        self.curr_generation = nextgen
        self.generations = self.generations + 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as f:
            f.readlines()
            grid = [list(map(int, list(line))) for line in f]
            life = GameOfLife((len(grid), len(grid[0])))
            life.curr_generation = grid
            return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        with open(filename, "w") as f:
            for _ in self.curr_generation:
                for t in _:
                    f.write(str(t) + "\n")
