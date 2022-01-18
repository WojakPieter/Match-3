from PySide2 import QtCore, QtGui, QtWidgets
from read_from_config import read_board_size_from_json
from read_from_config import name_of_config_file
from save_and_read_to_yml import find_max_result

window_sizes_regarding_quantity_of_squares = {
    5: (600, 400),
    6: (700, 450),
    7: (800, 533),
    8: (900, 600),
    9: (1200, 800),
    10: (1200, 800),
    11: (1300, 850),
    12: (1400, 900)
}


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        file = open(name_of_config_file, 'r')
        number_of_squares = read_board_size_from_json(file)
        size = window_sizes_regarding_quantity_of_squares[number_of_squares]
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(size[0], size[1])
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.right_bar = QtWidgets.QWidget(self.centralwidget)
        self.right_bar.setGeometry(QtCore.QRect(size[0] - 250, 0, 250, size[1]))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_bar.sizePolicy().hasHeightForWidth())
        self.right_bar.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        self.right_bar.setPalette(palette)
        self.right_bar.setAutoFillBackground(False)
        self.right_bar.setStyleSheet("background-color: rgba(0, 255, 255, 0.5);")
        self.right_bar.setObjectName("right_bar")
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.splitter = QtWidgets.QSplitter(self.right_bar)
        self.splitter.setGeometry(QtCore.QRect(10, 160, 131, 32))
        self.splitter.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_points = QtWidgets.QLabel(self.right_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_points.sizePolicy().hasHeightForWidth())
        self.label_points.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        self.button_swap_buttons = QtWidgets.QPushButton(self.right_bar)
        self.button_swap_buttons.setGeometry(QtCore.QRect(10, 0.4 * size[1], 191, 29))
        self.button_swap_buttons.setEnabled(False)
        self.button_swap_buttons.setText("Swap")
        self.button_swap_buttons.setFont(font)
        self.button_swap_buttons.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_swap_buttons.setStyleSheet("QPushButton\n"
                                               "{\n"
                                               "border: 1px solid black;\n"
                                               "background-color: rgba(200, 200, 200, 0.8);\n"
                                               "border-radius: 7px;\n"
                                               "}\n"
                                               "QPushButton::hover {\n"
                                               "background-color: rgba(240, 240, 240, 0.9)\n"
                                               "}")
        self.button_swap_buttons.setObjectName("button_swap_buttons")
        self.label_points.setFont(font)
        self.label_points.setStyleSheet("background-color: none")
        self.label_points.setObjectName("label_points")
        self.label_points.setGeometry(QtCore.QRect(10, 0.2 * size[1], 100, 32))
        self.label_points_value = QtWidgets.QLabel(self.right_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_points_value.sizePolicy().hasHeightForWidth())
        self.label_points_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_points_value.setFont(font)
        self.label_points_value.setAutoFillBackground(False)
        self.label_points_value.setStyleSheet("background-color: none")
        self.label_points_value.setObjectName("label_points_value")
        self.label_points_value.setGeometry(QtCore.QRect(100, 0.2 * size[1], 120, 32))
        self.label_level = QtWidgets.QLabel(self.right_bar)
        self.label_level.setGeometry(QtCore.QRect(11, 0.1 * size[1], 100, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        self.label_level.setFont(font)
        self.label_level.setAutoFillBackground(False)
        self.label_level.setStyleSheet("background-color: none")
        self.label_level.setObjectName("label_level")
        self.label_level_value = QtWidgets.QLabel(self.right_bar)
        self.label_level_value.setGeometry(QtCore.QRect(100, 0.1 * size[1], 80, 32))
        self.label_level_value.setStyleSheet("background-color: none")
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(16)
        self.label_level_value.setFont(font)
        self.label_level_value.setAutoFillBackground(False)
        self.label_level_value.setObjectName("label_level_value")
        self.label_best_result = QtWidgets.QLabel(self.right_bar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        self.label_best_result.setFont(font)
        self.label_best_result.setToolTip("")
        self.label_best_result.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.label_best_result.setObjectName("label_best_result")
        self.label_best_result.setGeometry(QtCore.QRect(10, 0.7 * size[1], 120, 32))
        self.label_best_result_value = QtWidgets.QLabel(self.right_bar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_best_result_value.setFont(font)
        self.label_best_result_value.setAutoFillBackground(False)
        self.label_best_result_value.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.label_best_result_value.setObjectName("label_best_result_value")
        self.label_best_result_value.setGeometry(QtCore.QRect(130, 0.7 * size[1], 90, 32))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Match-3"))

        self.label_points.setText(_translate("MainWindow", "Points:"))
        self.label_points_value.setText(_translate("MainWindow", "0"))
        self.label_level.setText(_translate("MainWindow", "Level:"))
        self.label_level_value.setText(_translate("MainWindow", "1"))
        self.label_best_result.setText(_translate("MainWindow", "Best result:"))
        self.label_best_result_value.setText(_translate("MainWindow", find_max_result()))
