# coding=utf-8

import re

from ordered_set import OrderedSet

from clara.base.error.ClaraException import ClaraException
from clara.sys.ccc.Instruction import Instruction
from clara.sys.ccc.Statement import Statement
from clara.sys.ccc.Constants import Regex
from clara.sys.ccc.Condition import Condition
from clara.util.CUtility import CUtility


class CCompiler(object):

    _SYNTAX_ERROR = "Syntax error in the Clara routing program. Malformed " +\
                    "routing statement"

    def __init__(self, service_name):
        self._instructions = OrderedSet()
        self._service_name = service_name

    @staticmethod
    def _no_blanks(string):
        no_blank_str = string.strip()
        return ''.join(no_blank_str.split())

    def compile(self, composition):
        self._instructions.clear()
        ppi = list(self._pre_process(CCompiler._no_blanks(composition)))

        i = 0
        while i < len(ppi):
            scs1 = ppi[i]

            if (scs1.startswith("if(") or
                scs1.startswith("}if(") or
                scs1.startswith("}else") or
                scs1.startswith("}elseif(")):

                instruction = self._parse_condition(scs1)

                j = i + 1
                while j < len(ppi):
                    scs2 = ppi[j]
                    if (not scs2.startswith("}") and
                            not scs2.startswith("if(") and
                            not scs2.startswith("}if(") and
                            not scs2.startswith("}elseif(") and
                            not scs2.startswith("}else")):
                        if instruction:
                            self._parse_conditional_statement(scs2,
                                                              instruction)
                    else:
                        break
                    j += 1

                if instruction:
                    self._instructions.add(instruction)

            else:
                self._parse_statement(scs1)
            i += 1

        if not bool(self._instructions):
            raise ClaraException("Composition is irrelevant for a service.")
        print self._instructions

    @staticmethod
    def _pre_process(code_string):
        if code_string.find(";") == -1 and not code_string.endswith(";"):
            raise ClaraException("Syntax error in the Clara routing program." + 
                                 "Missing end of statement operator = \";\"")
        instruction_set = []
        for text in code_string.split(";"):
            if text != "" and text != "}":
                instruction_set.append(text)

        return instruction_set

    def _parse_statement(self, statement_string):
        ti = Instruction(self._service_name)
        statement_string = CUtility.remove_first(statement_string, "}")
        try:
            pattern = re.compile(Regex.ROUTING_STATEMENT)
            match = pattern.match(statement_string)

            if match:
                if not (self._service_name in statement_string):
                    return False
                ts = Statement(statement_string, self._service_name)
                ti.unconditional_statements.add(ts)
                self._instructions.add(ti)

                return True
            else:
                raise ClaraException(self._SYNTAX_ERROR)
        except Exception as e:
            print e
            raise e

    def _parse_conditional_statement(self, statement_string, instruction):
        pattern = re.compile(Regex.ROUTING_STATEMENT)
        match = pattern.match(statement_string)
        if match:
            if not (self._service_name in statement_string):
                return False

            ts = Statement(statement_string, self._service_name)

            if instruction.if_condition:
                instruction.if_statements.add(ts)
            elif instruction.elseif_statements:
                instruction.elseif_statements.add(ts)
            else:
                instruction.else_statements.add(ts)

            return True
        else:
            raise ClaraException(self._SYNTAX_ERROR)

    def _parse_condition(self, condition):
        pattern = re.compile(Regex.CONDITION)
        match = pattern.match(condition)

        if match:
            try:
                index = condition.find("{") + 1
                statement_string = condition[index:]
                if not (self._service_name in statement_string):
                    return None
                ts = Statement(statement_string, self._service_name)
                ti = Instruction(self._service_name)

                if condition.startswith("if(") or condition.startswith("}if("):
                    par1 = condition.find("(") + 1
                    par2 = condition.rfind(")")

                    tc = Condition(condition[par1:par2], self._service_name)
                    ti.if_condition = tc
                    ti.if_statements.add(ts)

                elif condition.startswith("}elseif("):
                    par1 = condition.find("(") + 1
                    par2 = condition.rfind(")")

                    tc = Condition(condition[par1:par2], self._service_name)
                    ti.elseif_condition = tc
                    ti.elseif_statements.add(ts)

                elif condition.startswith("}else"):
                    ti.else_statements.add(ts)

                return ti

            except Exception as e:
                print e
                raise ClaraException(self._SYNTAX_ERROR)

        else:
            raise ClaraException(self._SYNTAX_ERROR)

    def get_unconditional_links(self):
        uncond = set()
        for instruction in self._instructions:
            for statement in instruction.unconditional_statements:
                uncond.update(statement.get_output_links())
        return uncond

    def get_links(self, owner_ss, input_ss):
        outputs = set()
        in_condition = False
        condition_chosen = False

        for instruction in self._instructions:
            if bool(instruction.unconditional_statements):
                in_condition = False

                for statement in instruction.unconditional_statements:
                    output = statement.get_output_links()
                    outputs.update(output)
                continue

            if instruction.if_condition:
                in_condition = True
                condition_chosen = False

                if instruction.if_condition.is_true(owner_ss, input_ss):
                    condition_chosen = True
                    for statement in instruction.if_statements:
                        output = statement.get_output_links()
                        outputs.update(output)
                continue

            if in_condition and not condition_chosen:
                if instruction.elseif_condition:
                    if instruction.elseif_condition.is_true(owner_ss,
                                                            input_ss):
                        condition_chosen = True
                        for statement in instruction.elseif_statements:
                            output = statement.get_output_links()
                            outputs.update(output)
                    continue

                if instruction.else_statements:
                    condition_chosen = True

                    for statement in instruction.else_statements:
                        output = statement.get_output_links()
                        outputs.update(output)
        return outputs
