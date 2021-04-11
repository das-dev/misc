""" This decomposition created on the basis of information hiding. """

import sys
from io import StringIO
from typing import TextIO, List, Iterator, Callable


class Line:

    def __init__(self, line: str) -> None:
        self._words = line.split(' ')

    def __iter__(self) -> Iterator[str]:
        return iter(self._words)

    def __getitem__(self, item: int) -> str:
        return self._words[item]

    def __len__(self) -> int:
        return len(self._words)

    @property
    def first_char(self) -> str:
        if self._words and self._words[0]:
            return self._words[0][0]
        return ''


class LineStorage:

    def __init__(self) -> None:
        self._lines: List[Line] = []

    def add_lines(self, lines: List[str]) -> None:
        for line in lines:
            self.add_line(line)

    def add_line(self, line: str) -> None:
        if line.strip():
            self._lines.append(Line(line))

    def sort(self, order: Callable[[Line], str]) -> None:
        self._lines = list(sorted(self._lines, key=order))

    def __iter__(self) -> Iterator[Line]:
        return iter(self._lines)


class Input:
    """ This module reads the original lines from the input media
    and calls the line storage module to have them stored internally. """

    def __init__(self, storage: LineStorage) -> None:
        self._storage = storage

    def read_lines(self, source: TextIO) -> None:
        lines = source.read().strip().splitlines()
        self._storage.add_lines(lines)


class CircularShifter:

    def __init__(self, lines: LineStorage) -> None:
        self.shifted = LineStorage()
        self._lines = lines

    def setup(self) -> None:
        for line in self._lines:
            for word_no, word in enumerate(line):
                shifted = []
                for i in range(word_no, word_no + len(line)):
                    shifted.append(line[i % len(line)])
                self.shifted.add_line(' '.join(shifted))


class Alphabetizer:

    def order(self, line: Line) -> str:
        return line.first_char.lower()

    def sort(self, shifter: CircularShifter) -> None:
        shifter.shifted.sort(self.order)


class Output:
    """ This module will give the desired printing of set of lines
    or circular shifts. """

    def __init__(self, destination: TextIO = sys.stdout) -> None:
        self.destination = destination

    def write(self, shifter: CircularShifter) -> None:
        for line in shifter.shifted:
            words = [''.join(word) for word in line]
            words[0] = words[0].upper()
            print(' '.join(words), file=self.destination)


class MasterControl:

    @staticmethod
    def execute(source: TextIO) -> None:
        storage = LineStorage()
        Input(storage).read_lines(source)
        shifter = CircularShifter(storage)
        shifter.setup()
        Alphabetizer().sort(shifter)
        Output().write(shifter)


if __name__ == '__main__':
    src = StringIO('hello world\ni am Yoda\n')
    MasterControl.execute(src)
