from PySide2 import QtWidgets

import sys

from main_window import Ui_MainWindow
from read_from_config import name_of_config_file, read_board_size_from_json
from board import Board


def Main():
    try:
        file = open(name_of_config_file, 'r')
        board_size = read_board_size_from_json(file)
        file.close()
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        board = Board(ui, board_size)
        board.show()
        ui.button_swap_buttons.clicked.connect(board.swap_sequences)
        file = open(name_of_config_file, 'r')
        file.close()
        MainWindow.show()
        sys.exit(app.exec_())
    except FileNotFoundError:
        print('No config file in directory!')


if __name__ == "__main__":
    Main()
