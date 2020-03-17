from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QApplication
from PyQt5.QtCore import pyqtSignal
import sys


class AddInstrumentWidget(QWidget):
    """
    TODO: Write documentation
    """

    submitted = pyqtSignal(object)

    def __init__(self):
        """
        TODO: Write documentation

        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        TODO: Write documentation

        :return:
        """
        _, _, width, height = QDesktopWidget().screenGeometry().getCoords()
        self.setGeometry(int(0.2 * width), int(0.2 * height), 400, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        h_layout_name = QHBoxLayout()
        self.instr_name_label = QLabel("Instrument name: ")
        self.instr_name_textbox = QLineEdit()
        h_layout_name.addWidget(self.instr_name_label)
        h_layout_name.addWidget(self.instr_name_textbox)
        layout.addLayout(h_layout_name)

        h_layout_ip = QHBoxLayout()
        self.ip_label = QLabel("Instrument IP: ")
        self.ip_textbox = QLineEdit()
        self.port_label = QLabel("Port: ")
        self.port_textbox = QLineEdit()
        h_layout_ip.addWidget(self.ip_label)
        h_layout_ip.addWidget(self.ip_textbox)
        h_layout_ip.addWidget(self.port_label)
        h_layout_ip.addWidget(self.port_textbox)
        layout.addLayout(h_layout_ip)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.ok_btn)

        self.show()

    def submit_data(self):
        """
        TODO: Write documentation

        :return:
        """
        data = {"ip": self.ip_textbox.text(), "port": self.port_textbox.text(), "name": self.instr_name_textbox.text()}
        self.submitted.emit(data)
        self.close()


def main():
    app = QApplication(sys.argv)
    AIW = AddInstrumentWidget()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()