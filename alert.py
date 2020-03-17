# This file should handle sending emails to address specified somewhere

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import asctime
from widgets.ErrorMsg import show_error_message
import re


class Alert:
    """

    """
    def __init__(self, receiver, sender, username, password):
        """
        Constructor for the Alert class. Alert class handles loging-in to the email server, and sending messages using
        the credentials provided by the user. Also makes sure that the credentials and sender/receiver data are valid
        email addresses.

        :param receiver:
        :param sender:
        :param username:
        :param password:
        """
        self.host = "owa.ist.ac.at"
        self.port = 587
        self.server = smtplib.SMTP(self.host, self.port)
        if self.check_valid_email(sender):
            self.sender = sender
        else:
            show_error_message("Invalid sender email address",
                               "Please input valid email and try again.")
            raise Exception("Invalid sender email address")
        if self.check_valid_email(receiver):
            self.receiver = receiver
        else:
            show_error_message("Invalid sender email address",
                               "Please input valid email and try again.")
            raise Exception("Invalid receiver email address")

        self.username = username
        self.password = password
        if not self.attempt_login():
            show_error_message("Failed to login. Most likely wrong credentials.",
                               "Please try again.")
            raise Exception("Failed to login")

        self.msg = MIMEMultipart()
        self.msg_text = MIMEText("")

    def attempt_login(self):
        """
        Attempt to login into server with the username and password provided in the settings window

        :return: Was login successful
        :type: bool
        """
        self.server.starttls()
        try:
            self.server.login(self.username, password=self.password)
        except Exception as e:
            self.server.close()
            show_error_message("Problem when logging into your account", str(e))
            return False
        else:
            return True

    def check_valid_email(self, email):
        """
        Regex that checks if the passed string is a valid email address

        :param email: string that needs to be checked
        :type email: str
        :return: Is passed string a valid email
        :type: bool
        """
        regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if re.search(regex, email):
            return True
        else:
            return False

    def send_msg(self, subject, content):
        """
        A method that calls methods that do pre steps, send a message, and do post steps.

        :param subject: Title of the email
        :type subject: str
        :param content: Body of the email
        :type content: str
        :return:
        :rtype: NoneType
        """
        self.format_msg(subject, content)
        self.server.send_message(self.msg)
        self.server.close()

    def format_msg(self, subject, content):
        """
        Method that knows how to format MIMEMultipart objects.

        :param subject: Title of the email
        :type subject: str
        :param content: Body of the email
        :type content: str
        :return:
        :rtype: NoneType
        """
        self.msg["From"] = self.sender
        self.msg["To"] = self.receiver
        self.msg["Subject"] = subject
        self.msg_text.set_payload(content)
        self.msg.attach(self.msg_text)

    def format_temperature_alert_msg(self, data):
        """
        Method that formats the message that will be sent when the temperature is above the limit set by user.

        :param data: Dictionary containing instrument data
        :type data: dict
        :return:
        :rtype: NoneType
        """
        subject = "Problem with temperature of one of the compressors !!"
        text = " ### ALERT ### \n" \
               "This msg was sent to you because one of your monitored instruments is out of the allowed range " \
               "for temperature.\n" \
               "Time: {} - {}\n" \
               "Instrument: {}\n" \
               "Temperature: {}".format(data["last_check"], asctime(), data["instr"], data["temp"])
        return subject, text

    def format_error_alert_msg(self, data):
        """
        Method that formats the message that will be sent when instruments has errors.

        :param data: Dictionary containing instrument data
        :type data: dict
        :return:
        :rtype: NoneType
        """
        subject = "An instrument has reported an error !!"
        text = " ### ALERT ### \n " \
               "This msg was sent to you because one of your monitored instruments is reporting an error that needs " \
               "acknowledgement." \
               "Time: {} - {}\n" \
               "Instrument: {}\"" \
               "Error: {}".format(data["last_check"], asctime(), data["instr"], data["error"])
        return subject, text


def main():

    sender_email = ""
    receiver_email = ""
    username = ""
    password = ""

    alert = Alert(sender_email, receiver_email, username, password)
    alert.send_msg(*alert.format_temperature_alert_msg({"last_check": asctime(),
                                                        "instr": "Some instruments IDN response",
                                                        "temp": "Some temperature"}))


if __name__ == "__main__":
    main()
