from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import Qt
from save_and_read_to_yml import save_result_to_file


class LossBox(object):
    def __init__(self, points):
        Dialog = QtWidgets.QDialog()
        self.showDialog(Dialog, points)
        Dialog.exec_()

    def showDialog(self, Dialog, points):
        Dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(596, 204)
        Dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label_text = QtWidgets.QLabel(Dialog)
        self.label_text.setGeometry(QtCore.QRect(130, 30, 350, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_text.setFont(font)
        self.label_text.setObjectName("label_text")
        self.label_write_name = QtWidgets.QLabel(Dialog)
        self.label_write_name.setGeometry(QtCore.QRect(30, 100, 121, 20))
        self.label_write_name.setObjectName("label_write_name")
        self.name_line_edit = QtWidgets.QLineEdit(Dialog)
        self.name_line_edit.setGeometry(QtCore.QRect(160, 100, 391, 26))
        self.name_line_edit.setObjectName("name_line_edit")
        self.name_line_edit.textEdited.connect(self._on_text_edit)
        self.OkButton = QtWidgets.QPushButton(Dialog)
        self.OkButton.setGeometry(QtCore.QRect(260, 150, 93, 29))
        self.OkButton.setObjectName("OkButton")
        self.OkButton.setEnabled(False)
        self.OkButton.clicked.connect(lambda: save_result_to_file(self.name_line_edit.text(), points))
        self.retranslateUi(Dialog, points)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, points):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Game over!"))
        self.label_text.setText(_translate("Dialog", f"You have no moves left! Your result is {points}."))
        self.label_write_name.setText(_translate("Dialog", "Write your name:"))
        self.OkButton.setText(_translate("Dialog", "Ok"))

    def _on_text_edit(self):
        if self._check_if_text_is_empty():
            self.OkButton.setEnabled(False)
        else:
            self.OkButton.setEnabled(True)

    def _check_if_text_is_empty(self):
        if self.name_line_edit.text().strip(' ') == '':
            return True
        else:
            return False
