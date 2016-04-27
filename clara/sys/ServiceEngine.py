# coding=utf-8

from threading import Semaphore

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgTopic import xMsgTopic

from clara.base.ClaraBase import ClaraBase
from clara.engine.EngineData import EngineData
from clara.engine.EngineDataType import Mimetype
from clara.engine.EngineStatus import EngineStatus
from clara.sys.ccc.CCompiler import CCompiler
from clara.sys.ccc.ServiceState import ServiceState
from clara.util.ClaraLogger import ClaraLogger


class ServiceEngine(ClaraBase):

    execution_time = 0

    def __init__(self, name, local_address, frontend_address, user_engine,
                 configuration):
        super(ServiceEngine, self).__init__(name,
                                            local_address.host,
                                            frontend_address.host,
                                            local_address.pub_port,
                                            frontend_address.port)
        self._engine_object = user_engine
        self._semaphore = Semaphore(1)
        self._sys_config = configuration
        self._compiler = CCompiler(self.myname)
        self._prev_composition = "undefined"
        self._logger = ClaraLogger(repr(self))

    def configure(self, msg):
        input_data = EngineData()
        out_data = None
        try:
            input_data = self._get_engine_data(msg)
            out_data = self._configure_engine(input_data)
        except Exception as e:
            self._logger.log_exception(e.message)
            out_data = self.build_system_error_data("unhandled exception",
                                                    -4, e.message)
        finally:
            print out_data
        reply_to = self._get_reply_to(msg)
        if reply_to:
            msg_out = self._put_engine_data(out_data, reply_to)
            self.send(msg_out)
        else:
            self._report_problem(out_data)

    def _configure_engine(self, engine_input_data):
        output_data = self._engine_object.configure(engine_input_data)
        if not output_data:
            output_data = EngineData()
        if output_data.get_data():
            output_data.set_data(Mimetype.STRING, "done")
        return output_data

    def _execute_engine(self, engine_input_data):
        # TODO: Start time function
        # start_clock = ?
        out_data = self._engine_object.execute(engine_input_data)
        # TODO: Stop time function
        # stop_clock = ?
        if not out_data:
            self._logger.log_exception("null engine result")
            raise Exception("null engine result")

        # TODO: Check if get data is null or none
        return out_data

    @staticmethod
    def _get_reply_to(message):
        reply = message.get_metadata().replyTo
        reply_to = reply if reply else None
        return reply_to

    def _get_engine_data(self, msg):
        return self.de_serialize(msg,
                                 self._engine_object.get_input_data_types())

    def _get_links(self, engine_input_data, engine_output_data):
        owner_ss = ServiceState(engine_output_data.engine_name(),
                                engine_output_data.state)
        input_ss = ServiceState(engine_input_data.engine_name(),
                                engine_input_data.state)
        return self._compiler.get_links(owner_ss, input_ss)

    def _update_metadata(self, in_meta, out_meta):
        out_meta.author = self.myname
        out_meta.version = self._engine_object.get_version()

        if not out_meta.communicationId:
            out_meta.communicationId = in_meta.communicationId

        out_meta.composition = in_meta.composition
        out_meta.executionTime = self.execution_time
        out_meta.action = in_meta.action

    def _parse_composition(self, engine_input_data):
        current_composition = engine_input_data.get_composition()
        if current_composition == self._prev_composition:
            self._compiler.compile(current_composition)
            self._prev_composition = current_composition

    def _put_engine_data(self, data, receiver):
        topic = xMsgTopic.wrap(receiver)
        return self.serialize(topic, data,
                              self._engine_object.get_output_datatypes())

    def _report_problem(self, engine_data):
        status = engine_data.status
        if status == EngineStatus.ERROR:
            self._report(xMsgConstants.ERROR, engine_data)
        elif status == EngineStatus.WARNING:
            self._report(xMsgConstants.WARNING, engine_data)

    def _report(self, topic_prefix, engine_data):
        topic = xMsgTopic.wrap(topic_prefix + ":" + self.myname)
        msg = self.serialize(topic,
                             engine_data,
                             self._engine_object.get_output_datatypes())
        self.send_frontend(msg)

    def execute(self, msg):
        out_data = None
        try:
            in_data = self._get_engine_data(msg)
            out_data = self._execute_engine(in_data)

        except Exception as e:
            self._logger.log_exception(e.message)
            out_data = self.build_system_error_data("unhandled exception",
                                                    -4, e.message)
        finally:
            self._update_metadata(msg.metadata, out_data.metadata)

    def try_acquire_semaphore(self):
        return self._semaphore.acquire(blocking=False)

    def release_semaphore(self):
        return self._semaphore.release()
