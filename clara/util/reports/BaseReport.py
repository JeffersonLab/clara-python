# coding=utf-8

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.ClaraLang import ClaraLang


class BaseReport(object):

    name = xMsgConstants.UNDEFINED
    lang = xMsgConstants.UNDEFINED
    author = xMsgConstants.UNDEFINED
    description = xMsgConstants.UNDEFINED
    start_time = xMsgConstants.UNDEFINED
    snapshot_time = xMsgConstants.UNDEFINED
    requests_count = xMsgConstants.UNDEFINED

    def __init__(self, name, author, description=""):
        self.name = name
        self.author = author
        self.lang = ClaraLang.PYTHON
        self.description = description
        self.start_time = xMsgUtil.current_time()

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def lang(self):
        return self.lang

    @lang.setter
    def lang(self, lang):
        self.lang = lang

    @property
    def author(self):
        return self.author

    @author.setter
    def author(self, author):
        self.author = author

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, description):
        self.description = description

    @property
    def start_time(self):
        return self.start_time

    @start_time.setter
    def start_time(self, start_time):
        self.start_time = start_time

    @property
    def snapshot_time(self):
        return self.snapshot_time

    @snapshot_time.setter
    def snapshot_time(self, snapshot_time):
        self.snapshot_time = snapshot_time

    @property
    def requests_count(self):
        return self.snapshot_time

    @requests_count.setter
    def requests_count(self, requests_count):
        self._requests_count = requests_count
