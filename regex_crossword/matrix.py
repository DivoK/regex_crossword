import typing


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
        return len(str(self).splitlines()[1])

    @property
    def str_height(self) -> int:
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
