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

from abc import ABCMeta, abstractmethod


class Engine:

    __metaclass__ = ABCMeta

    @abstractmethod
    def configure(self, engine_data):
        pass

    @abstractmethod
    def execute(self, engine_data):
        pass

    @abstractmethod
    def execute_group(self, inputs):
        pass

    @abstractmethod
    def get_input_data_types(self):
        pass

    @abstractmethod
    def get_output_data_types(self):
        pass

    @abstractmethod
    def get_states(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def get_author(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def destroy(self):
        pass
