class Mail():
    def __init__(self):
        self.__sender = None
        self.__date = None
        self.__subject = None

    def __init__(self, sender, date, subject):
        self.__sender = sender
        self.__date = date
        self.__subject = subject

    def get_sender(self):
        return self.__sender

    def get_date(self):
        return self.__date

    def get_subject(self):
        return self.__subject
