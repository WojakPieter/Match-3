from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMessageBox, QInputDialog, QFormLayout, QLineEdit
from PySide2.QtGui import QCursor, Qt
import random

from main_window import Ui_MainWindow
from sequences import Sequence
from read_from_config import name_of_config_file, read_board_size_from_json
from read_from_config import read_mark_color_from_json
from read_from_config import read_colors_from_json
from final_box import LossBox


clicked_buttons = []
levels = {
    1: 300,
    2: 900,
    3: 2300,
    4: 5000,
    5: 10000,
    6: 25000
}

number_of_colors_for_levels = {
    1: 6,
    2: 8,
    3: 9,
    4: 9,
    5: 12,
    6: 13
}

file = open('config.json', 'r')
mark_color = read_mark_color_from_json(file)


class CustomAnimationGroup(QtCore.QParallelAnimationGroup):
    '''
        Class inheriting from QParallelAnimationGroup. The class stands for starting a few animations
        (QPropertyAnimation objects) in the same time. Unlike the original class QParallelAnimationGroup,
        it can be instatiated.

        Args:
            widget (QObject): the parent window 
    '''
    def __init__(self, widget):
        super().__init__(widget)


class CustomSequentialAnimationGroup(QtCore.QSequentialAnimationGroup):
    '''
        Class inheriting from QSequentialAnimationGroup. The class stands for starting a few animations
        (QPropertyAnimation objects) one by one. Unlike the original class QSequentialAnimationGroup,
        it can be instatiated.

        Args:
            widget (QObject): the parent window
    '''
    def __init__(self, widget):
        super().__init__(widget)


class Square(QtWidgets.QPushButton):
    '''
        Class representing a square displayng on a board.

        Args:
            widget (QObject): the parent window
            x_index (int): x-coordinate of the square on a board. Default: 0
            y_index (int): y-coordinate of the square on a board. Default: 0
            bg_color (str): name of color of the button, compliant with CSS color
            names standard
    '''
    def __init__(self, widget, x_index=0, y_index=0, bg_color='none'):
        super().__init__(widget)
        self.widget = widget
        self.x_index = x_index
        self.y_index = y_index
        self.updateCoordinates()
        self.setGeometry(QtCore.QRect(self.x_coordinate, self.y_coordinate, 50, 50))
        self.button_style = f'border: none; background-color: {bg_color}'
        self.clicked.connect(self.onClick)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(self.button_style)

    def onClick(self):
        '''
            Function called when a square is clicked. It marks a square with a given color
            (unless there are two already clicked squares)
            or ummark when it has been clicked already.
        '''
        if f'border: 5px solid {mark_color}' in self.button_style:
            self.button_style = self.button_style.replace(f'5px solid {mark_color}',
                                                          'none')
        else:
            if len(clicked_buttons) != 2:
                self.button_style = self.button_style.replace('none',
                                                              f'5px solid {mark_color}')
        self.setStyleSheet(self.button_style)
        coordinates = (self.x_index, self.y_index)
        self.widget.button_onclick_caller(coordinates)

    def swap_x_index(self, other):
        '''
            Function which swaps Square object parameter x_index between two objects.

            Args:
                other (Square): an objects which to swap x_index with 
        '''
        bufor = self.x_index
        self.x_index = other.x_index
        other.x_index = bufor

    def swap_y_index(self, other):
        '''
            Function which swaps Square object parameter y_index between two objects.

            Args:
                other (Square): an objects which to swap y_index with 
        '''
        bufor = self.y_index
        self.y_index = other.y_index
        other.y_index = bufor

    def updateCoordinates(self):
        '''
            Counts square's x-coordinate and y-coordinate on the widget.
        '''
        self.x_coordinate = self.x_index * 60
        self.y_coordinate = self.y_index * 60


