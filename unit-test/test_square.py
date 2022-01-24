from board import Square, Board
from PySide2 import QtWidgets
from main_window import Ui_MainWindow
from PySide2.QtWidgets import QApplication


def test_square_class():
    try:
        app = QtWidgets.QApplication()
    except RuntimeError:
        pass
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    board = Board(ui, 6)
    sqr = Square(board, 4, 5, 'cyan')
    assert sqr.x_index == 4
    assert sqr.y_index == 5
    assert sqr.button_style == 'border: none; background-color: cyan'
    assert sqr.x_coordinate == 240
    assert sqr.y_coordinate == 300



def test_square_swap_coordinates():
    try:
        app = QtWidgets.QApplication()
    except RuntimeError:
        pass
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    board = Board(ui, 6)
    sqr1 = Square(board, 4, 5, 'cyan')
    sqr2 = Square(board, 4, 6, 'red')
    sqr1.swap_x_index(sqr2)
    sqr1.swap_y_index(sqr2)
    assert sqr1.x_index == 4
    assert sqr2.x_index == 4
    assert sqr1.y_index == 6
    assert sqr2.y_index == 5


def test_square_count_coordinates():
    try:
        app = QtWidgets.QApplication()
    except RuntimeError:
        pass
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    board = Board(ui, 6)
    sqr = Square(board)
    sqr.x_index = 5
    sqr.y_index = 7
    assert sqr.x_coordinate == 0
    assert sqr.y_coordinate == 0
    sqr.updateCoordinates()
    assert sqr.x_coordinate == 300
    assert sqr.y_coordinate == 420
