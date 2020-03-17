from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


def show_error_message(title, message):
    """
    Function for displaying warnings/errors. Opens a QMessageBox and displays title + msg.

    :param title: Title of the displayed warning window
    :type title: str
    :param message: Message shown by the displayed watning window
    :type message: str
    :return: NoneType
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowIcon(QIcon("img/warning_icon.png"))
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
