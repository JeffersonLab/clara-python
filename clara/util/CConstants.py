# coding=utf-8


class CConstants(object):

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
