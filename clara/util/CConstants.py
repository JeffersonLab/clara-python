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

    DPE = "dpe"
    START_DPE = "startDpe"
    STOP_DPE = "stopDpe"
    DPE_UP = "dpeIsUp"
    DPE_DOWN = "dpeIsDown"
    DPE_PING = "dpePing"
    DPE_EXIT = "dpeExit"
    DPE_ALIVE = "dpeAlive"
    LIST_DPES = "listDpes"

    CONTAINER = "container"
    START_CONTAINER = "startContainer"
    STOP_CONTAINER = "stopContainer"
    CONTAINER_UP = "containerIsUp"
    CONTAINER_DOWN = "containerIsDown"
    REMOVE_CONTAINER = "removeContainer"
    LIST_CONTAINERS = "listContainers"

    SERVICE = "service"
    START_SERVICE = "startService"
    STOP_SERVICE = "stopService"
    DEPLOY_SERVICE = "deployService"
    REMOVE_SERVICE = "removeService"
    SERVICE_UP = "serviceIsUp"
    SERVICE_DOWN = "serviceIsDown"
    SERVICE_REPORT_DONE = "serviceReportDone"
    SERVICE_REPORT_DATA = "serviceReportData"
    RUN_SERVICE = "runService"
    LIST_SERVICES = "listServices"

    SHARED_MEMORY_KEY = "clara/shmkey"
    ALIVE = "alive"

    TOPIC_SEP = ":"
    DATA_SEP = "?"
    LANG_SEP = "_"

    BENCHMARK = 10000

    UNDEFINED = "undefined"
