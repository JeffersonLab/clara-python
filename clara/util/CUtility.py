# coding=utf-8

from xmsg.core.xMsgUtil import xMsgUtil


class CUtility(object):

    @staticmethod
    def form_canonical_name(host, container, engine_name):

        """
        Constructs and returns CLARA specified canonical name.
        For e.g. service name convention, i.e. host:container:engine

        Args:
            host (String): DPE host IP address
            container (String): Clara service container name
            engine_name (String): Clara service engine name

        Returns:
            canonical name of the Clara service
        """
        return "%s:%s:%s" % (xMsgUtil.host_to_ip(host),
                             str(container), str(engine_name))

    @staticmethod
    def remove_first(input_string, first_character):
        if input_string.startswith(first_character):
            return input_string[1:]
        else:
            return input_string
