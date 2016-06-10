# coding=utf-8


from xmsg.core.xMsgUtil import xMsgUtil


class ClaraLogger(object):
    """Helper class for logging relevant output """

    def __init__(self, class_name):
        """
        Args:
            class_name (String): class name of the class to log
        """
        self.__class_name = class_name

    def __warning(self):
        return "WARNING"

    def __error(self):
        return "ERROR"

    def __info(self):
        return "INFO"

    def log(self, msg_type, msg):
        """logging method with custom type tag
        Args:
            msg_type (String): type of message to log
            msg (String): message to log
        """
        log_msg = "[%s] <%s> %s" % (msg_type.upper(),
                                    self.__class_name,
                                    msg)
        xMsgUtil.log(log_msg)

    def log_error(self, msg):
        """Log error messages
        """
        self.log(self.__error(), msg)

    def log_exception(self, msg):
        """Log exception messages
        """
        self.log("EXCEPTION", msg)

    def log_info(self, msg):
        """Log info messages
        """
        self.log(self.__info(), msg)

    def log_warning(self, msg):
        """Log info messages
        """
        self.log(self.__warning(), msg)
