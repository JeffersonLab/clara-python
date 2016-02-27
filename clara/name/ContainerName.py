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

from clara.base.DpeName import DpeName
from clara.base.ClaraName import ClaraName
from clara.util.CConstants import CConstants


class ContainerName(ClaraName):

    def __init__(self, dpe, name):
        if not isinstance(dpe, DpeName):
            raise TypeError("dpe argument must be of type DpeName")
        else:
            self.__canonical_name = str(dpe) + CConstants.TOPIC_SEP + str(name)
            self.__name = name
            self.__dpe = dpe

    def __str__(self):
        return self.canonical_name()

    def canonical_name(self):
        return self.__canonical_name

    def name(self):
        return self.__name

    def get_dpe_name(self):
        return self.__dpe
