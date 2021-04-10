""" Implementation of modularization by shared data.
Based on "On the criteria to be used in decomposing systems into modules" by D. Parnas. """
import sys
from io import StringIO
from typing import TextIO, List, Tuple


class Input:
    """ Reads the data lines from the input medium and stores them.
    An index is kept to show the starting address of each line. """

    def __init__(self) -> None:
        self.chars: List[str] = []
        self.index: List[int] = []

    def read_lines(self, medium: TextIO) -> None:
        self.index = [0]
        for address, char in enumerate(medium.read().strip()):
            if char == '\n':
                self.index.append(address + 1)
            self.chars.append(char)


class CircularShift:
    """ This module is called after the input module has completed its work.
    It prepares an index which gives the address of the first character
    of each circular shift, and the original index of the line
    in the array made up by module 1. It leaves its output in core
    with words in pairs (original line number, starting address). """

    def __init__(self):
        self.shifts: List[Tuple[int, int]] = []

    def make_shifts(self, chars: List[str], index: List[int]) -> None:
        for lineno, line_start in enumerate(index):
            for shift, char in enumerate(chars[line_start:]):
                address = shift + line_start
                if address == line_start:
                    self.shifts.append((lineno, address))
                elif address + 1 in index:
                    break
                elif char in (' ', '\n'):
                    self.shifts.append((lineno, address + 1))


class Alphabetizing:
    """ This module takes as input the arrays produced by modules I and 2.
    It produces an array in the same format as that produced by module 2.
    In this case, however, the circular shifts are listed
    in another order (alphabetically). """

    def __init__(self, chars: List[str], index: List[int]) -> None:
        self.chars = chars
        self.index = index

    def order(self, shift: Tuple[int, int]) -> str:
        _, shift_address = shift
        if shift_address < len(self.chars):
            return self.chars[shift_address].lower()

    def sort(self, shifts: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return list(sorted(shifts, key=self.order))


class Output:
    """ Using the arrays produced by module 3 and module 1,
    this module produces a nicely formatted output listing
    all of the circular shifts. In a sophisticated system
    the actual start of each line will be marked,
    pointers to further information may be inserted,
    and the start of the circular shift may actually
    not be the first word in the line, etc. """

    def __init__(self, chars: List[str], index: List[int], destination: TextIO = sys.stdout):
        self.destination = destination
        self.chars = chars
        self.index = index

    def write(self, shifts: List[Tuple[int, int]]) -> None:
        for lineno, shift_address in shifts:
            start_address = self.index[lineno]
            first_part = self.chars[start_address:shift_address]
            shifted = self.chars[shift_address:] + [' '] + first_part
            for address, char in enumerate(self.chars):
                if address > shift_address and char == '\n':
                    shifted = self.chars[shift_address:address] + [' '] + first_part
            print(''.join(shifted).strip(), file=self.destination)


class MasterControl:
    """ This module does little more than control the sequencing
     among the other four modules. It may also handle error messages,
     space allocation, etc. """

    @staticmethod
    def to_kwic(source: TextIO) -> None:
        reader = Input()
        reader.read_lines(source)
        shifter = CircularShift()
        shifter.make_shifts(reader.chars, reader.index)
        sorter = Alphabetizing(reader.chars, reader.index)
        out = Output(reader.chars, reader.index)
        out.write(sorter.sort(shifter.shifts))


if __name__ == '__main__':
    MasterControl.to_kwic(StringIO('hello world\ni am Yoda\n'))
