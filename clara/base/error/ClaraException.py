# coding=utf-8


class ClaraException(Exception):

    def __init__(self, *args, **kwargs):
        super(ClaraException, self).__init__(*args, **kwargs)
