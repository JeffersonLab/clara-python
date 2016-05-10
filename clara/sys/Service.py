# coding=utf-8

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.sys.ServiceSysConfig import ServiceSysConfig
from clara.sys.ServiceEngine import ServiceEngine
from clara.util.ClaraLogger import ClaraLogger
from clara.util.CConstants import CConstants
from clara.util.RequestParser import RequestParser


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
        super(Service, self).__init__(name.canonical_name(),
                                      local_address.host,
                                      frontend_address.host,
                                      local_address.pub_port,
                                      frontend_address.port)

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
        self._engine = self._load_engine(self._engine_class, self._engine_name)
        engine_instance = self._engine()
        self._service_sys_config = ServiceSysConfig(name.canonical_name,
                                                    initial_state)
        self._engine_pool = []
        for _ in range(self._pool_size):
            self._engine_pool.append(ServiceEngine(name.canonical_name(),
                                                   local_address,
                                                   frontend_address,
                                                   engine_instance,
                                                   self._service_sys_config))
        self._logger.log_info("deploying service...")
        # Get description defined in the service engine
        self.description = engine_instance.get_description()

        try:
            # Subscribe messages addressed to this service container
            topic = ClaraUtils.build_topic(CConstants.SERVICE, self.myname)
            self.subscription_handler = self.listen(topic,
                                                    _ServiceCallBack(self))
            self._logger.log_info("service deployed")

        except Exception as e:
            self._logger.log_exception(str(e))
            raise e

    def __repr__(self):
        return str("Service:%s" % self.myname)

    def configure(self, message):
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

    def execute(self, msg):
        while True:
            for engine in self._engine_pool:
                if engine.try_acquire_semaphore():
                    try:
                        engine.execute(msg)
                    except Exception as e:
                        self._logger.log_exception(e.message)
                    finally:
                        engine.release_semaphore()
                    return

    def setup(self, message):
        setup = RequestParser.build_from_message(message)
        report = setup.next_string()
        value = setup.next_integer()

        if report == CConstants.SERVICE_REPORT_DONE:
            self._service_sys_config.done_request = True
            self._service_sys_config.done_report_threshold = value
            self._service_sys_config.reset_done_request_count()

        elif report == CConstants.SERVICE_REPORT_DATA:
            self._service_sys_config.data_request = True
            self._service_sys_config.data_report_threshold = value
            self._service_sys_config.reset_data_request_count()

        else:
            self._logger.log_error("invalid report request: %s" % str(report))

    def exit(self):
        self.stop_listening(self.subscription_handler)
        self._logger.log_info("service stopped")

    def _load_engine(self, module_name, engine_name):
        try:
            loaded_module = __import__(module_name, fromlist=[engine_name])
            return getattr(loaded_module, engine_name)

        except ImportError as e:
            self._logger.log_exception(e.message)
            raise e


class _ServiceCallBack(xMsgCallBack):

    def __init__(self, service):
        self._service = service
        self._logger = ClaraLogger(repr(service))

    def callback(self, msg):
        try:
            if msg.metadata.action == xMsgMeta.EXECUTE:
                self._logger.log_info("received : EXECUTE")
                self._service.execute(msg)

            elif msg.metadata.action == xMsgMeta.CONFIGURE:
                self._logger.log_info("received : CONFIGURE")
                self._service.configure(msg)

            else:
                self._logger.log_info("received : SETUP")
                self._service.setup(msg)

        except Exception as e:
            self._logger.log_exception(str(e))
