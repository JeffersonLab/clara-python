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
from clara.base.ClaraLang import ClaraLang
from clara.util.CConstants import CConstants


class DpeName(ClaraName):

    def __init__(self, host, port, language=ClaraLang.PYTHON):
        self.__dpe_language = language
        self.__dpe_address = ClaraAddress(host, port)

        if port != int(xMsgConstants.DEFAULT_PORT):
            port = "%" + str(port)
            self.__name = "%s%s%s%s" % (host, port,
                                        CConstants.LANG_SEP, language)
        else:
            self.__name = "%s%s%s" % (host, CConstants.LANG_SEP, language)

    def __str__(self):
        return self.__name

    def name(self):
        return self.__name

    def canonical_name(self):
        return self.__name

    def language(self):
        return self.__dpe_language

    def address(self):
        return self.__dpe_address
