'''
Created on 04-05-2015

@author: royarzun
'''

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

    BENCHMARK = 10000
