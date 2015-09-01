#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
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

class CConstants:
    
    def __init__(self):
        pass
    
    DPE = "dpe"
    DPE_UP = "dpeIsUp"
    DPE_DOWN = "dpeIsDown"
    DPE_PING = "dpePing"
    DPE_EXIT = "dpeExit"
    START_CONTAINER = "startContainer"
    REMOVE_CONTAINER = "removeContainer"
    LIST_CONTAINERS = "listContainers"

    CONTAINER = "container"
    CONTAINER_UP = "containerIsUp"
    CONTAINER_DOWN = "containerIsDown"
    DEPLOY_SERVICE = "deployService"
    REMOVE_SERVICE = "removeService"
    RUN_SERVICE = "runService"

    SERVICE = "service"
    SERVICE_UP = "serviceIsUp"
    SERVICE_DOWN = "serviceIsDown"
    SERVICE_REPORT_DONE = "serviceReportDone"
    SERVICE_REPORT_DATA = "serviceReportData"

    ALIVE = "alive"
    
    LANG_SEP = "_"
    TOPIC_SEP = ":"
    DATA_SEP = "?"

    BENCHMARK = 10000
