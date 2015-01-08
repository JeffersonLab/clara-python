import socket

__author__ = 'gurjyan'


class CConstants:

    def __init__(self):
        pass

    # Note: out means outside of the Clara cloud, i.e. port
    # that orchestrator, monitors, etc will be connecting to.
    # Attention: sub or pub means that Clara cloud proxy is
    # subscribing and/or publishing, NOT the Clara inner components.
    p_external_in = b"7771"
    p_external_out = b"7772"

    # Note: in means inside of the Clara cloud, i.e. port
    # that DPEs, containers and services will be connecting to.
    p_internal_in = b"8881"
    p_internal_out = b"8882"

    # DPE proxy ports. This ports are used for service communications,
    # with the exception of d_sub port that is used by orchestrator
    # to communicate with a first service in an application service chain.
    d_external_in = b"7773"
    d_internal_out = b"8883"

    # Registrar service listening port (request-reply pattern)
    r_port = b"8888"

    ANY_HOST = b"*"

    # Discovery service action strings
    DISCOVERY_ADD_SERVICE = b"register_service"
    DISCOVERY_ADD_DPE = b"register_dpe"
    DISCOVERY_REMOVE_SERVICE = b"remove_service"
    DISCOVERY_REMOVE_DPE = b"remove_dpe"
    DISCOVERY_LIST_SERVICES_ENGINE = b"list_services_by_engine"
    DISCOVERY_LIST_SERVICES_HOST = b"list_services_by_host"
    DISCOVERY_LIST_DPES = b"list_dpes"

    # Registrar service action strings
    REGISTRAR_ADD_SERVICE = b"add"
    REGISTRAR_REMOVE_SERVICE = b"delete"
    REGISTRAR_GET_SERVICE_DESCRIPTION = b"get_service"
    REGISTRAR_SERVICES_CONTAINER = b"get_services_container"

    # Clara message data types
    CLARA_TRANSIT = b"clara_transit"
    STRING = b"string"
    LIST_STRING = b"list_of_strings"
    UNSUPPORTED_DATA_TYPE = "unsupported_data_type"

    EMPTYSTRING = b""
    NO_RESULT = b"none"
    ERROR = b"error"
    WARNING = b"warning"

    EXCEPTION = b"exception"
    DATA = b"data"
    DONE = b"done"

    UNR = b"unregistered"
    UND = b"undefined"

    # currently set to be local host name
    # ATTENTION: do not use "localhost"
    platform_host = socket.gethostname()
