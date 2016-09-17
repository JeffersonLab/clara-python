# coding=utf-8

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara.base.ClaraBase import ClaraBase
from clara.sys.EngineLoader import EngineLoader
from clara.sys.ServiceSysConfig import ServiceSysConfig
from clara.sys.ServiceEngine import ServiceEngine
from clara.util.ClaraLogger import ClaraLogger
from clara.util.CConstants import CConstants
from clara.util.RequestParser import RequestParser
from clara.util.reports.ServiceReport import ServiceReport


class Service(ClaraBase):
    """Service container/broker class. This creates ServiceMP object pool.
    Handles subscriptions and callbacks. Calls service (service executor)
    object's run method in a separate thread.

    Attributes:
        engine_class (String): the name of the python class containing
            service engine class
        engine_name (String): the name of the service engine python class
            within the engine_container_class
        pool_size (int): Service object pool size, i.e. number of parallel
            services
    """

    def __init__(self, name, engine_class, engine_name, pool_size,
                 initial_state, local_address, frontend_address):
        """Create thread pool to run requests to this service

        Create object pool to hold the engines this service. Object pool size
        is set to be 2 in case it was requested to be 0 or negative number.

        Args:
            name (String): Service canonical name
            engine_class (String): Engine class containing Engine
            engine_name (String): Engine name
            pool_size (int): Service object pool size
            initial_state (String): Initial state
            local_address (ProxyAddress): Address info for local proxy
                connection
            frontend_address (ProxyAddress): Address info for frontend
                connection
        """
        super(Service, self).__init__(name.canonical_name(),
                                      local_address.host,
                                      local_address.pub_port,
                                      frontend_address.host,
                                      frontend_address.pub_port)
        self._logger = ClaraLogger(repr(self))
        # user provided engine class container class name
        self._engine_class = engine_class
        # actual engine class name
        self._engine_name = engine_name
        # pool size
        self._pool_size = pool_size
        # Create service executor objects and fill the pool
        self._available_object_pool = dict()
        # Dynamically loads service engine class
        engine_instance = EngineLoader(engine_class,
                                       engine_name).load_engine()
        self._service_sys_config = ServiceSysConfig(name.canonical_name,
                                                    initial_state)
        self._report = ServiceReport(self, engine_instance)
        self._engine_pool = []
        for _ in range(self._pool_size):
            self._engine_pool.append(ServiceEngine(name.canonical_name(),
                                                   local_address,
                                                   frontend_address,
                                                   engine_instance,
                                                   self._service_sys_config,
                                                   self._report))
        # Get description defined in the service engine
        self.description = engine_instance.get_description()

        try:
            # Subscribe messages addressed to this service container
            self.subscription_handler = self.listen(self.myname,
                                                    _ServiceCallBack(self))
            self._logger.log_info("service deployed")

        except Exception as e:
            self._logger.log_exception(str(e))
            raise e
        except KeyboardInterrupt:
            return

    def configure(self, message):
        """Configures engine from the engine pool

        Args:
            message (xMsgMessage): Input data for service engine
        """
        while True:
            for engine in self._engine_pool:
                if engine.try_acquire_semaphore():
                    try:
                        engine.configure(message)
                    except Exception as e:
                        self._logger.log_exception(e.message)
                    finally:
                        engine.release_semaphore()
                    return

    def execute(self, message):
        """Executes engine from the engine pool

        Args:
            message (xMsgMessage): Input data for service engine
        """
        while True:
            for engine in self._engine_pool:
                if engine.try_acquire_semaphore():
                    try:
                        engine.execute(message)
                    except Exception as e:
                        self._logger.log_exception(e.message)
                    finally:
                        engine.release_semaphore()
                    return

    def exit(self):
        """Exits the service gracefully"""
        self.stop_listening(self.subscription_handler)
        self._logger.log_info("service stopped")

    def get_engine_class(self):
        """Returns the engine class as string

        Returns:
            String
        """
        return self._engine_class

    def get_engine_name(self):
        """Returns engine name as string

        Returns:
            String
        """
        return self._engine_name

    def get_report(self):
        """Returns service report object

        Returns:
            ServiceReport
        """
        return self._report

    def _send_response(self, message, status, data):
        response_message = xMsgMessage.from_string(message.topic, data)
        response_message.metadata.status = status
        self.send(response_message)

    def setup(self, message):
        """Configure service reporting messages

        Args:
            message (xMsgMessage): message with setup request
        """
        setup = RequestParser.build_from_message(message)
        report = setup.next_string()
        value = setup.next_integer()

        for engine in self._engine_pool:
            try:
                if report == CConstants.SERVICE_REPORT_DONE:
                    engine.sys_config.done_request = True
                    engine.sys_config.done_report_threshold = value
                    engine.sys_config.reset_done_request_count()
                elif report == CConstants.SERVICE_REPORT_DATA:
                    engine.sys_config.data_request = True
                    engine.sys_config.data_report_threshold = value
                    engine.sys_config.reset_data_request_count()
                else:
                    self._logger.log_error("invalid report request: " +
                                           str(report))
            except Exception as e:
                self._logger.log_exception(e.message)
            return

        if message.has_reply_topic():
            self._send_response(message, xMsgMeta.INFO, setup)


class _ServiceCallBack(xMsgCallBack):

    def __init__(self, service):
        self._service = service
        self._logger = ClaraLogger(repr(service))

    def callback(self, msg):
        try:
            if not msg.metadata.HasField('action'):
                self._logger.log_info("received : SETUP")
                self._service.setup(msg)
            elif msg.metadata.action == xMsgMeta.EXECUTE:
                self._logger.log_info("received : EXECUTE")
                self._service.execute(msg)

            elif msg.metadata.action == xMsgMeta.CONFIGURE:
                self._logger.log_info("received : CONFIGURE")
                self._service.configure(msg)

        except Exception as e:
            self._logger.log_exception(str(e))

        finally:
            return msg
