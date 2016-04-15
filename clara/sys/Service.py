# coding=utf-8

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
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
    subscription_handler = None
    engine_pool = []

    def __init__(self, name, engine_class, engine_name, pool_size,
                 initial_state, local_address, frontend_address):
        super(Service, self).__init__(name.canonical_name(),
                                      local_address.host,
                                      frontend_address.host,
                                      local_address.pub_port,
                                      frontend_address.port)

        self.logger = ClaraLogger(repr(self))
        # user provided engine class container class name
        self.engine_class = engine_class
        # actual engine class name
        self.engine_name = engine_name
        # initial state of the service
        self.initial_state = initial_state
        # pool size
        self.pool_size = pool_size
        # Create service executor objects and fill the pool
        self.available_object_pool = dict()
        # Dynamically loads service engine class
        engine_class = self.__load_engine(self.engine_class, self.engine_name)
        self.engine_object = engine_class()

        for engine_count in range(self.pool_size):
            engine_name = "%s-%d" % (name.canonical_name(), engine_count)
            self.engine_pool.append(ServiceEngine(engine_name,
                                                  local_address,
                                                  frontend_address,
                                                  self.engine_object,
                                                  'blah'))
        self.logger.log_info("deploying service...")

        # Get description defined in the service engine
        self.description = self.engine_object.get_description()

        try:
            # Subscribe messages addressed to this service container
            topic = ClaraUtils.build_topic(CConstants.SERVICE, self.myname)
            self.subscription_handler = self.listen(topic, _ServiceCallBack(self))
            self.logger.log_info("service deployed")

        except Exception as e:
            self.logger.log_exception(str(e))
            raise e

    def __repr__(self):
        return str("Service:%s" % self.myname)

    def configure(self, msg):
        while True:
            for engine in self.engine_pool:
                if engine.try_acquire():
                    try:
                        engine.configure(msg)
                    except Exception as e:
                        self.logger.log_exception(e.message)
                    finally:
                        engine.release()
            return

    def execute(self, msg):
        while True:
            for engine in self.engine_pool:
                if engine.try_acquire():
                    try:
                        engine.execute(msg)
                    except Exception as e:
                        self.logger.log_exception(e.message)
                    finally:
                        engine.release()
            return

    def setup(self, msg):
        setup = RequestParser.build_from_message(msg)
        report = setup.next_string()
        value = setup.next_integer()

        if report == CConstants.SERVICE_REPORT_DONE:
            # TODO: Implement ServiceSysConfig
            pass

        elif report == CConstants.SERVICE_REPORT_DATA:
            # TODO: Implement ServiceSysConfig
            pass

        else:
            self.logger.log_error("invalid report request: %s" % str(report))

    def exit(self):
        self.stop_listening(self.subscription_handler)
        self.logger.log_info("service stopped")

    def __load_engine(self, module_name, engine_name):
        loaded_module = __import__(module_name, fromlist=[engine_name])
        try:
            self.service_object = getattr(loaded_module, engine_name)

        except ImportError as e:
            self.logger.log_exception(str(e))
            raise e

        return self.service_object


class _ServiceCallBack(xMsgCallBack):

    def __init__(self, service):
        self.service = service

    def callback(self, msg):
        try:
            metadata = xMsgMeta()
            metadata.MergeFrom(msg.metadata)
            if metadata.action == 0:
                self.service.logger.log_info("received : SETUP")
                self.service.setup(msg)

            elif metadata.action == xMsgMeta.CONFIGURE:
                self.service.logger.log_info("received : CONFIGURE")
                self.service.configure(msg)

            else:
                self.service.logger.log_info("received : EXECUTE")
                self.service.execute(msg)

        except Exception as e:
            self.service.logger.log_exception(str(e))
