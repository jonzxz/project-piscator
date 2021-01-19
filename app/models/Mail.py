from datetime import datetime

# Class created to create prettified display for detection results
class Mail():
    def __init__(self):
        self.__sender = None
        self.__date = None
        self.__subject = None

    def __init__(self, sender: str, date: datetime, subject: str):
        self.__sender = sender
        self.__date = date
        self.__subject = subject

    def get_sender(self) -> str:
        return self.__sender

    def get_date(self) -> str:
        return self.__date

    def get_subject(self) -> str:
        return self.__subject

    def __repr__(self) -> str:
        return "Sender: {} -- Subject: {} -- Date: {}" \
        .format(self.get_sender(), self.get_subject(), self.get_date())
