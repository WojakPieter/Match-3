class NotQuadraticListError(Exception):
    def __init__(self):
        super().__init__("Nested sublists don't have the same length that original list")


class Sequence:
    '''
        Class responsible for finding a set of at least three same elements in a row or column
        in two-dimensional list.

        Args:
            list_of_elements (list): two-dimensional list (it must be quadratic)

    '''
    def __init__(self, list_of_elements):
        for sublist in list_of_elements:
            if len(sublist) != len(list_of_elements):
                raise NotQuadraticListError
        self.list_of_elements = list_of_elements

    def findSequences(self):
        '''
            Finds coordinates of three or more same elements in row or column in a list  (counted from 0).

            Returns:
                list: list of tuples with coordinates
        '''
        sequence_squares = []
        # vertical
        for x in range(len(self.list_of_elements)):
            for y in range(len(self.list_of_elements) - 2):
                if self.list_of_elements[x][y] == self.list_of_elements[x][y + 1] ==\
                        self.list_of_elements[x][y + 2] and self.list_of_elements[x][y] != '':
                    sequence_squares.append((x, y))
                    sequence_squares.append((x, y + 1))
                    sequence_squares.append((x, y + 2))
        # horizontal
        for x in range(len(self.list_of_elements) - 2):
            for y in range(len(self.list_of_elements)):
                if self.list_of_elements[x][y] == self.list_of_elements[x + 1][y] ==\
                        self.list_of_elements[x + 2][y] and self.list_of_elements[x][y] != '':
                    sequence_squares.append((x, y))
                    sequence_squares.append((x + 1, y))
                    sequence_squares.append((x + 2, y))

        # remove repeating elements
        sequence_squares = set(sequence_squares)
        sequence_squares = list(sequence_squares)
        return sequence_squares

    # vertical
    def _check_up_left_square(self, x, y):
        if x - 1 >= 0 and y - 1 >= 0:
            if self.list_of_elements[x][y] == self.list_of_elements[x - 1][y - 1]:
                return [(x - 1, y - 1), (x, y - 1)]

    def _check_up_right_square(self, x, y):
        if y - 1 >= 0 and x + 1 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x + 1][y - 1]:
                return [(x, y - 1), (x + 1, y - 1)]

    def _check_up_beyond_square(self, x, y):
        if y - 2 >= 0:
            if self.list_of_elements[x][y] == self.list_of_elements[x][y - 2]:
                return [(x, y - 2), (x, y - 1)]

    def _check_bottom_left_square(self, x, y):
        if x - 1 >= 0 and y + 2 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x - 1][y + 2]:
                return [(x - 1, y + 2), (x, y + 2)]

    def _check_bottom_right_square(self, x, y):
        if x + 1 < len(self.list_of_elements) and y + 2 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x + 1][y + 2]:
                return [(x, y + 2), (x + 1, y + 2)]

    def _check_bottom_beyond_square(self, x, y):
        if y + 3 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x][y + 3]:
                return [(x, y + 2), (x, y + 3)]

    def _check_between_left_square(self, x, y):
        if x - 1 >= 0:
            if self.list_of_elements[x - 1][y + 1] == self.list_of_elements[x][y]:
                return [(x - 1, y + 1), (x, y + 1)]

    def _check_between_right_square(self, x, y):
        if x + 1 < len(self.list_of_elements):
            if self.list_of_elements[x + 1][y + 1] == self.list_of_elements[x][y]:
                return [(x, y + 1), (x + 1, y + 1)]

    # horizontal

    def _check_left_upper_square(self, x, y):
        if x - 1 >= 0 and y - 1 >= 0:
            if self.list_of_elements[x][y] == self.list_of_elements[x - 1][y - 1]:
                return [(x - 1, y - 1), (x - 1, y)]

    def _check_left_down_square(self, x, y):
        if x - 1 >= 0 and y + 1 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x - 1][y + 1]:
                return [(x - 1, y), (x - 1, y + 1)]

    def _check_left_beyond_square(self, x, y):
        if x - 2 >= 0:
            if self.list_of_elements[x][y] == self.list_of_elements[x - 2][y]:
                return [(x - 2, y), (x - 1, y)]

    def _check_right_upper_square(self, x, y):
        if y - 1 >= 0 and x + 2 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x + 2][y - 1]:
                return [(x + 2, y - 1), (x + 2, y)]

    def _check_right_down_square(self, x, y):
        if y + 1 < len(self.list_of_elements) and x + 2 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x + 2][y + 1]:
                return [(x + 2, y), (x + 2, y + 1)]

    def _check_right_beyond_square(self, x, y):
        if x + 3 < len(self.list_of_elements):
            if self.list_of_elements[x][y] == self.list_of_elements[x + 3][y]:
                return [(x + 2, y), (x + 3, y)]

    def _check_between_upper_square(self, x, y):
        if y - 1 >= 0:
            if self.list_of_elements[x + 1][y - 1] == self.list_of_elements[x][y]:
                return [(x + 1, y - 1), (x + 1, y)]

    def _check_between_down_square(self, x, y):
        if y + 1 < len(self.list_of_elements):
            if self.list_of_elements[x + 1][y + 1] == self.list_of_elements[x][y]:
                return [(x + 1, y), (x + 1, y + 1)]

    def findPossibleSequences(self):
        '''
            Finds coordinates of every two elements in a table, which swapped will create
            a sequence of at least three repeating elements in a line.

            Returns:
                list: list of sublists, each with two tuples
        '''
        possible_sequences = []
        list = self.list_of_elements
        for x in range(len(list)):
            for y in range(len(list)):
                # vertical sequences
                if y + 1 < len(list) and list[x][y] == list[x][y + 1]:
                    possible_sequences.append(self._check_up_beyond_square(x, y))
                    possible_sequences.append(self._check_up_left_square(x, y))
                    possible_sequences.append(self._check_up_right_square(x, y))
                    possible_sequences.append(self._check_bottom_beyond_square(x, y))
                    possible_sequences.append(self._check_bottom_left_square(x, y))
                    possible_sequences.append(self._check_bottom_right_square(x, y))
                if y + 2 < len(list) and list[x][y] == list[x][y + 2]:
                    possible_sequences.append(self._check_between_left_square(x, y))
                    possible_sequences.append(self._check_between_right_square(x, y))

                # horizontal sequences
                if x + 1 < len(list) and list[x][y] == list[x + 1][y]:
                    possible_sequences.append(self._check_left_beyond_square(x, y))
                    possible_sequences.append(self._check_left_upper_square(x, y))
                    possible_sequences.append(self._check_left_down_square(x, y))
                    possible_sequences.append(self._check_right_beyond_square(x, y))
                    possible_sequences.append(self._check_right_upper_square(x, y))
                    possible_sequences.append(self._check_right_down_square(x, y))
                if x + 2 < len(list) and list[x][y] == list[x + 2][y]:
                    possible_sequences.append(self._check_between_upper_square(x, y))
                    possible_sequences.append(self._check_between_down_square(x, y))
        while None in possible_sequences:
            possible_sequences.remove(None)
        return possible_sequences
