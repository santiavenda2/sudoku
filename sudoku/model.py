
from UserDict import IterableUserDict

EMPTY_CELL_CHARACTER = '.'


class SudokuTable(IterableUserDict):

    COLUMN_SEPARATOR = "| "

    ROW_SEPARATOR = "+-------+-------+-------+\n"

    def read_from_line(self, line):
        assert len(line) == 81
        for i, v in enumerate(line):
            if v != EMPTY_CELL_CHARACTER:
                self[(i / 9, i % 9)] = int(v)

    def write_to_line(self):
        line = "".join(str(self.data[(i, j)]) if (i, j) in self.data else EMPTY_CELL_CHARACTER
                       for i in range(9) for j in range(9))
        return line

    def __setitem__(self, position, value):
        self.data[position] = value

    def __getitem__(self, position):
        return self.data[position]

    def __delitem__(self, position):
        del self.data[position]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        sudoku_str = ""
        for r in range(9):
            if r == 0 or r == 3 or r == 6:
                sudoku_str += self.ROW_SEPARATOR
            for c in range(9):
                if c == 0 or c == 3 or c == 6:
                    sudoku_str += self.COLUMN_SEPARATOR
                if (r, c) in self.data:
                    sudoku_str += "{} ".format(self.data[(r, c)])
                else:
                    sudoku_str += "  "
                if c == 8:
                    sudoku_str += self.COLUMN_SEPARATOR + "\n"
        sudoku_str += self.ROW_SEPARATOR
        return sudoku_str


def main():
    example_line = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"
    sudoku_example = SudokuTable()
    sudoku_example.read_from_line(line=example_line)
    write_line = sudoku_example.write_to_line()
    print example_line
    print write_line

    assert write_line == example_line
    print (0, 1) in sudoku_example
    print sudoku_example.values()
    print sudoku_example.keys()
    print list(sudoku_example.iteritems())
    print sudoku_example


if __name__ == '__main__':
    main()
