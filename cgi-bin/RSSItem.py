from datetime import timedelta, datetime


class Item:
    dateadded = datetime(9999, 1, 1, 1, 1, 1)
    read = False
    old = False
    link = ""
    name = ""

    def __lt__(self, other):
        if self == other:
            return False
        if not self.read and other.read:
            return True
        if self.read and not other.read:
            return False
        if self.dateadded == other.dateadded:
            return self.name < other.name
        return self.dateadded < other.dateadded

    def __gt__(self, other):
        return not (self < other or self == other)

    def __hash__(self):
        return hash((self.link, self.dateadded))

    def __eq__(self, other):
        return self.dateadded == other.dateadded and self.link == other.link

    def __leq__(self, other):
        return self < other or self == other

    def __geq__(self, other):
        return self > other or self == other

    def isOld(self):
        self.old = (datetime.today() - self.dateadded) > timedelta(7)
        return self.old

    def isRead(self):
        return self.read

    def __init__(self, information):
        if "published_parsed" in information:
            if information["published_parsed"] is not None:
                self.dateadded = datetime(*information["published_parsed"][:6])
        if "updated_parsed" in information:
            if information["updated_parsed"] is not None:
                self.dateadded = datetime(*information["updated_parsed"][:6])
        if "link" in information:
            self.link = information["link"].encode('utf8')
        try:
            self.name = information["title"].encode('utf8')
            if self.name == "":
                self.name = self.link
        except BaseException:
            self.name = "Unknown Name"

    def get_link(self):
        return self.__link

    def get_name(self):
        return self.__name

    def __str__(self):
        return "{}\n\t{}\n\t{}\n\t{}".format(
            self.name, self.link, str(
                self.dateadded), "Read" if self.read else "Unread")
