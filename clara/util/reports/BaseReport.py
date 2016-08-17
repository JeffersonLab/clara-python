# coding=utf-8

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.ClaraLang import ClaraLang


class BaseReport(object):

    _name = xMsgConstants.UNDEFINED
    _lang = xMsgConstants.UNDEFINED
    _author = xMsgConstants.UNDEFINED
    _description = xMsgConstants.UNDEFINED
    _start_time = xMsgConstants.UNDEFINED
    _snapshot_time = xMsgConstants.UNDEFINED
    _requests_count = xMsgConstants.UNDEFINED

    def __init__(self, name, author, description):
        self._name = name
        self._author = author
        self._lang = ClaraLang.PYTHON
        self._description = description
        self._start_time = xMsgUtil.current_time()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def snapshot_time(self):
        return self._snapshot_time

    @snapshot_time.setter
    def snapshot_time(self, snapshot_time):
        self._snapshot_time = snapshot_time

    @property
    def requests_count(self):
        return self._snapshot_time

    @requests_count.setter
    def requests_count(self, requests_count):
        self._requests_count = requests_count
