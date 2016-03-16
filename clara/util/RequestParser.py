# coding=utf-8


class RequestParser(object):

    def __init__(self, data):
        """

        Args:
            data (String): data request string
        """
        self.cmd_data = data
        self.tokens = data.split("?")

    @classmethod
    def build_from_message(cls, msg):
        """Class method that builds Request parser from Clara transient message

        Args:
            msg (xMsgMessage): xMsgMessage object

        Returns:
            RequestParser object
        """

        if msg.get_metadata().dataType == "text/string":
            return cls(msg.get_data())

        else:
            raise Exception("Invalid mimetype: " + msg.get_metadata().dataType)

    def next_string(self):
        """Returns the following string from the Request

        Returns:
            cmd_data (String): string token from request
        """
        try:
            return self.tokens.pop(0)

        except IndexError:
            raise Exception("Invalid request: " + self.cmd_data)

    def next_integer(self):
        """Returns the following integer from the Request

        Returns:
            cmd_data (int): string token from request
        """
        try:
            return int(self.tokens.pop(0))

        except IndexError:
            raise Exception("Invalid request: " + self.cmd_data)
