# coding=utf-8

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.net.xMsgAddress import ProxyAddress


class ClaraAddress(ProxyAddress):

    def __init__(self, host, port=xMsgConstants.DEFAULT_PORT):
        super(ClaraAddress, self).__init__(host, port)
