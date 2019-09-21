import curses
import curses.ascii
import dataclasses
import math
import time
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
        self.matrix_cursor_pos = Coordinate(0, 0)
        self.window_legend = None
        self.window_legend_alt = None
        self.window_game = None
        self.window_title_bar = None
        self.start_time = None

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

    def _create_title_bar(self):
        window_title_bar = curses.newwin(1, curses.COLS - 1)
        window_title_bar.addstr(self.level.title)
        window_title_bar.refresh()
        return window_title_bar

    def _clear_windows(self) -> None:
        if self.window_game is not None:
            self.window_game.clear()
            self.window_game.noutrefresh()
        if self.window_legend is not None:
            self.window_legend.clear()
            self.window_legend.noutrefresh()
        if self.window_legend_alt is not None:
            self.window_legend_alt.clear()
            self.window_legend_alt.noutrefresh()
        if self.window_title_bar is not None:
            self.window_title_bar.clear()
            self.window_title_bar.noutrefresh()
        curses.doupdate()

    def _init_windows(self) -> None:
        self._clear_windows()
        self.window_title_bar = self._create_title_bar()
        offset_y = 1
        legend_position_x = math.ceil(curses.COLS / 2)
        self.window_legend = self._create_legend_window(
            self.level.format_utd_ltr_regexes(), position=(offset_y, legend_position_x)
        )
        self.window_legend_alt = self._create_legend_window(
            self.level.format_dtu_rtl_regexes(),
            position=(offset_y, legend_position_x + self.window_legend.getmaxyx()[1]),
        )
        self.window_game = curses.newwin(
            self.matrix.str_height, self.matrix.str_width + 1, offset_y, 0
        )
        self.window_game.keypad(True)
        self._redraw_game()
        self.window_game.move(
            2 + (2 * self.matrix_cursor_pos.row), 4 + (4 * self.matrix_cursor_pos.col)
        )

    def _redraw_game(self) -> None:
        cur_pos_y, cur_pos_x = self.window_game.getyx()
        self.window_game.move(0, 0)
        self.window_game.addstr(str(self.matrix))
        self.window_game.refresh()
        self.window_game.move(cur_pos_y, cur_pos_x)

    def _handle_input(self, char: int) -> bool:
        cur_pos_y, cur_pos_x = self.window_game.getyx()
        try:
            if char == curses.KEY_RIGHT:
                if self.matrix_cursor_pos.col + 1 >= self.matrix.columns:
                    raise IndexError('Cursor got off the matrix')
                self.window_game.move(cur_pos_y, cur_pos_x + 4)
                self.matrix_cursor_pos.col += 1
            elif char == curses.KEY_LEFT:
                if self.matrix_cursor_pos.col - 1 < 0:
                    raise IndexError('Cursor got off the matrix')
                self.window_game.move(cur_pos_y, cur_pos_x - 4)
                self.matrix_cursor_pos.col -= 1
            elif char == curses.KEY_DOWN:
                if self.matrix_cursor_pos.row + 1 >= self.matrix.rows:
                    raise IndexError('Cursor got off the matrix')
                self.window_game.move(cur_pos_y + 2, cur_pos_x)
                self.matrix_cursor_pos.row += 1
            elif char == curses.KEY_UP:
                if self.matrix_cursor_pos.row - 1 < 0:
                    raise IndexError('Cursor got off the matrix')
                self.window_game.move(cur_pos_y - 2, cur_pos_x)
                self.matrix_cursor_pos.row -= 1
            elif char in (curses.KEY_ENTER, curses.ascii.NL):
                if self.level.check_matrix(self.matrix):
                    return True
            elif char == curses.KEY_RESIZE:
                curses.update_lines_cols()
                self._init_windows()
            elif curses.ascii.isprint(char):
                self.matrix[self.matrix_cursor_pos.row][self.matrix_cursor_pos.col] = chr(
                    char
                ).upper()
                self._redraw_game()
        except Exception:
            pass
        return False

    def _finished_level(self) -> None:
        curses.flash()
        curses.curs_set(0)
        success_offset_y = int(curses.LINES * (1 / 5))
        success_offset_x = int(curses.COLS * (1 / 5))
        success_text = f'Success! You\'ve finished "{self.level.title}" after {round(time.time() - self.start_time, 2)} seconds!\nPress {{ENTER}} to continue...'
        success_text_split = success_text.splitlines()
        success_width = len(max(success_text_split, key=len))
        success_length = len(success_text_split)
        success_box = curses.newwin(
            success_length + 2, success_width + 3, success_offset_y - 1, success_offset_x - 1
        )
        success_box.border()
        success_box.refresh()
        window_success = curses.newwin(
            success_length, success_width + 1, success_offset_y, success_offset_x
        )
        window_success.addstr(success_text.strip())
        window_success.refresh()
        char = window_success.getch()
        while char not in (curses.KEY_ENTER, curses.ascii.NL):
            char = window_success.getch()
        curses.curs_set(1)

    def play_level(self) -> int:
        self._init_windows()
        self.start_time = time.time()
        char = self.window_game.getch()
        while char != curses.ascii.ESC:
            if char == curses.KEY_NPAGE:
                return -1
            if char == curses.KEY_PPAGE:
                return 1
            if self._handle_input(char):
                self._finished_level()
                return 1
            char = self.window_game.getch()
        return 0
