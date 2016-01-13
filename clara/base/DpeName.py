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

from xmsg.core.xMsgConstants import xMsgConstants
from clara.base.ClaraAddress import ClaraAddress
from clara.base.ClaraName import ClaraName


class DpeName(ClaraName):

    def __init__(self, host, port, language="python"):
        self.__dpe_host = host
        self.__dpe_port = port
        self.__dpe_language = language
        self.__dpe_address = ClaraAddress(host, port)

        if port != int(xMsgConstants.DEFAULT_PORT):
            self.__name = "%s%%d%s%s" % (host, port, "_", language)
        else:
            self.__name = "%s_%s" % (host, language)

    def canonical_name(self):
        return self.__name

    def name(self):
        return self.__name

    def language(self):
        return self.__dpe_language

    def address(self):
        return self.__dpe_address
