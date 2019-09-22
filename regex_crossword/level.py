import re
import typing

from .matrix import Matrix

LevelDataType = typing.Dict[str, typing.Union[str, typing.List[str]]]


class Level:
    def __init__(self, level_data: LevelDataType):
        self.title = level_data.get('title')
        self.up_to_down_regexes = [re.compile(regex) for regex in level_data['up_to_down']]
        self.down_to_up_regexes = [re.compile(regex) for regex in level_data['down_to_up']]
        self.left_to_right_regexes = [
            re.compile(regex) for regex in level_data['left_to_right']
        ]
        self.right_to_left_regexes = [
            re.compile(regex) for regex in level_data['right_to_left']
        ]

    def create_matrix(self) -> Matrix:
        return Matrix(
            len(max([self.left_to_right_regexes, self.right_to_left_regexes], key=len)),
            len(max([self.up_to_down_regexes, self.down_to_up_regexes], key=len)),
        )

    def check_matrix(self, mat: Matrix) -> bool:
        matrix_row_strings = [
            ''.join(mat[i][j] for j in range(mat.columns)) for i in range(mat.rows)
        ]
        matrix_colum_strings = [
            ''.join(mat[j][i] for j in range(mat.rows)) for i in range(mat.columns)
        ]

        for row, utd_regex, dtu_regex in zip(
            matrix_colum_strings, self.up_to_down_regexes, self.down_to_up_regexes
        ):
            if (utd_regex.pattern and re.fullmatch(utd_regex, row) is None) or (
                dtu_regex.pattern and re.fullmatch(dtu_regex, row) is None
            ):
                return False

        for row, ltr_regex, rtl_regex in zip(
            matrix_row_strings, self.left_to_right_regexes, self.right_to_left_regexes
        ):
            if (ltr_regex.pattern and re.fullmatch(ltr_regex, row) is None) or (
                rtl_regex.pattern and re.fullmatch(rtl_regex, row) is None
            ):
                return False

        return True

    def format_up_to_down_regexes(self) -> str:
        ret_str = 'up_to_down:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.up_to_down_regexes)]
        )
        return ret_str.strip()

    def format_down_to_up_regexes(self) -> str:
        ret_str = 'down_to_up:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.down_to_up_regexes)]
        )
        return ret_str.strip()

    def format_left_to_right_regexes(self) -> str:
        ret_str = 'left_to_right:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.left_to_right_regexes)]
        )
        return ret_str.strip()

    def format_right_to_left_regexes(self) -> str:
        ret_str = 'right_to_left:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.right_to_left_regexes)]
        )
        return ret_str.strip()

    def format_utd_ltr_regexes(self) -> str:
        format_list = []
        if any(regex.pattern for regex in self.up_to_down_regexes):
            format_list.append(self.format_up_to_down_regexes())
        if any(regex.pattern for regex in self.left_to_right_regexes):
            format_list.append(self.format_left_to_right_regexes())
        return '\n\n'.join(format_list).strip()

    def format_dtu_rtl_regexes(self) -> str:
        format_list = []
        if any(regex.pattern for regex in self.down_to_up_regexes):
            format_list.append(self.format_down_to_up_regexes())
        if any(regex.pattern for regex in self.right_to_left_regexes):
            format_list.append(self.format_right_to_left_regexes())
        return '\n\n'.join(format_list).strip()

    def __str__(self) -> str:
        format_list = []
        if any(regex.pattern for regex in self.up_to_down_regexes):
            format_list.append(self.format_up_to_down_regexes())
        if any(regex.pattern for regex in self.down_to_up_regexes):
            format_list.append(self.format_down_to_up_regexes())
        if any(regex.pattern for regex in self.left_to_right_regexes):
            format_list.append(self.format_left_to_right_regexes())
        if any(regex.pattern for regex in self.right_to_left_regexes):
            format_list.append(self.format_right_to_left_regexes())
        return '\n\n'.join(format_list).strip()
