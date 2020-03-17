# This file should implement the GUI to setup monitoring of the instruments

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QMenu, QTableWidget, QTableWidgetItem, \
    QAction, QVBoxLayout, QHeaderView
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt, QThreadPool
from widgets.AddInstrumentWidget import AddInstrumentWidget
from widgets.SettingsWidget import SettingsWidget
from Pump import Pump
from alert import Alert
from time import sleep, asctime
from ThreadWorker import Worker
from widgets.ErrorMsg import show_error_message


def trap_exc_during_debug(exctype, value, traceback, *args):
    # when app raises uncaught exception, print info
    print(args)
    print(exctype, value, traceback)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class CompressorMonitor(QMainWindow):
    """

    """
    def __init__(self):
        """
        Constructor for the main program window. Initiates default values to member variables.

        """
        super().__init__()
        self.title = "Compressor tool"
        self.instruments = {}
        self.width = 500
        self.height = 300

        self.centralWidget = QWidget()

        self.thread_pool = QThreadPool()

        self.settings = {"username": "", "password": "", "sender": "", "receiver": ""}

        self.init_ui()
        self.init_menu_bar()

    def init_ui(self):
        """
        Build user interface.

        :return:
        :rtype: NoneType
        """
        _, _, width, height = QDesktopWidget().screenGeometry().getCoords()
        # set position of the window relative to the dimensions of the display screen
        self.setGeometry(int(0.02 * width), int(0.05 * height), self.width, self.height)
        # set the title of the window
        self.setWindowTitle(self.title)
        # set the icon of the window

        self.main_layout = QVBoxLayout()

        self.instrument_table = QTableWidget(0, 4)
        self.instrument_table.setHorizontalHeaderLabels(("Name", "Address", "Last check", "Status"))
        header = self.instrument_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.instrument_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.main_layout.addWidget(self.instrument_table)
        self.centralWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralWidget)

        self.show()

    def init_menu_bar(self):
        """
        Build menu bar, and actions in it.

        :return:
        :rtype: NoneType
        """

        add_instrument_action = QAction("&Add", self)
        add_instrument_action.setStatusTip("Add new instrument to monitor")
        add_instrument_action.triggered.connect(self.add_instrument)

        exit_action = QAction("&Exit", self)
        # add shortcut to this action
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        # connect action to exit method
        exit_action.triggered.connect(self.exit)

        start_monitoring_action = QAction("&Start monitoring", self)
        start_monitoring_action.setStatusTip("Run a loop that checks instruments every n seconds")
        start_monitoring_action.triggered.connect(self.run_monitoring_loop)

        stop_monitoring_action = QAction("Stop monitoring", self)
        stop_monitoring_action.triggered.connect(self.stop_worker)
        stop_monitoring_action.setDisabled(True)

        check_all_action = QAction("&Check All", self)
        check_all_action.setStatusTip("Check status of all monitored instruments")
        check_all_action.triggered.connect(self.check_all)

        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(add_instrument_action)
        file_menu.addAction(start_monitoring_action)
        file_menu.addAction(stop_monitoring_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(settings_action)
        edit_menu.addSeparator()
        edit_menu.addAction(check_all_action)

    def exit(self):
        """
        Method called upon closing main window. Closes all other windows belongig to this application

        :return:
        :rtype: NoneType
        """
        print("Closing all windows and exiting the application . . .")
        app = QGuiApplication.instance()
        app.closeAllWindows()
        self.close()

    def closeEvent(self, *args, **kwargs):
        """
        Overload pyqts close event to call the local exit method.

        :param args: arguments
        :param kwargs: key word arguments
        :return:
        :rtype: NoneType
        """
        self.exit()

    def add_instrument(self, data, instruments=None):
        """
        Open a small widget that allows user to input data needed to connect to the instrument. Widget has an OK button
         which when clicked emits a pyqtSignal. This signal is connected to a method that tries to connect to the
         instrument specified by the user input in the widget. If the connection is successful the instrument is added
         to the table, otherwise a msg is displayed to user informing him that the connection was not successful.

        :param data:
        :param instruments:
        :return:
        """
        # Opens a mini window that allows user to input i guess IP and PORT and maybe some instrument name to easily
        # recognize the instruments
        if instruments is not None:
            for name, instrument in instruments.items():
                self.attempt_instr_connect(instrument)
        else:
            self.aiw = AddInstrumentWidget()
            self.aiw.submitted.connect(self.attempt_instr_connect)

    def attempt_instr_connect(self, data):
        """
        Try to connect to the instrument. If it succeeds, add the instrument to the table of instruments, otherwise
        return

        TODO 1: Check that name is not taken

        :return:
        :rtype: NoneType
        """
        try:
            instr = Pump(data["name"], data["ip"], data["port"])
        except Exception as e:
            show_error_message("Exception was caught !", str(e))
        else:
            self.add_instr_to_table(instr)

    def add_instr_to_table(self, instr):
        """
        A method that creates a new row in the instruments table and adds the instrument to it.

        :param instr: Pump object
        :type instr: Pump
        :return:
        :rtype: NoneType
        """
        rows = self.instrument_table.rowCount()
        self.instrument_table.insertRow(rows)
        table_item = QTableWidgetItem(instr.name)
        table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.instrument_table.setItem(rows, 0, table_item)
        address_item = QTableWidgetItem(instr.ip + "::" + str(instr.port))
        address_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.instrument_table.setItem(rows, 1, address_item)
        self.instrument_table.setItem(rows, 2, QTableWidgetItem(instr.last_check))
        self.instrument_table.setItem(rows, 3, QTableWidgetItem(instr.status))

        self.instruments[instr.name] = instr

    def update_table(self, row, temp, errors):
        """
        Updates the vales of a certain row in the instruments table.

        :param row: A row in the instrument table which is to be updated
        :type row: int
        :param temp: Last obtained temperature of the oil
        :type temp: int
        :param errors: Indicator if there are any errors returned by the instrument
        :type errors: bool
        :return:
        :rtype: NoneType
        """
        self.instrument_table.item(row, 2).setText(asctime())
        self.instrument_table.item(row, 3).setText("T: {} || Err: {}".format(temp, errors))

    def check_all(self):
        """
        Method that queries for the data for each instrument in the instrument table and if there are any problems it
        calls the method that sends the email. If there are no problems, it calls the method that updates the rows in
        the table.

        :return:
        :rtype: NoneType
        """
        for row in range(self.instrument_table.rowCount()):
            instr_name = self.instrument_table.item(row, 0).text()
            temp, errors = self.instruments[instr_name].check_status()
            limit = self.instruments[instr_name].alert_temp
            if temp >= limit:
                print("Alerting for temp {}".format(temp))
                self.temp_alert({"last_check": self.instrument_table.item(row, 2).text(),
                                 "instr": instr_name,
                                 "temp": temp})
            else:
                print(temp)
                self.update_table(row, temp, errors)
                self.instrument_table.viewport().update()

    def open_settings(self):
        """
        This method opens the settings widget that allows the user the input login data, and adjust some settings of
        each instrument. Submit signal of that widget is connected to update settings mathod in this widget.

        :return:
        :rtype: NoneType
        """
        self.sw = SettingsWidget(self)
        self.sw.submitted.connect(self.update_settings)
        self.sw.show()

    def run_monitoring_loop(self):
        """
        This method passes check_all() method to a thread worker so it could be ran in a separate thread from the GUI.
        Prior to starting the thread it checks if the Alert object can be instantiated.

        :return:
        """
        if self.ready_to_alert():
            self.worker = Worker(self.check_all, True)
            self.thread_pool.start(self.worker)
        else:
            show_error_message("You need to login to be able to send alerts", "You did not login. Please do it.")

    def stop_worker(self):
        """
        Set the stop request flag of the thread worker to be true so the next time when worker checks this flag it would
        stop the execution.

        :return:
        :rtype: NoneType
        """
        self.worker.stop_requested = True

    def temp_alert(self, data):
        """
        Method that instantiates Alert object and calls its method for sending alert email to a specified address.

        :param data: Data about the state of the instrument
        :type data: dict
        :return:
        :rtype: NoneType
        """
        alert = Alert(self.settings["receiver"], self.settings["sender"],
                      self.settings["username"], self.settings["password"])
        sleep(5)
        alert.send_msg(*alert.format_temperature_alert_msg(data))

    def error_alert(self, data):
        """
        Method that instantiates Alert object and calls its method for sending alert email to a specified address.

        :param data: Data about the state of the instrument
        :type data: dict
        :return:
        :rtype: NoneType
        """
        pass

    def ready_to_alert(self):
        """
        A method that creates an Alert object to check if the login data is correct.

        :return: True if the object was successfuly instantiated, else False
        :rtype: bool
        """
        try:
            test_alert = Alert(self.settings["receiver"], self.settings["sender"],
                               self.settings["username"], self.settings["password"])
        except Exception as e:
            return False
        else:
            del test_alert
            return True

    def update_settings(self, settings):
        """
        Update internally saved settings after they have been changed in the settings widget.

        :param settings: dictionary containing all the settings changeable in the settings widget
        :type settings: dict
        :return:
        :rtype: NoneType
        """
        for k, v in settings.items():
            if k in self.settings:
                self.settings[k] = v
            else:
                self.instruments[k].set_temp_alert_limit(v)


def main():
    app = QApplication(sys.argv)
    cm = CompressorMonitor()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()