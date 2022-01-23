import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 50, speed: int = 1) -> None:
        super().__init__(life)

        # параметры игрового поля
        self.width = 500
        self.height = 500
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.pause = False

    def draw_lines(self) -> None:
        for j in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, j), (self.width, j))
        for i in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (i, 0), (i, self.height))

    def draw_grid(self) -> None:
        for x in range(0, self.height, self.cell_size):
            for y in range(0, self.width, self.cell_size):
                if self.life.curr_generation[x // self.cell_size][y // self.cell_size] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (y, x, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (y, x, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.life.create_grid(True)

        running = True
        paused = False
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        paused = not paused

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = [coord // self.cell_size for coord in event.pos]
                        if self.life.curr_generation[y][x] == 0:
                            self.life.curr_generation[y][x] = 1
                        else:
                            self.life.curr_generation[y][x] = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = [coord // self.cell_size for coord in event.pos]
                    if self.life.curr_generation[y][x] != 0:
                        self.life.curr_generation[y][x] = 0
                    else:
                        self.life.curr_generation[y][x] = 1

            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()

            if not paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
