import socket
import time
from core.xMsgConstants import xMsgConstants

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
        return CUtility.host_to_ip(host) + ":" + str(container) + ":" + str(engine_name)

    @staticmethod
    def get_domain(canonical):
        """
        Parses canonical name of a service or a container
        and returns IP of a host where service or container is running.

        :param canonical: Clara service or container canonical name
        :return: doted notation of the DPE host
        """
        if ":" not in canonical:
            raise Exception("error: malformed canonical name.")
        else:
            st = canonical.split(":")
            if "." not in st[0]:
                raise Exception("error: malformed DPE host IP address.")
            else:
                ip = st[0]
                return str(ip)

    @staticmethod
    def get_subject(canonical):
        """
        Returns service container name from the Clara service canonical name

        :param canonical: Clara service or container canonical name
        :return: Clara service container name
        """
        if ":" not in canonical:
            raise Exception("error: malformed canonical name.")
        else:
            st = canonical.split(":")
            if len(st) < 2:
                raise Exception("error: malformed canonical name.")
            else:
                container_name = st[1]
                return str(container_name)

    @staticmethod
    def get_type(canonical):
        """
        Returns service engine name from the Clara service canonical name

        :param canonical: Clara service canonical name
        :return: Clara service engine name
        """
        if ":" not in canonical:
            raise Exception("error: malformed canonical name.")
        else:
            st = canonical.split(":")
            if len(st) < 3:
                raise Exception("error: malformed canonical name.")
            else:
                engine_name = st[1]
                return str(engine_name)

    @staticmethod
    def host_to_ip(hostname):

        """
        Converts host name to IP address representation

        :param hostname:
        :return: IP address of the required host
        """
        if hostname == xMsgConstants.LOCALHOST:
            return CUtility.get_local_ip()
        else:
            if any(c.isalpha() for c in hostname):
                return socket.gethostbyname(hostname)
            else:
                return hostname

    @staticmethod
    def get_local_ip():
        local_host = socket.gethostbyname(socket.gethostname())
        return local_host

    @staticmethod
    def list_to_string(in_l):
        return ', '.join(map(str, in_l))

    @staticmethod
    def string_to_list(in_d):
        return in_d.split(",")

    @staticmethod
    def sleep(second):
        time.sleep(second)

