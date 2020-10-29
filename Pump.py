# This is a file that represents the pump instrument and all the communication with the instrument will be handled from
# this file

from time import asctime
from random import randint


class Pump:
    """
    TODO: Study how the instrument works and write the driver for it
    """
    def __init__(self, name, address, port):
        """
        TODO: Write documentation
        TODO: Rewrite this driver to work with TELNET

        :param name:
        :param address:
        :param port:
        """
        self.name = name
        self.ip = address
        self.port = port
        self.last_check = "Never"
        self.status = "Unknown"
        self.temp = None
        self.error = None

        self.temp_limit = self.get_temp_limit()
        self.alert_temp = self.temp_limit - (0.1 * self.temp_limit)

    def check_status(self):
        """
        TODO: Write documentation

        :return:
        """
        self.temp = self.get_temp()
        self.error = self.get_errors()
        self.last_check = asctime()
        return self.temp, self.error

    def get_temp(self):
        """
        TODO: One of the two methods that needs to communicate with the real instrument
        TODO: Write documentation

        :return:
        """
        # in reality i should get this from the instrument, this is just for testing
        return randint(0, 100)

    def get_errors(self):
        """
        TODO: One of the two methods that needs to communicate with the real instrument
        TODO: Write documentation

        :return:
        """
        # in reality i should get this from the instrument, this is just for testing
        return False

    def get_temp_limit(self):
        """
        TODO: Write documentation

        :return:
        """
        # in reality i should get this from the instrument, this is just for testing
        return 90

    def set_temp_alert_limit(self, value):
        """
        TODO: Write documentation

        :param value:
        :return:
        """
        self.alert_temp = value


def main():
    pass


if __name__ == "__main__":
    main()
