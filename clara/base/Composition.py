# coding=utf-8


class Composition(object):

    def __init__(self, composition):
        assert isinstance(composition, basestring)
        self._text = composition
        self._all_services = [s.strip() for s in composition.split("+;&,")]

    def __str__(self):
        return self._text

    def first_service(self):
        return self._all_services[0]
