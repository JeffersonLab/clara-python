# coding=utf-8


class RequestParser(object):

    def __init__(self, data):
        """

        Args:
            data (String): data request string
        """
        self._request = data
        self._tokens = data.split("?")

    @classmethod
    def build_from_message(cls, msg):
        """Class method that builds Request parser from Clara transient message

        Args:
            msg (xMsgMessage): xMsgMessage object

        Returns:
            RequestParser object
        """

        if msg.mimetype == "text/string":
            return cls(msg.data)

        else:
            raise Exception("Invalid mimetype: " + msg.mimetype)

    def next_string(self):
        """Returns the following string from the Request

        Returns:
            cmd_data (String): string token from request
        """
        try:
            return self._tokens.pop(0)

        except IndexError:
            raise Exception("Invalid request: " + self._request)

    def next_integer(self):
        """Returns the following integer from the Request

        Returns:
            cmd_data (int): string token from request
        """
        try:
            return int(self._tokens.pop(0))

        except IndexError:
            raise Exception("Invalid request: " + self._request)

    def request(self):
        """Returns request as array of str

        Returns:
            []: request string array
        """
        return self._request
