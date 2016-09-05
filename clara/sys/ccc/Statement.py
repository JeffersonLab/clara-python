# coding=utf-8

from clara.base.error.ClaraException import ClaraException
from clara.sys.ccc.utils import remove_first


class Statement(object):
    """This class presents routing schema for a service,

    result of the Clara composition compiler, parsing routing statements of a
    composition.

    Contains Map that has keys = input service names, data from which are
    required logically to be ANDed. I.e. data from all services in the AND must
    be present in order for the receiving service to execute its service
    engine.

    Also contains a Set of names of all services that are linked to the service
    of interest, i.e. names of all services that this services will send it's
    output data.
    """

    def __init__(self, statement_string, service_name):
        if service_name in statement_string:
            self._service_name = service_name
            self._statement_string = statement_string
            self._input_links = set()
            self._output_links = set()
            self._log_and_inputs = {}
            self._process()
        else:
            raise ClaraException("Irrelevant statement")

    def __repr__(self):
        return "<Statement: %s, Service: %s>" % (self._statement_string,
                                                 self._service_name)

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return False
        cmp1 = str(self.get_input_links()) == str(other.get_input_links())
        cmp2 = str(self.get_output_links()) == str(other.get_output_links())
        cmp3 = str(self.get_log_and_inputs()) == str(other.get_log_and_inputs())
        return cmp1 and cmp2 and cmp3

    def __hash__(self):
        return hash((self._service_name, self._statement_string,
                     str(self._input_links), str(self._output_links),
                     str(self._log_and_inputs)))

    @property
    def service_name(self):
        return self._service_name

    def get_input_links(self):
        return self._input_links

    def get_output_links(self):
        return self._output_links

    def get_log_and_inputs(self):
        return self._log_and_inputs

    def _process(self):
        self._parsed_linked()
        if self._is_log_and():
            for sn in self._input_links:
                self._log_and_inputs[sn] = None

    def _parsed_linked(self):
        """Parses composition field of the transient data and returns the list
        of services output linked to this service, i.e. that are getting output
        data of this service.

        Attention: service name CAN NOT appear twice in the composition.
        """
        element_list = []
        statement_iterator = iter(self._statement_string.split("+"))

        while True:
            try:
                element = statement_iterator.next()
                element = remove_first(element, "&")
                element = remove_first(element, "{")
                element_list.append(element)
            except StopIteration:
                break

        index = -1
        for element in element_list:
            index += 1
            if self._service_name in element:
                break

        if index == -1:
            raise ClaraException("Routing statement parsing exception. " + 
                                 "Service name can not be found in the " + 
                                 "statement.")

        else:
            p_index = index - 1
            if p_index >= 0:
                element = Statement._get_element(element_list, p_index)

                if "," in element:
                    element = element.split(",")
                    statement_iterator = iter(element)
                    while True:
                        try:
                            self._input_links.add(statement_iterator.next())
                        except StopIteration:
                            break
                else:
                    self._input_links.add(element)

            n_index = index + 1
            if len(element_list) > n_index:
                element = Statement._get_element(element_list, n_index)

                if "," in element:
                    element = element.split(",")
                    statement_iterator = iter(element)
                    while True:
                        try:
                            self._output_links.add(statement_iterator.next())
                        except StopIteration:
                            break
                else:
                    self._output_links.add(element)

    @staticmethod
    def _get_element(element_list, index):
        i = -1
        for element in element_list:
            i += 1
            if index == i:
                return element
        return None

    def _is_log_and(self):
        ac = "&" + self._service_name
        element_set = set()
        statement_iterator = iter(self._statement_string.split("+"))

        while True:
            try:
                element_set.add(statement_iterator.next())
            except StopIteration:
                break

        for element in element_set:
            if element == ac:
                return True
        return False
