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
        self.grid = self.create_grid(randomize=False)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        if randomize is False:
            for _ in range(self.cell_height):
                col = []
                for _ in range(self.cell_width):
                    col.append(0)
                grid.append(col)
            return grid
        for _ in range(self.cell_height):
            col = []
            for _ in range(self.cell_width):
                col.append(random.choice((0, 1)))
            grid.append(col)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for y in range(1, self.height, self.cell_size):
            for x in range(1, self.width, self.cell_size):
                if self.grid[y // self.cell_size][x // self.cell_size] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x, y, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x, y, self.cell_size - 1, self.cell_size - 1),
                    )

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
        updated_grid = []
        for y in range(0, self.height, self.cell_size):
            row = []
            for x in range(0, self.width, self.cell_size):
                if sum(self.get_neighbours((y, x))) == 3 or (
                    self.grid[y // self.cell_size][x // self.cell_size] == 1
                    and sum(self.get_neighbours((y, x))) == 2
                ):
                    row.append(1)
                else:
                    row.append(0)
            updated_grid.append(row)
        self.grid = updated_grid
        return self.grid


if __name__ == "__main__":
    life = GameOfLife()
    life.run()