class Board(QtWidgets.QWidget):
    '''
        Class representing a square board with squares on a window.

        Args:
            window_parent (QObject): widget which is a parent of the board
            side_length (int): number of squares in one row 
    '''
    def __init__(self, window_parent, side_length):
        super().__init__(window_parent.centralwidget)
        self.window_parent = window_parent
        colors = read_colors_from_json(open(name_of_config_file, 'r'))
        self.potential_colors = random.sample(colors, number_of_colors_for_levels[1])
        self.side_length = side_length
        self.buttons = []
        self.points = 0
        self.level = 1
        self.button_colors = self.generate_colors()
        for i in range(side_length):
            self.buttons.append([])
        for x in range(side_length):
            for y in range(side_length):
                button = Square(self, x, y, self.button_colors[x][y])   
                self.buttons[x].append(button)
        self.setGeometry(QtCore.QRect(30, 30, side_length * 60,
                                      side_length * 60))
        button = ''
        self.show()

    def button_onclick_caller(self, coordinates):
        '''
            Called when a square on a board is clicked. The function enables button "Swap"
            on a screen when there are two clicked squares, which swapped will make a sequence of
            at least three squares with same color in a line, or disables it when the button is unclicked.

            Args:
                coordinates (tuple): a tuple with two integers, which stand for
                                     square's x-index and y-index on a board
        '''
        if coordinates in clicked_buttons:
            clicked_buttons.remove(coordinates)
            self.window_parent.button_swap_buttons.setEnabled(False)
        else:
            if len(clicked_buttons) != 2:
                clicked_buttons.append(coordinates)
            seq = Sequence(self.button_colors).findPossibleSequences()
            if clicked_buttons in seq or clicked_buttons[::(-1)] in seq:
                self.window_parent.button_swap_buttons.setEnabled(True)

    def grow_sequences(self, list_of_squares):
        '''
            Creates an animation group which stands for growing up by 10%
            squares which are to be crossed out. When the squares are grown, points
            are added to a player.

            Args:
                list_of_squares (list): list of tuples with x-index and y-index of squares
                                        which are to be grown up
            
            Returns:
                CustomAnimationGroup: an animation group for growing up squares
        '''
        self.anim_grow = CustomAnimationGroup(Square(self))
        for i in range(len(list_of_squares)):
            actual_button = self.buttons[list_of_squares[i][0]][list_of_squares[i][1]]
            anim = QtCore.QPropertyAnimation(actual_button, b'geometry')
            anim.setStartValue(QtCore.QRect(actual_button.x_coordinate,
                                            actual_button.y_coordinate,
                                            50, 50))
            anim.setEndValue(QtCore.QRect(actual_button.x_coordinate - 2,
                                          actual_button.y_coordinate - 2, 55, 55))
            anim.setDuration(400)
            self.anim_grow.addAnimation(anim)
        self.anim_grow.finished.connect(lambda: self.addPoints(len(list_of_squares)))
        return self.anim_grow

    def nullify_sequences(self, list_of_squares):
        '''
            Creates an animation group which stands for disappearing
            squares which are to be crossed out. It also removes a square object from list self.buttons.

            Args:
                list_of_squares (list): list of tuples with x-index and y-index of squares
                                        which are to be nullified

            Returns:
                CustomAnimationGroup: an animation group for nulllifying squares
        '''
        self.anim_nullify = CustomAnimationGroup(Square(self))
        for i in range(len(list_of_squares)):
            actual_button = self.buttons[list_of_squares[i][0]][list_of_squares[i][1]]
            anim = QtCore.QPropertyAnimation(actual_button, b'geometry')
            anim.setStartValue(QtCore.QRect(actual_button.x_coordinate - 2,
                                            actual_button.y_coordinate - 2,
                                            55, 55))
            anim.setEndValue(QtCore.QRect(actual_button.x_coordinate + 25,
                                          actual_button.y_coordinate + 25, 0, 0))
            anim.setDuration(400)
            self.anim_nullify.addAnimation(anim)
            self.buttons[list_of_squares[i][0]][list_of_squares[i][1]] = ''
            self.button_colors[list_of_squares[i][0]][list_of_squares[i][1]] = ''
        return self.anim_nullify

    def unlock_buttons(self):
        '''
            Changes all squares' property "Enabled" to True.
        '''
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)

    def reloadBoard(self):
        '''
            Called when player ranks up. The function nullifies all squares on a board,
            creates new squares with another colors, sets them over the screen and brigns
            the entire new board donw on the widget.
        '''
        self.potential_colors = random.sample(read_colors_from_json(open(name_of_config_file, 'r')),
                                              number_of_colors_for_levels[self.level])
        integrated_buttons_array = []
        for x in range(self.side_length):
            for y in range(self.side_length):
                integrated_buttons_array.append((x, y))
        sequencial1 = CustomSequentialAnimationGroup(Square(self))
        sequencial1.addAnimation(self.grow_sequences(integrated_buttons_array))
        sequencial1.addAnimation(self.nullify_sequences(integrated_buttons_array))
        sequencial1.addPause(250)
        self.button_colors = self.generate_colors()
        fall_new_board = CustomAnimationGroup(Square(self))
        for x in range(self.side_length):
            for y in range(self.side_length):
                button = Square(self, x, y - self.side_length, self.button_colors[x][y])   
                self.buttons[x][y] = button
                button.show()
                button.y_index += self.side_length
                button.updateCoordinates()
                anim = self._animate_button_to_fall(button, self.side_length)
                fall_new_board.addAnimation(anim)
                fall_new_board.finished.connect(self.unlock_buttons)
        sequencial1.addAnimation(fall_new_board)
        sequencial1.start()

    def swap_buttons(self, first_button, second_button):
        '''
            Sets property Enabled = False to all squares on a board (until the animations end),
            creates animation objects (QPropertyAnimation) which stand for swapping
            two marked squares. It also updates squares' attributes x-index and y-index.

            Args:
                first_button (Square): first of two squares to be swapped
                second_button (Square): second of two squares to be swapped
            
            Returns:
                CustomAnimationGroup: animation group with two animation objects
        '''
        # disabling all buttons
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)
        # creating animations instances
        self.anim1 = QtCore.QPropertyAnimation(first_button, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QtCore.QRect(first_button.x_coordinate,
                                              first_button.y_coordinate, 50, 50))
        self.anim1.setEndValue(QtCore.QRect(second_button.x_coordinate,
                                            second_button.y_coordinate, 50, 50))

        self.anim2 = QtCore.QPropertyAnimation(second_button, b"geometry")
        self.anim2.setDuration(300)
        self.anim2.setStartValue(QtCore.QRect(second_button.x_coordinate,
                                              second_button.y_coordinate, 50, 50))
        self.anim2.setEndValue(QtCore.QRect(first_button.x_coordinate,
                                            first_button.y_coordinate, 50, 50))
        swap_group = CustomAnimationGroup(Square(self))
        swap_group.addAnimation(self.anim1)
        swap_group.addAnimation(self.anim2)

        # updating buttons' parameters and global table self.buttons 
        first_button.swap_x_index(second_button)
        first_button.swap_y_index(second_button)

        first_button.updateCoordinates()
        second_button.updateCoordinates()

        self.buttons[first_button.x_index][first_button.y_index] = first_button
        self.buttons[second_button.x_index][second_button.y_index] = second_button
        return swap_group

    def loss(self):
        '''
            Creates the final dialog box, when the game is lost.
        '''
        file.close()
        msg_box = LossBox(self.points)

    def _check_the_promotion(self):
        '''
            Called after sequence of animations ends. It checks whether player ranks up,
            and afterwards - whether he losses. If not - unlocks all button and lets
            player play.
        '''
        if levels[self.level] <= self.points:
            self.level = self.level + 1
            msg_box = QMessageBox()
            msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Congratulations!")
            msg_box.setText(f'You received level {self.level}! Press Ok to continue.')
            msg_box.exec_()
            self.window_parent.label_level_value.setText(str(self.level))
            self.reloadBoard()
        seq = Sequence(self.button_colors)
        if seq.findPossibleSequences() == []:
            self.loss()

        self.unlock_buttons()

    def _animate_button_to_fall(self, button, how_many_to_fall):
        '''
            Creates an animation object (QPropertyAnimation) to bring a square down by
            certain number of positions.

            Args:
                button (Square): the square to be animated
                how_many_to_fall (int): number of positions to lower the square down

            Returns:
                QPropertyAnimation: an animation objects
        '''
        anim4 = QtCore.QPropertyAnimation(button, b'geometry')
        anim4.setStartValue(QtCore.QRect(button.x_coordinate,
                                         button.y_coordinate -
                                         60 * how_many_to_fall,
                                         50, 50))
        anim4.setEndValue(QtCore.QRect(button.x_coordinate,
                                       button.y_coordinate,
                                       50, 50))
        anim4.setDuration(150 * how_many_to_fall)
        return anim4

    def _move_down_buttons_from_above(self, x):
        '''
            Finds the empty positions on the board and creates animation objects
            (QPropertyAnimation) to all squares above, so that they fall down.

            Args:
                x: number of column of the board where to bring down squares

            Returns:
                list: array of appropriate animation objects
        '''
        fall_animations = []
        for i in range(len(self.button_colors[x]) - 1, -1, -1):
            empty_squares_number = self.button_colors[x][i:].count('')
            if self.button_colors[x][i] != '':
                bufor = self.button_colors[x][i]
                self.button_colors[x][i] = ''
                self.button_colors[x][i + empty_squares_number] = bufor

                self.buttons[x][i].y_index += empty_squares_number
                self.buttons[x][i].updateCoordinates()
                bufor = self.buttons[x][i]
                self.buttons[x][i] = ''
                self.buttons[x][i + empty_squares_number] = bufor
                animated_button = bufor
                anim = self._animate_button_to_fall(animated_button, empty_squares_number)
                if empty_squares_number != 0:
                    fall_animations.append(anim)

        return fall_animations

    def _create_new_button_to_fall(self, x, y, bg_color, how_many_to_fall):
        '''
            Creates new squares to firstly display above screen and then fall down.

            Args:
                x (int): x-index of a new square
                y (int): y-index of a new square (should be a negative number, it will be
                increased appropriately during the programme)
                bg_color (str): color of new square (compliant with CSS color
            names standard)

            Returns:
                Square: new created square
        '''
        button = Square(self, x, y, bg_color)
        button.show()
        button.y_index += how_many_to_fall
        button.updateCoordinates()
        return button

    def fall_squares(self):
        '''
            Called when squares are crossed out. Creates animation group which stands for
            falling down all squares over the empty fields on the board. Also creates new squares
            to be fallen on the top.

            Returns:
                CustomAnimationGroup: described animation group
        '''
        fall_animation_group = CustomAnimationGroup(Square(self))
        for x in range(len(self.buttons)):
            empty_squares_number = self.button_colors[x].count('')

            if empty_squares_number == 0:
                continue

            fall_animation_objects = self._move_down_buttons_from_above(x)

            for object in fall_animation_objects:
                fall_animation_group.addAnimation(object)

            for i in range(-1 * empty_squares_number, 0, +1):
                new_color = random.choice((self.potential_colors))
                self.button_colors[x][i + empty_squares_number] = new_color
                button = self._create_new_button_to_fall(x, i, new_color, empty_squares_number)
                self.buttons[x][i + empty_squares_number] = button
                anim = self._animate_button_to_fall(button, empty_squares_number)
                fall_animation_group.addAnimation(anim)

        return fall_animation_group

    def swap_sequences(self):
        '''
            Creates and starts animation group for: swapping marked squares, grow up
            the sequences, nullify them and bring down squares from above.
        '''
        self.window_parent.button_swap_buttons.setEnabled(False)

        first_button = self.buttons[clicked_buttons[0][0]][clicked_buttons[0][1]]
        second_button = self.buttons[clicked_buttons[1][0]][clicked_buttons[1][1]]

        for button in (first_button, second_button):
            button.button_style = button.button_style.replace(f'5px solid {mark_color}',
                                                              'none')
            button.setStyleSheet(button.button_style)
        clicked_buttons.clear()
        bufor = self.button_colors[first_button.x_index][first_button.y_index]
        self.button_colors[first_button.x_index][first_button.y_index] =\
            self.button_colors[second_button.x_index][second_button.y_index]
        self.button_colors[second_button.x_index][second_button.y_index] = bufor
        sequence = Sequence(self.button_colors)
        sequencial = CustomSequentialAnimationGroup(Square(self))
        sequencial.addAnimation(self.swap_buttons(first_button, second_button))
        while sequence.findSequences() != []:
            sequencial.addAnimation(self.grow_sequences(sequence.findSequences()))
            sequencial.addAnimation(self.nullify_sequences(sequence.findSequences()))
            sequencial.addAnimation(self.fall_squares())
        sequencial.addPause(250)
        sequencial.finished.connect(self._check_the_promotion)
        sequencial.start()

    def addPoints(self, crossed_squares_number):
        '''
            Increases number of player points.

            Args:
                crossed_squares_number (int): number of crossed squares
        '''
        if crossed_squares_number < len(self.buttons)**2:
            self.points += 10 * crossed_squares_number * self.level
            self.window_parent.label_points_value.setText(str(self.points))

    def generate_colors(self):
        '''
            Creates and returns a two-dimensional list with randomized
            colors of squares on the board.
        '''
        button_colors = []
        for i in range(self.side_length):
            button_colors.append([])
        for x in range(self.side_length):
            for y in range(self.side_length):
                button_colors[x].append(random.choice(self.potential_colors))
        sequence = Sequence(button_colors)
        while sequence.findSequences() != [] or sequence.findPossibleSequences() == []:
            return self.generate_colors()
        return button_colors


def swap_values_in_table(table, x_index1, y_index1, x_index2, y_index2):
    '''
        Swaps two elements in a two-dimensional list.

        Args:
            table (list): a list

            x_index1 (int): index of sublist with element 1
            y_index1 (int): index of element 1 in a sublist

            x_index2 (int): index of sublist with element 2
            y_index2 (int): index of element 2 in a sublist
    '''
    bufor = table[x_index1][y_index1]
    table[x_index1][y_index1] = table[x_index2][y_index2]
    table[x_index2][y_index2] = bufor