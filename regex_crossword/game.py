import math
import curses
import curses.ascii
import dataclasses
import typing

from .level import Level


@dataclasses.dataclass
class Coordinate:
    row: int
    col: int


class Game:
    def __init__(self, level: Level):
        self.level = level
        self.matrix = level.create_matrix()
        self.cursor_pos = Coordinate(0, 0)
        self.window_legend = None
        self.window_legend_alt = None
        self.window_game = None

    def _create_legend_window(self, legend_str: str, *, position: typing.Tuple[int] = None):
        if not legend_str:
            return
        if position is None:
            position = (0, math.ceil(curses.COLS / 2))
        legend_str_split = legend_str.splitlines()
        legend_width = len(max(legend_str_split, key=len)) + 1
        legend_height = len(legend_str_split)
        window_legend = curses.newwin(legend_height, legend_width, *position)
        window_legend.addstr(legend_str)
        window_legend.refresh()
        return window_legend

    def _init_windows(self) -> None:
        legend_position_y = 0
        legend_position_x = math.ceil(curses.COLS / 2)
        self.window_legend = self._create_legend_window(
            self.level.format_utd_ltr_regexes(),
            position=(legend_position_y, legend_position_x),
        )
        self.window_legend_alt = self._create_legend_window(
            self.level.format_dtu_rtl_regexes(),
            position=(legend_position_y, legend_position_x + self.window_legend.getmaxyx()[1]),
        )
        self.window_game = curses.newwin(self.matrix.str_height, self.matrix.str_width + 1)
        self.window_game.keypad(True)
        self.redraw_game()
        self.window_game.move(1, 2)

    def redraw_game(self) -> None:
        cur_pos_y, cur_pos_x = self.window_game.getyx()
        self.window_game.move(0, 0)
        self.window_game.addstr(str(self.matrix))
        self.window_game.refresh()
        self.window_game.move(cur_pos_y, cur_pos_x)

    def handle_input(self, char: int) -> bool:
        cur_pos_y, cur_pos_x = self.window_game.getyx()
        try:
            if char == curses.KEY_RIGHT:
                self.window_game.move(cur_pos_y, cur_pos_x + 4)
                self.cursor_pos.col += 1
            elif char == curses.KEY_LEFT:
                self.window_game.move(cur_pos_y, cur_pos_x - 4)
                self.cursor_pos.col -= 1
            elif char == curses.KEY_DOWN:
                self.window_game.move(cur_pos_y + 2, cur_pos_x)
                self.cursor_pos.row += 1
            elif char == curses.KEY_UP:
                self.window_game.move(cur_pos_y - 2, cur_pos_x)
                self.cursor_pos.row -= 1
            elif char in (curses.KEY_ENTER, curses.ascii.NL):
                if self.level.check_matrix(self.matrix):
                    return True
            elif curses.ascii.isprint(char):
                self.matrix[self.cursor_pos.row][self.cursor_pos.col] = chr(char).upper()
                self.redraw_game()
        except Exception:
            pass
        return False

    def play_level(self) -> None:
        self._init_windows()
        char = self.window_game.getch()
        while char != curses.ascii.ESC:
            if self.handle_input(char):
                break
            char = self.window_game.getch()
