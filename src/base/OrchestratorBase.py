import random
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from src.base.CBase import CBase

from src.util.CUtility import CUtility


__author__ = 'gurjyan'


class OrchestratorBase(CBase):
    """
    Base class for Clara application orchestrator classes.
    Includes methods to connect/subscribe Clara DPEs as well
     as methods to handle naming conventions.
    """

    _discover_data = []

    def __init__(self, name="Orchestrator"):
        my_name = name + "_" + str(random.randint(1, 100))
        CBase.__init__(self, my_name)

    def get_my_name(self):
        """
        Orchestrator will subscribe the subject = to its given name.
        This will assure multiple orchestrator communication privacy.
        Constructor of this base class will generate a unique name.
        This method will return generated unique name of
        this orchestrator.

        :return: unique name of this orchestrator
        """
        return self.name

    def get_service_by_host(self, dpe_host):
        """
        Asks the Registrar service of a specified DPE
        (host) to return the registration information of
        service/services based on dpe_host

        :param dpe_host:
        :return: set of xMsgRegistrationData objects
        """
        s_name = CUtility.form_canonical_name(dpe_host, xMsgConstants.ANY, xMsgConstants.ANY)
        return self.find_service(s_name)

    def get_service_by_container(self, container_name, dpe_host=xMsgUtil.get_local_ip()):
        """
        Asks the Registrar service of a specified DPE
        (host) to return the registration information of
        service/services based on the name of the service
        container

        :param container_name: the name of the service container
        :param dpe_host:
        :return: set of xMsgRegistrationData objects
        """
        s_name = CUtility.form_canonical_name(dpe_host, container_name, xMsgConstants.ANY)
        return self.find_service(s_name)

    def get_service_by_engine(self, engine_name, dpe_host=xMsgUtil.get_local_ip()):
        """
        Asks the Registrar service of a specified DPE
        (host) to return the registration information of
        service/services based on the name of the service
        engine

        :param engine_name: the name of the service engine
        :param dpe_host:
        :return: set of xMsgRegistrationData objects
        """

        s_name = CUtility.form_canonical_name(dpe_host, xMsgConstants.ANY, engine_name)
        return self.find_service(s_name)

    def get_service_description(self, dpe_host, container, engine):
        """
        Asks the Registrar service of a specified DPE
        (host) to return the description of a service
        based on the name of the service container and
        the name of the service engine

        :param dpe_host:
        :param container: service container name
        :param engine: service engine name
        :return: Description of the service
        """
        s_name = CUtility.form_canonical_name(dpe_host, container, engine)
        s = self.find_service(s_name)
        return s[0].description

    @staticmethod
    def engine_to_composition_dpe(host, container, composition):

        """
        Parses the specified composition and replaces the engine names with
        a proper service canonical names, using specified host and container
        names.
        Note: This method assumes that all engines specified in the
              composition are deployed on a same host and the same container

        :param host: the name of the host where the services are deployed
        :param container: container name of the services.
        :param composition: string of the CLARA application composition
        :return: proper composition string with service canonical names.
        """
        # find branching compositions in supplied the composition string
        b_list = composition.split(";")

        _bName = []

        for b in b_list:

            # find participating services engine names in the composition
            s_list = b.split("+")

            # temporary list of service names. Later these list
            # are going to be used to recreate service composition string
            _sName = []

            # create a list of clara canonical names for each service engine.
            for s in s_list:

                # in case we have multiple service outputs as an input to a service
                if "," in s:
                    # temporary list of comma separated service names
                    _csName = []

                    for k in s.split(","):
                        # replace the name of a service (that for this
                        # orchestrator is the name of the engine) with
                        # the proper service name: host:engine_name
                        _csName.append(CUtility.form_canonical_name(host, container, k))
                    # recreate logical OR (, separated service names) string
                    # with actual service names
                    ts = ""
                    for cs in _csName:
                        ts = ts + cs + ","
                    ts = ts[:-1]
                    _sName.append(ts)
                else:

                    # do the same replacement for a single input case
                    if "&" in s:
                        # properly replace & at the beginning of the service canonical name
                        ss = s[1:]
                        _sName.append("&" + CUtility.form_canonical_name(host, container, ss))
                    else:
                        _sName.append(CUtility.form_canonical_name(host, container, s))

            # build the final composition
            tf = ""
            for ss in _sName:
                tf = tf + ss + "+"

            # removing the last + character
            tf = tf[:-1]
            _bName.append(tf)

        bf = ""
        for bs in _bName:
            bf = bf + bs + ";"
        bf = bf[:-1]

        return bf

    def engine_to_composition(self, composition):

        """
        Note: This method is a test method that assumes that composition is
              created using engines name only. Also this method assumes that
              we have only one service with the same engine and that these
              services are running in a local DPE.

        This method accepts composition that has engine names in it,
        and asks platform Discovery service to see if composition
        engines are deployed as services and returns composition
        with service canonical names. If at least one service is not
        deployed this method will return string = none.
        Note: the same engine can be deployed multiple times in CLARA cloud.
              This method will use the first deployed service from the Discovery
              service.

        :param composition: string of the CLARA application composition
        :return: proper composition string with service canonical names.
        """

        # find branching compositions in supplied the composition string
        b_list = composition.split(";")

        _bName = []

        for b in b_list:

            # find participating services engine names in the composition
            s_list = b.split("+")

            # temporary list of service names. Later these list
            # are going to be used to recreate service composition string
            _sName = []

            # create a list of clara canonical names for each service engine.
            for s in s_list:

                # in case we have multiple service outputs as an input to a service
                if "," in s:
                    # temporary list of comma separated service names
                    _csName = []

                    for k in s.split(","):
                        # replace the name of the engine with
                        # the proper service name: host:container:engine_name
                        # Result from the request Discovery service for
                        # a deployed service with the name of the engine

                        l = self.get_service_by_engine(k)
                        if l[0] == xMsgConstants.NO_RESULT:
                            return xMsgConstants.NO_RESULT
                        else:
                            _s_name = l[0]
                            _csName.append(_s_name.name)

                    # recreate logical OR (, separated service names) string
                    # with actual service names
                    ts = ""
                    for cs in _csName:
                        ts = ts + cs + ","
                    ts = ts[:-1]
                    _sName.append(ts)
                else:

                    # do the same replacement for a single input case
                    if "&" in s:
                        # properly replace & at the beginning of the service canonical name
                        ss = s[1:]
                        l = self.get_service_by_engine(ss)
                        if l[0] == xMsgConstants.NO_RESULT:
                            return xMsgConstants.NO_RESULT
                        else:
                            _s_name = l[0]
                            _sName.append("&" + _s_name.name)
                    else:
                        l = self.get_service_by_engine(s)
                        if l[0] == xMsgConstants.NO_RESULT:
                            return xMsgConstants.NO_RESULT
                        else:
                            _s_name = l[0]
                            _sName.append(_s_name.name)

            # build the final composition
            tf = ""
            for ss in _sName:
                print type(ss)
                tf = tf + ss + "+"

            # removing the last + character
            tf = tf[:-1]
            _bName.append(tf)

        bf = ""
        for bs in _bName:
            bf = bf + bs + ";"
        bf = bf[:-1]

        return bf

    def receive_all_errors(self, callback_function, is_sync=True):
        """
        Subscribes all error messages generated from services
        of entire Clara cloud. Only severity = 1 is supported
        for subscription. Yet you can analyze severity after
        getting xMsgData in the call back.

        :param callback_function: call back function
        :param is_sync: if true this call will block until
                        callback receives the data
        """
        sev = "1"
        self.receive(xMsgConstants.ERROR + ":" + sev,
                     callback_function,
                     is_sync)

    def receive_all_warnings(self, callback_function, is_sync=True):
        """
        Subscribes all warning messages generated from services
        of entire Clara cloud. Only severity = 1 is supported
        for subscription. Yet you can analyze severity after
        getting xMsgData in the call back.

        :param callback_function: call back function
        :param is_sync: This call will block until
                        callback receives the data
        """
        sev = "1"
        self.receive(xMsgConstants.WARNING + ":" + sev,
                     callback_function,
                     is_sync)

    def receive_all_info(self, callback_function, is_sync=True):
        """
        Subscribes all info messages generated from services
        of entire Clara cloud.

        :param callback_function: call back function
        :param is_sync: This call will block until
                        callback receives the data
        """
        self.receive(xMsgConstants.INFO,
                     callback_function,
                     is_sync)

    def receive_error(self, service_name, callback_function, is_sync=True):
        """
        Subscribes error messages generated from a specific service.
        Only severity = 1 is supported for subscription. Yet you can
        analyze severity after getting xMsgData in the call back.
        Note that service name is constructed as dpe:container:engine.
        So, one can require for example to subscribe messages from
        services from a specific dpe (dpe:*:engine) or services
        from a specific dpe and a specific container (dpe:container:*).
        The construct service_name = *:container:engine is equivalent to
        receive_all_ call. Also note that no other combinations are supported.

        :param service_name: the name of the service of interest
        :param callback_function: call back function
        :param is_sync: This call will block until
                        callback receives the data
        """
        sev = "1"
        self.receive(xMsgConstants.ERROR + ":" + sev + ":" + service_name,
                     callback_function,
                     is_sync)

    def receive_warning(self, service_name, callback_function, is_sync=True):
        """
        Subscribes warning messages generated from a specific service.
        Only severity = 1 is supported for subscription. Yet you can
        analyze severity after getting xMsgData in the call back.
        Note that service name is constructed as dpe:container:engine.
        So, one can require for example to subscribe messages from
        services from a specific dpe (dpe:*:engine) or services
        from a specific dpe and a specific container (dpe:container:*).
        The construct service_name = *:container:engine is equivalent to
        receive_all_ call. Also note that no other combinations are supported.

        :param callback_function: call back function
        :param is_sync: This call will block until
                        callback receives the data
        """
        sev = "1"
        self.receive(xMsgConstants.WARNING + ":" + sev + ":" + service_name,
                     callback_function,
                     is_sync)

    def receive_info(self, service_name, callback_function, is_sync=True):
        """
        Subscribes info messages generated from a specific service.
        Only severity = 1 is supported for subscription. Yet you can
        analyze severity after getting xMsgData in the call back.
        Note that service name is constructed as dpe:container:engine.
        So, one can require for example to subscribe messages from
        services from a specific dpe (dpe:*:engine) or services
        from a specific dpe and a specific container (dpe:container:*).
        The construct service_name = *:container:engine is equivalent to
        receive_all_ call. Also note that no other combinations are supported.

        :param callback_function: call back function
        :param is_sync: This call will block until
                        callback receives the data
        """
        self.receive(xMsgConstants.INFO + ":" +
                     service_name,
                     callback_function,
                     is_sync)