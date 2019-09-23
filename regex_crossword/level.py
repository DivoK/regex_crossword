import itertools
import re
import typing

from .matrix import Matrix

LevelDataType = typing.Dict[str, typing.Union[str, typing.List[str]]]


class Level:
    """
    Class that manages the static data of a level.
    """

    def __init__(self, level_data: LevelDataType):
        self.title = level_data.get('title')
        self.up_to_down_regexes = [
            re.compile(regex) for regex in level_data.get('up_to_down', [])
        ]
        self.down_to_up_regexes = [
            re.compile(regex) for regex in level_data.get('down_to_up', [])
        ]
        self.left_to_right_regexes = [
            re.compile(regex) for regex in level_data.get('left_to_right', [])
        ]
        self.right_to_left_regexes = [
            re.compile(regex) for regex in level_data.get('right_to_left', [])
        ]

    def create_matrix(self) -> Matrix:
        """
        Create a matrix coresponding in height and width to the level.

        :return: the created matrix
        :rtype: Matrix
        """
        return Matrix(
            len(max([self.left_to_right_regexes, self.right_to_left_regexes], key=len)),
            len(max([self.up_to_down_regexes, self.down_to_up_regexes], key=len)),
        )

    def check_matrix(self, mat: Matrix) -> bool:
        """
        Check if a given matrix has been validated against all regexes.

        :param mat: the matrix to validate.
        :type mat: Matrix
        :return: True if the matrix has been validated successfully, False otherwise.
        :rtype: bool
        """
        matrix_expected_row_len = len(
            max([self.left_to_right_regexes, self.right_to_left_regexes], key=len)
        )
        matrix_row_strings = [
            ''.join(mat[i][j] for j in range(mat.columns)) for i in range(mat.rows)
        ]
        if matrix_expected_row_len != len(matrix_row_strings):
            raise ValueError(
                f'Matrix with {len(matrix_row_strings)} rows is incompatible with level of {matrix_expected_row_len} rows.'
            )

        matrix_expected_column_len = len(
            max([self.up_to_down_regexes, self.down_to_up_regexes], key=len)
        )
        matrix_column_strings = [
            ''.join(mat[j][i] for j in range(mat.rows)) for i in range(mat.columns)
        ]
        if matrix_expected_column_len != len(matrix_column_strings):
            raise ValueError(
                f'Matrix with {len(matrix_column_strings)} columns is incompatible with level of {matrix_expected_column_len} columns.'
            )

        for row, utd_regex, dtu_regex in itertools.zip_longest(
            matrix_column_strings,
            self.up_to_down_regexes,
            self.down_to_up_regexes,
            fillvalue=re.compile(''),
        ):
            if (utd_regex.pattern and re.fullmatch(utd_regex, row) is None) or (
                dtu_regex.pattern and re.fullmatch(dtu_regex, row) is None
            ):
                return False

        for row, ltr_regex, rtl_regex in itertools.zip_longest(
            matrix_row_strings,
            self.left_to_right_regexes,
            self.right_to_left_regexes,
            fillvalue=re.compile(''),
        ):
            if (ltr_regex.pattern and re.fullmatch(ltr_regex, row) is None) or (
                rtl_regex.pattern and re.fullmatch(rtl_regex, row) is None
            ):
                return False

        return True

    def format_up_to_down_regexes(self) -> str:
        """
        Format a string listing all the regexes that will validate the columns from top to bottom.

        :return: the formatted string.
        :rtype: str
        """
        ret_str = 'Up -> Down:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.up_to_down_regexes)]
        )
        return ret_str.strip()

    def format_down_to_up_regexes(self) -> str:
        """
        Format a string listing all the regexes that will validate the columns from bottom to top.

        :return: the formatted string.
        :rtype: str
        """
        ret_str = 'Down -> Up:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.down_to_up_regexes)]
        )
        return ret_str.strip()

    def format_left_to_right_regexes(self) -> str:
        """
        Format a string listing all the regexes that will validate the rows from left to right.

        :return: the formatted string.
        :rtype: str
        """
        ret_str = 'Left -> Right:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.left_to_right_regexes)]
        )
        return ret_str.strip()

    def format_right_to_left_regexes(self) -> str:
        """
        Format a string listing all the regexes that will validate the rows from right to left.

        :return: the formatted string.
        :rtype: str
        """
        ret_str = 'Right -> Left:\n'
        ret_str += '\n'.join(
            [f'{i}: {regex.pattern}' for i, regex in enumerate(self.right_to_left_regexes)]
        )
        return ret_str.strip()

    def format_utd_ltr_regexes(self) -> str:
        """
        Format both `up_to_down` and `left_to_right` together (aka the standard checks).

        :return: concatenation of `up_to_down` and `left_to_right`.
        :rtype: str
        """
        format_list = []
        if any(regex.pattern for regex in self.up_to_down_regexes):
            format_list.append(self.format_up_to_down_regexes())
        if any(regex.pattern for regex in self.left_to_right_regexes):
            format_list.append(self.format_left_to_right_regexes())
        return '\n\n'.join(format_list).strip()

    def format_dtu_rtl_regexes(self) -> str:
        """
        Format both `down_to_up` and `right_to_left` together (aka the alternative checks).

        :return: concatenation of `down_to_up` and `right_to_left`.
        :rtype: str
        """
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
