import re
import json
import curses
import curses.ascii
import dataclasses
import typing

LevelDataType = typing.Dict[str, typing.List[str]]


@dataclasses.dataclass
class Coordinate:
    row: int
    col: int


class Matrix:
    def __init__(self, rows, columns):
        self.rows: int = rows
        self.columns: int = columns
        self._matrix: typing.List[typing.List[str]] = [
            ['\0' for _ in range(columns)] for _ in range(rows)
        ]

    def __getitem__(self, index) -> typing.List:
        return self._matrix[index]

    def __setitem__(self, index, value) -> None:
        self._matrix[index] = value

    @property
    def str_width(self) -> int:
        return len(str(self).splitlines()[0])

    @property
    def str_height(self) -> int:
        return len(str(self).splitlines())

    def __str__(self) -> str:
        strtab = ''
        strtab += '+' + '---+' * self.columns
        strtab += '\n'
        for row in self._matrix:
            strtab += '|'
            for cell in row:
                strtab += ' {} |'.format(cell if cell != '\0' else ' ')
            strtab += '\n'
            strtab += '+' + '---+' * self.columns
            strtab += '\n'
        return strtab.strip()


class Level:
    def __init__(self, name: str, level_data: LevelDataType):
        self.name = name
        self.row_regexes = [re.compile(regex) for regex in level_data['rows']]
        self.col_regexes = [re.compile(regex) for regex in level_data['columns']]

    @property
    def rows(self):
        return len(self.row_regexes)

    @property
    def columns(self):
        return len(self.col_regexes)

    def check_matrix(self, mat: Matrix) -> bool:
        with open('log.log', 'a') as log:
            log.write('===============\n')
            matrix_row_strings = [
                ''.join(mat[i][j] for j in range(mat.columns)) for i in range(mat.rows)
            ]
            matrix_colum_strings = [
                ''.join(mat[j][i] for j in range(mat.rows)) for i in range(mat.columns)
            ]
            log.write('lrr: ' + str(self.row_regexes))
            log.write('\n')
            log.write('lcr: ' + str(self.col_regexes))
            log.write('\n')
            log.write('mrs: ' + str(matrix_row_strings))
            log.write('\n')
            log.write('mcs: ' + str(matrix_colum_strings))
            log.write('\n')

            for row, regex in zip(matrix_row_strings, self.row_regexes):
                log.write(f'running {row} against {regex.pattern}\n')
                if re.fullmatch(regex, row) is None:
                    log.write(f'failed: {regex.pattern} :: {row}')
                    log.write('\n')
                    return False

            for col, regex in zip(matrix_colum_strings, self.col_regexes):
                log.write(f'running {col} against {regex.pattern}\n')
                if re.fullmatch(regex, col) is None:
                    log.write(f'failed: {regex.pattern} :: {col}')
                    log.write('\n')
                    return False
            log.write('True')
            log.write('\n')

            return True

    def format_column_regexes(self) -> str:
        ret_str = 'Columns:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.col_regexes)]
        )
        return ret_str.strip()

    def format_rows_regexes(self) -> str:
        ret_str = 'Rows:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.row_regexes)]
        )
        return ret_str.strip()


def main(stdscr):
    with open('crossword.json') as cw:
        crosswords: typing.Dict = json.load(cw)
    for level_name, level_data in crosswords.items():
        level = Level(level_name, level_data)
        formatted_cols = level.format_column_regexes()
        formatted_rows = level.format_rows_regexes()
        legend_width = (
            len(max(formatted_cols.splitlines() + formatted_rows.splitlines(), key=len)) + 1
        )
        legend_height = len(formatted_cols + formatted_rows) + 1
        legend_win = curses.newwin(
            # legend_height, legend_width, 0, curses.COLS - legend_width - 1
            legend_height,
            legend_width,
            0,
            int(curses.COLS / 2),  # - legend_width - 1
        )
        legend_win.addstr(formatted_cols + '\n\n' + formatted_rows)
        legend_win.refresh()

        mat = Matrix(len(level_data['rows']), len(level_data['columns']))
        matrix_location = Coordinate(0, 0)

        begin_x = 0
        begin_y = 0
        height = mat.str_height
        width = mat.str_width + 1
        win = curses.newwin(height, width, begin_y, begin_x)
        win.keypad(True)
        win.addstr(str(mat))
        win.move(1, 2)
        win.refresh()

        char = win.getch()
        while char != curses.ascii.ESC:
            cur_pos_y, cur_pos_x = win.getyx()
            try:
                if char == curses.KEY_RIGHT:
                    win.move(cur_pos_y, cur_pos_x + 4)
                    matrix_location.col += 1
                elif char == curses.KEY_LEFT:
                    win.move(cur_pos_y, cur_pos_x - 4)
                    matrix_location.col -= 1
                elif char == curses.KEY_DOWN:
                    win.move(cur_pos_y + 2, cur_pos_x)
                    matrix_location.row += 1
                elif char == curses.KEY_UP:
                    win.move(cur_pos_y - 2, cur_pos_x)
                    matrix_location.row -= 1
                elif char in (curses.KEY_ENTER, curses.ascii.NL):
                    if level.check_matrix(mat):
                        break
                elif curses.ascii.isprint(char):
                    mat[matrix_location.row][matrix_location.col] = chr(char).upper()
                    win.move(0, 0)
                    win.addstr(str(mat))
                    win.refresh()
                    win.move(cur_pos_y, cur_pos_x)
            except Exception:
                pass
            char = win.getch()
        del win


if __name__ == '__main__':
    curses.wrapper(main)
