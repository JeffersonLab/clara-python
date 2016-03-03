#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from xmsg.core.xMsgUtil import xMsgUtil


class ClaraLogger(object):
    """Helper class for logging relevant output

    """
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

    def log_info(self, msg):
        """Log info messages
        """
        self.log(self.__info(), msg)

    def log_warning(self, msg):
        """Log info messages
        """
        self.log(self.__warning(), msg)
