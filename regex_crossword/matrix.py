import typing


class Matrix:
    """
    Class that stores a matrix (list of lists).
    """

    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self._matrix: typing.List[typing.List[str]] = [
            ['\0' for _ in range(columns)] for _ in range(rows)
        ]  # The underlying matrix.

    def __getitem__(self, index) -> typing.List:
        return self._matrix[index]

    def __setitem__(self, index, value) -> None:
        self._matrix[index] = value

    @property
    def str_width(self) -> int:
        """
        Return the maximum width of str(self).

        :return: maximum width of str(self).
        :rtype: int
        """
        return len(max(str(self).splitlines(), key=len))

    @property
    def str_height(self) -> int:
        """
        Return the height of str(self).

        :return: height of str(self).
        :rtype: int
        """
        return len(str(self).splitlines())

    def __str__(self) -> str:
        strtab = ''
        strtab += '    ' + '   '.join(str(i) for i in range(self.columns)) + '\n'
        strtab += '  +' + '---+' * self.columns
        strtab += '\n'
        for i, row in enumerate(self._matrix):
            strtab += f'{i} |'
            for cell in row:
                strtab += ' {} |'.format(cell if cell != '\0' else ' ')
            strtab += '\n'
            strtab += '  +' + '---+' * self.columns
            strtab += '\n'
        return strtab.rstrip()
