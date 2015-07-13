from core.xMsgUtil import xMsgUtil

__author__ = 'gurjyan'


class CUtility(object):

    def __init__(self):
        pass

    @staticmethod
    def form_canonical_name(host, container, engine_name):

        """
        Constructs and returns CLARA specified canonical name.
        For e.g. service name convention, i.e. host:container:engine

        :param host: DPE host IP address
        :param container: Clara service container name
        :param engine_name: Clara service engine name
        :return: canonical name of the Clara service
        """
        return xMsgUtil.host_to_ip(host) + ":" + str(container) + ":" + str(engine_name)
