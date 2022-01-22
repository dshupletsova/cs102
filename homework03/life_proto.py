import random
import typing as tp
from random import choice
from typing import List, Type

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

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if not randomize:
            return [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        else:
            return [
                [random.randint(0, 1) for i in range(self.cell_width)]
                for j in range(self.cell_height)

    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] != 1:
                    colour = "white"
                else:
                    colour = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colour),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

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


if __name__ == "__main__":
    game = GameOfLife(640, 480, 10, 1)
    game.run()
