# coding=utf-8


class Instruction(object):

    def __init__(self, service_name):
        self._service_name = service_name
        self.if_condition = False
        self.elseif_condition = False
        self.if_statements = set()
        self.elseif_statements = set()
        self.else_statements = set()
        self.unconditional_statements = set()

    def __eq__(self, other):
        if self == other:
            return True
        if not isinstance(other, Instruction):
            return False

        return (self.if_condition == other.if_condition and
                self.if_statements == other.if_statements and
                self.else_statements == other.else_statements and
                self.elseif_statements == other.elseif_statements and
                self.unconditional_statements == other.unconditional_statements)

    @property
    def condition(self):
        return self.if_condition

    @condition.setter
    def condition(self, if_condition):
        self.if_condition = if_condition
