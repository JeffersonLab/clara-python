# coding=utf-8


class ServiceState(object):

    def __init__(self, name, state):
        self._name = name
        self._state = state

    def __repr__(self):
        return "ServiceState{name=\'%s\',state=\'%s\'}" % (self.name,
                                                           self.state)

    def __key(self):
        return (self._name, self._state)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, ServiceState):
            return False
        return (self.name == other.name and
                self.state == other.state)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
