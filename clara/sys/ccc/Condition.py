# coding=utf-8

import re

from clara.base.error.ClaraException import ClaraException
from clara.sys.ccc.ServiceState import ServiceState
from clara.sys.ccc.Constants import Regex


class Condition(object):
    
    _CONDITION_ERROR = "syntax error: malformed conditional statement"

    def __init__(self, condition_string, service_name):
        self._service_name = service_name
        self.and_states = set()
        self.and_not_states = set()
        self.or_states = set()
        self.or_not_states = set()
        self._process(condition_string)

    def _process(self, condition_string):
        if condition_string.find("(") != -1:
            condition_string.replace("\\C", "")

        if condition_string.find(")") != -1:
            condition_string.replace("\\)", "")

        if condition_string.find("&&") != -1:
            self._parse_condition(condition_string, "&&")

        elif condition_string.find("!!") != -1:
            self._parse_condition(condition_string, "!!")

        else:
            self._parse_condition(condition_string, None)

    def _parse_condition(self, condition_string, operator):
        if operator:
            if condition_string.find("&&") != -1 and\
               condition_string.find("!!") == -1:
                iterator = iter(condition_string.split(operator))
                while True:
                    try:
                        ac = iterator.next()
                        pattern = re.compile(Regex.COMPLEX_CONDITION)
                        match = pattern.match(ac)

                        if match:
                            if ac.find("!=") != -1:
                                condition = ac.next()
                                condition = condition.split("!=")

                                if len(condition) != 2:
                                    raise ClaraException(self._CONDITION_ERROR)

                                self.and_not_states.add(ServiceState(condition[0],
                                                                     condition[1]))

                            elif ac.find("==") != -1:
                                condition = ac.next()
                                condition = condition.split("==")

                                if len(condition) != 2:
                                    raise ClaraException(self._CONDITION_ERROR)

                                self.and_states.add(ServiceState(condition[0],
                                                                 condition[1]))

                            else:
                                raise ClaraException(self._CONDITION_ERROR)
                        else:
                            raise ClaraException(self._CONDITION_ERROR)

                    except StopIteration:
                        break

            elif (condition_string.find("!!") != -1 and
                  condition_string.find("&&") == -1):
                iterator = iter(condition_string.split(operator))

                while True:
                    try:
                        ac = iterator.next()
                        pattern = re.compile(Regex.SIMPLE_CONDITION)
                        match = pattern.match(ac)

                        if match:
                            if ac.find("!=") != -1:
                                condition = ac.next()
                                condition = condition.split("!=")

                                if len(condition) != 2:
                                    raise ClaraException(self._CONDITION_ERROR)
                                self.or_not_states.add(ServiceState(condition[0],
                                                                    condition[1]))

                            elif ac.find("==") != -1:
                                condition = ac.next()
                                condition = condition.split("==")

                                if len(condition) != 2:
                                    raise ClaraException(self._CONDITION_ERROR)
                                self.or_states.add(ServiceState(condition[0],
                                                                condition[1]))
                            else:
                                raise ClaraException(self._CONDITION_ERROR)
                        else:
                            raise ClaraException(self._CONDITION_ERROR)
                    except StopIteration:
                        break

            else:
                raise ClaraException(self._CONDITION_ERROR)

        else:
            pattern = re.compile(Regex.SIMPLE_CONDITION)
            match = pattern.match(condition_string)

            if match:
                if condition_string.find("!=") != -1:
                    condition = condition_string.split("!=")

                    if len(condition) != 2:
                        raise ClaraException(self._CONDITION_ERROR)
                    self.or_not_states.add(ServiceState(condition[0],
                                                        condition[1]))

                elif condition_string.find("==") != -1:
                    condition = condition_string.split("==")
                    if len(condition) != 2:
                        raise ClaraException(self._CONDITION_ERROR)
                    self.or_states.add(ServiceState(condition[0],
                                                    condition[1]))
                else:
                    raise ClaraException(self._CONDITION_ERROR)
            else:
                raise ClaraException(self._CONDITION_ERROR)

    def is_true(self, owner_ss, input_ss):
        c1 = Condition._check_and_condition(self.and_states, owner_ss,
                                            input_ss)
        c2 = Condition._check_and_condition(self.and_not_states, owner_ss,
                                            input_ss)
        c3 = Condition._check_or_condition(self.or_states, owner_ss, input_ss)
        c4 = Condition._check_or_condition(self.or_not_states, owner_ss,
                                           input_ss)
        return c1 and c2 and c3 and c4

    @staticmethod
    def _check_and_condition(ss_set, ss1, ss2):
        return ((ss1 in ss_set) and (ss2 in ss_set)) or not bool(len(ss_set))

    @staticmethod
    def _check_or_condition(ss_set, ss1, ss2):
        return (ss1 in ss_set) or (ss2 in ss_set) or not bool(len(ss_set))
