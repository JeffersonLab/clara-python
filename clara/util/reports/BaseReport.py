# coding=utf-8

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.ClaraLang import ClaraLang


class BaseReport(object):

    name = xMsgConstants.UNDEFINED
    language = xMsgConstants.UNDEFINED
    author = xMsgConstants.UNDEFINED
    description = xMsgConstants.UNDEFINED
    start_time = xMsgConstants.UNDEFINED
    snapshot_time = xMsgConstants.UNDEFINED
    requests_count = 0

    def __init__(self, name, author, description=""):
        self.name = name
        self.author = author
        self.language = str(ClaraLang.PYTHON)
        self.description = description
        self.start_time = xMsgUtil.current_time()
        self.snapshot_time = xMsgUtil.current_time()

    def _snap(self):
        self.snapshot_time = xMsgUtil.current_time()

    def as_dict(self, exclude_list=[]):
        self._snap()
        key_set = set(self.__dict__.keys()) - set(exclude_list)
        return {k: self.__dict__[k] for k in key_set}

    def increment_requests_count(self):
        self.requests_count += 1
