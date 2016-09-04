# coding=utf-8

import colorama
from colorama import Fore, Style
from xmsg.core.xMsgUtil import xMsgUtil


class ClaraLogger(object):
    """Helper class for logging relevant output """

    def __init__(self, class_name):
        """
        Args:
            class_name (String): class name of the class to log
        """
        colorama.init()

        self._class_name = class_name
        self._warning = Fore.YELLOW
        self._error = Fore.RED

    def log(self, msg_type, msg):
        """logging method with custom type tag
        Args:
            msg_type (String): type of message to log
            msg (String): message to log
        """
        prefix  = msg_type
        log_msg = " <%s> %s" % (self._class_name, msg)
        xMsgUtil.log(prefix + log_msg + Style.RESET_ALL)

    def log_error(self, msg):
        """Log error messages """
        self.log(self._error, msg)

    def log_exception(self, msg):
        """Log exception messages """
        self.log("EXCEPTION", msg)

    def log_info(self, msg):
        """Log info messages """
        self.log("", msg)

    def log_warning(self, msg):
        """Log info messages """
        self.log(self._warning, msg)
