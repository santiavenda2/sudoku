

class Sudoku(dict):

    COLUMN_SEPARATOR = "| "

    ROW_SEPARATOR = "+-------+-------+-------+\n"

    def read_from_line(self, line):
        assert len(line) == 81
        for i, v in enumerate(line):
            if v != '.':
                self[(i / 9, i % 9)] = int(v)

    def __setitem__(self, position, value):
        self.__dict__[position] = value

    def __getitem__(self, position):
        return self.__dict__[position]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, position):
        del self.__dict__[position]

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, position):
        return position in self.__dict__

    def add(self, position, value):
        self.__dict__[position] = value

    def __iter__(self):
        return self.__dict__.__iter__()

    def __call__(self):
        return self.__dict__

    def __str__(self):
        sudoku_str = ""
        for r in range(9):
            if r == 0 or r == 3 or r == 6:
                sudoku_str += self.ROW_SEPARATOR
            for c in range(9):
                if c == 0 or c == 3 or c == 6:
                    sudoku_str += self.COLUMN_SEPARATOR
                if (r, c) in self.__dict__:
                    sudoku_str += "{} ".format(self.__dict__[(r, c)])
                else:
                    sudoku_str += "  "
                if c == 8:
                    sudoku_str += self.COLUMN_SEPARATOR + "\n"
        sudoku_str += self.ROW_SEPARATOR
        return sudoku_str


def main():
    example_line = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"
    sudoku_example = Sudoku()
    sudoku_example.read_from_line(line=example_line)
    print (0, 1) in sudoku_example
    print sudoku_example.values()
    print sudoku_example.keys()
    print list(sudoku_example.iteritems())


if __name__ == '__main__':
    main()
