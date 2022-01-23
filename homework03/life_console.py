import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cell = "*" if grid[i][j] == 1 else " "
                screen.addch(i + 1, j + 1, cell)

    def run(self) -> None:
        window = curses.initscr()
        game_running = True
        while game_running:
            self.draw_grid(window)
            self.draw_borders(window)
            self.life.step()
            window.refresh()
            curses.napms(150)
        curses.endwin()


life = GameOfLife((24, 80), max_generations=50)
ui = Console(life)
ui.run()
