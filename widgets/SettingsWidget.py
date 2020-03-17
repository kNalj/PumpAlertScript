from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QApplication, QListWidget, QScrollArea, QTabWidget, QSlider
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import sys


class SettingsWidget(QWidget):
    """
    """
    submitted = pyqtSignal(object)  # a signal that is emitted when data is submitted

    def __init__(self, parent):
        """
        TODO: Documentation
        """
        super(QWidget, self).__init__()

        self.categories = ["User", "Instruments"]
        self.parent = parent
        self.settings = self.parent.settings.copy()

        self.option_tabs = {}
        self.tab_widgets = {}

        self.init_ui()

    def init_ui(self):
        """
        TODO: Documentation
        :return:
        """
        _, _, width, height = QDesktopWidget().screenGeometry().getCoords()
        self.setGeometry(int(0.2 * width), int(0.2 * height), 600, 300)

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("img/settingsIcon.png"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        h_layout = QHBoxLayout()

        self.categories_list = QListWidget()
        for category in self.categories:
            self.categories_list.addItem(category)
        h_layout.addWidget(self.categories_list)

        self.options_area = QWidget()
        options_area_layout = QVBoxLayout()
        self.options_area.setLayout(options_area_layout)
        h_layout.addWidget(self.options_area, stretch=1)

        layout.addLayout(h_layout)

        h_layout_buttons = QHBoxLayout()

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.submit_data)
        h_layout_buttons.addWidget(apply_btn)
        submit_btn = QPushButton("OK")
        submit_btn.clicked.connect(self.submit_and_close)
        h_layout_buttons.addWidget(submit_btn)

        layout.addLayout(h_layout_buttons)

        for category in self.categories:
            self.option_tabs[category] = QTabWidget()
            self.tab_widgets[category] = {}

        self.categories_list.currentItemChanged.connect(self.update_options_area)

        for name, tab in self.build_user_tabs().items():
            scroll = self.build_tab()
            category = "User"
            self.add_tab(category, name, scroll)
            self.fill_tab(category, name, tab)

        for name, tab in self.build_instruments_tabs().items():
            scroll = self.build_tab()
            category = "Instruments"
            self.add_tab(category, name, scroll)
            self.fill_tab(category, name, tab)

        self.show()

    def build_tab(self):
        """
        TODO: Documentation
        :return: QScrollArea that is to be added to the QTabWidget
        """
        # Create scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        # Create widget that fills scroll area
        scroll_area_widget = QWidget(scroll_area)
        scroll_area.setWidget(scroll_area_widget)

        return scroll_area

    def add_tab(self, category, name, widget):
        """
        TODO: Documentation
        :param category: To which category in the side menu to add this tab to. This category has to already exist in
        side menu.
        :param widget:
        :param name:
        :return: NoneType
        """
        self.tab_widgets[category][name] = widget
        self.option_tabs[category].addTab(widget, name)
        return

    def fill_tab(self, category, name, layout):
        """
        TODO: Documentation
        :param category:
        :param name:
        :param layout:
        :return:
        """
        # set the layout as the layout of the tab
        self.tab_widgets[category][name].setLayout(layout)

    def update_options_area(self, category):
        """
        TODO: Documentation
        :param category:
        :return:
        """
        item = self.options_area.layout().itemAt(0)
        if item is not None:
            item.widget().setParent(None)
        self.options_area.layout().addWidget(self.option_tabs[category.text()])

    def build_user_tabs(self):
        """
        TODO: Documentation
        :return:
        """
        login_tab = self.build_login_tab()
        receiver_tab = self.build_receivers_tab()

        return {"Login": login_tab, "Receiver": receiver_tab}

    def build_instruments_tabs(self):
        """
        TODO: Documentation

        :return:
        """
        tabs = {}
        for name, instrument in self.parent.instruments.items():
            tabs[name] = self.build_instrument_tab(instrument)

        return tabs

    def build_login_tab(self):
        """
        TODO: Documentation

        :return:
        """
        layout = QVBoxLayout()

        sender_email_layout = QHBoxLayout()
        sender_email_label = QLabel("Sender email: ")
        sender_email_textbox = QLineEdit(self.parent.settings["sender"])
        sender_email_textbox.textChanged.connect(lambda text: self.update_settings(("sender", text)))
        sender_email_layout.addWidget(sender_email_label)
        sender_email_layout.addWidget(sender_email_textbox)
        layout.addLayout(sender_email_layout)

        username_layout = QHBoxLayout()
        username_label = QLabel("Username: ")
        username_textbox = QLineEdit(self.parent.settings["username"])
        username_textbox.textChanged.connect(lambda text: self.update_settings(("username", text)))
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_textbox)
        layout.addLayout(username_layout)

        pass_layout = QHBoxLayout()
        pass_label = QLabel("Password")
        pass_textbox = QLineEdit(self.parent.settings["password"])
        pass_textbox.textChanged.connect(lambda text: self.update_settings(("password", text)))
        pass_textbox.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(pass_textbox)
        layout.addLayout(pass_layout)

        return layout

    def build_receivers_tab(self):
        """
        TODO: Documentation

        :return:
        """
        layout = QVBoxLayout()

        receiver_email_layout = QHBoxLayout()
        receiver_email_label = QLabel("Send alerts to: ")
        receiver_email_textbox = QLineEdit(self.parent.settings["receiver"])
        receiver_email_textbox.textChanged.connect(lambda text: self.update_settings(("receiver", text)))
        receiver_email_textbox.setPlaceholderText("Example: some.name@ist.ac.at")
        receiver_email_layout.addWidget(receiver_email_label)
        receiver_email_layout.addWidget(receiver_email_textbox)
        layout.addLayout(receiver_email_layout)

        return layout

    def build_instrument_tab(self, instrument):
        """
        TODO: Documentation

        :param instrument:
        :return:
        """
        layout = QVBoxLayout()

        temp_slider_layout = QHBoxLayout()
        temp_slider_label = QLabel("Alert temperature: ")
        temp_slider = QSlider(Qt.Horizontal)
        temp_slider.valueChanged.connect(lambda value: self.update_settings((instrument.name, value)))
        temp_slider.setMinimum(-100)
        limit = instrument.temp_limit
        alert = instrument.alert_temp
        temp_slider.setMaximum(limit)
        temp_slider.setValue(alert)
        temp_val = QLabel(str(alert))
        temp_slider.valueChanged.connect(temp_val.setNum)
        temp_slider_layout.addWidget(temp_slider_label)
        temp_slider_layout.addWidget(temp_slider)
        temp_slider_layout.addWidget(temp_val)

        layout.addLayout(temp_slider_layout)

        return layout

    def submit_data(self):
        """
        TODO: Documentation

        :return:
        """
        self.submitted.emit(self.settings)

    def submit_and_close(self):
        """
        TODO: Documentation

        :return:
        """
        self.submitted.emit(self.settings)
        self.close()

    def update_settings(self, data):
        """
        TODO: Documentation

        :param data:
        :return:
        """
        key, value = data
        self.settings[key] = value


def main():
    from main import CompressorMonitor  # to avoid circular import

    app = QApplication(sys.argv)

    cm = CompressorMonitor()
    cm.add_instrument(None, instruments={"I1": {"name": "Comp1", "ip": "10.21.42.187", "port": "34"},
                                         "I2": {"name": "Comp2", "ip": "10.21.42.155", "port": "34"}})
    sw = SettingsWidget(cm)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()