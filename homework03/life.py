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
        self.cell_height, self.cell_width = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [
            [random.randint(0, 1) if randomize else 0 for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return 

        for _ in range(self.cell_height):
            col = []
            for _ in range(self.cell_width):
                col.append(random.choice((0, 1)))
            grid.append(col)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x = cell[0]
        y = cell[1]
        lnx = len(self.curr_generation) - 1
        lny = len(self.curr_generation[0]) - 1
        cells = []
        if x != 0:
            cells.append(self.curr_generation[x - 1][y])
            if y != 0:
                cells.append(self.curr_generation[x - 1][y - 1])
            if y != lny:
                cells.append(self.curr_generation[x - 1][y + 1])
        if x != lnx:
            cells.append(self.curr_generation[x + 1][y])
            if y != 0:
                cells.append(self.curr_generation[x + 1][y - 1])
            if y != lny:
                cells.append(self.curr_generation[x + 1][y + 1])
        if y != 0:
            cells.append(self.curr_generation[x][y - 1])
        if y != lny:
            cells.append(self.curr_generation[x][y + 1])

        return cells

    def get_next_generation(self) -> Grid:
        grid = []
        for x in range(0, self.cell_height):
            col = []
            for y in range(0, self.cell_width):
                if (
                    sum(self.get_neighbours((x, y))) == 3
                    and self.curr_generation[x][y] == 0
                    or self.curr_generation[x][y] == 1
                    and (
                        sum(self.get_neighbours((x, y))) == 3
                        or sum(self.get_neighbours((x, y))) == 2
                    )
                ):
                    col.append(1)
                else:
                    col.append(0)
            grid.append(col)
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.is_changing and not self.is_max_generations_exceeded:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.save(pathlib.Path("glider-4-steps.txt"))
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(f"{filename}") as file:
            lines = file.readlines()
        for i in range(len(lines)):
            row = []
            for j in range(len(lines[0])):
                row.append(int(lines[i][j]))
            grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for _, line in enumerate(self.curr_generation):
                for _, e in enumerate(line):
                    f.write(str(e))
                f.write("\n")


if __name__ == "__main__":
    life = GameOfLife.from_file(pathlib.Path("glider.txt"))
    steps = 4  # задает количество итераций
    for _ in range(steps):
        life.step()
