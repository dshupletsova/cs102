import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    """отрисовка и запуск игры"""

    def __init__(self, game_life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(game_life)
        self.cell_size = cell_size
        self.speed = speed
        self.height, self.width = (self.life.rows * self.cell_size, self.life.cols * self.cell_size)
        self.screen = pygame.display.set_mode((self.height, self.width))

    def draw_lines(self) -> None:
        """Отобразить сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, x), (self.height, x))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (y, 0), (y, self.width))

    def draw_grid(self) -> None:
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 0:
                    color = "white"
                else:
                    color = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size],
                )

    def run(self) -> None:
        """запускаем игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    break
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    x, y = pygame.mouse.get_pos()
                                    prev_cell_state = self.life.curr_generation[
                                        x // self.cell_size
                                    ][y // self.cell_size]
                                    self.life.curr_generation[x // self.cell_size][
                                        y // self.cell_size
                                    ] = (0 if prev_cell_state == 1 else 1)
                                    self.draw_grid()
                                    self.draw_lines()
                                    pygame.display.flip()
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((30, 30))
    gui = GUI(life)
    gui.run()
