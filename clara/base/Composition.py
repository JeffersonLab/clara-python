# coding=utf-8
import re


class Composition(object):

    def __init__(self, composition):
        assert isinstance(composition, basestring)
        self._text = composition
        self._all_services = re.split("\+|;|&", composition)

    def __str__(self):
        return self._text

    def first_service(self):
        return self._all_services[0]
