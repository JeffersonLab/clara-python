# coding=utf-8

import sys
import time
from threading import Semaphore

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.engine.EngineData import EngineData
from clara.engine.EngineDataType import Mimetype
from clara.engine.EngineStatus import EngineStatus
from clara.sys.ccc.CCompiler import CCompiler
from clara.sys.ccc.ServiceState import ServiceState
from clara.util.CConstants import CConstants
from clara.util.ClaraLogger import ClaraLogger


class ServiceEngine(ClaraBase):

    def __init__(self, name, local_address, frontend_address, user_engine,
                 service_sys_configuration, service_report):
        super(ServiceEngine, self).__init__(name,
                                            local_address.host,
                                            local_address.pub_port,
                                            frontend_address.host,
                                            frontend_address.pub_port)
        self._engine_object = user_engine
        self._semaphore = Semaphore(1)
        self.sys_config = service_sys_configuration
        self._compiler = CCompiler(self.myname)
        self._prev_composition = "undefined"
        self._report = service_report
        self._logger = ClaraLogger(repr(self))
        self.execution_time = 0

    def configure(self, message):
        """Sends configuration message to the Engine

        Args:
            message (xMsgMessage): message containing engine configuration data
        """
        input_data = None
        outgoing_data = None

        try:
            input_data = self._get_engine_data(message)
            outgoing_data = self._configure_engine(input_data)

        except Exception as e:
            self._logger.log_exception(e.message)
            outgoing_data = self.build_system_error_data(message,
                                                         -4, e.message)
        finally:
            self._update_metadata(input_data.metadata, outgoing_data.metadata)

        reply_to = self._get_reply_to(message)
        if reply_to:
            outgoing_message = self._put_engine_data(outgoing_data, reply_to)
            self.send(outgoing_message)
        else:
            self._report_problem(outgoing_data)

    def _configure_engine(self, engine_input_data):
        output_data = self._engine_object.configure(engine_input_data)
        if not output_data:
            output_data = EngineData()
        if output_data.get_data():
            output_data.set_data(Mimetype.STRING, "done")
        return output_data

    @staticmethod
    def _get_reply_to(message):
        reply = message.metadata.replyTo
        reply_to = reply if reply and reply != "undefined" else None
        return reply_to

    def _get_engine_data(self, message):
        msg = self.de_serialize(message,
                                self._engine_object.get_input_data_types())
        self._report.increment_bytes_received(sys.getsizeof(msg))
        return msg

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
        current_composition = engine_input_data.composition
        if current_composition != self._prev_composition:
            self._compiler.compile(current_composition)
            self._prev_composition = current_composition

    def _put_engine_data(self, data, receiver):
        topic = ClaraUtils.build_topic(CConstants.SERVICE, receiver)
        msg = self.serialize(topic, data,
                             self._engine_object.get_output_data_types())
        self._report.increment_bytes_sent(sys.getsizeof(msg))
        return msg

    def _report_problem(self, engine_data):
        status = engine_data.status
        if status == EngineStatus.ERROR:
            self._report(xMsgConstants.ERROR, engine_data)
        elif status == EngineStatus.WARNING:
            self._report(xMsgConstants.WARNING, engine_data)

    def _report(self, topic_prefix, engine_data):
        topic = xMsgTopic.wrap(str(topic_prefix) + ":" + self.myname)
        msg = self.serialize(topic, engine_data,
                             self._engine_object.get_output_data_types())
        self.send_frontend(msg)

    def _report_data(self, data):
        self._report(xMsgConstants.DATA, data)

    def _report_done(self, data):
        self._report(xMsgConstants.DONE, data)

    def _send_reports(self, outgoing_data):
        if self.sys_config.data_request:
            self._report_data(outgoing_data)
            self.sys_config.reset_data_request_count()
        if self.sys_config.done_request:
            self._report_done(outgoing_data)
            self.sys_config.reset_done_request_count()

    def _send_response(self, outgoing_data, outgoing_links):
        for link in outgoing_links:
            msg = self._put_engine_data(outgoing_data, link)
            self.send(msg)

    def execute(self, message):
        """Executes the engine with the given input data

        Args:
            message (xMsgMessage): message containing input data
        """
        in_data = None
        outgoing_data = None
        self.sys_config.add_request()
        self._report.increment_request_count()

        try:
            in_data = self._get_engine_data(message)
            self._parse_composition(in_data)
            start_time = time.time()
            outgoing_data = self._execute_engine(in_data)
            elapsed_time = time.time() - start_time
            self._report.increment_execution_time(elapsed_time)

        except Exception as e:
            self._logger.log_exception(e.message)
            self._report.increment_failure_count()
            outgoing_data = self.build_system_error_data(message, -4,
                                                         e.message)
            raise e
        finally:
            self._update_metadata(message.metadata, outgoing_data.metadata)

        reply_to = self._get_reply_to(message)
        if reply_to and reply_to != "undefined":
            outgoing_message = self._put_engine_data(outgoing_data, reply_to)
            self.send(outgoing_message)

        self._send_reports(outgoing_data)
        self._report_problem(outgoing_data)
        self._send_response(outgoing_data, self._get_links(in_data,
                                                           outgoing_data))

    def _execute_engine(self, engine_input_data):
        out_data = self._engine_object.execute(engine_input_data)
        if not out_data:
            self._logger.log_exception("null engine result")
            raise Exception("null engine result")

        return out_data

    def try_acquire_semaphore(self):
        """Returns true if service semaphore is available in a non blocking op

        Returns:
            boolean
        """
        return self._semaphore.acquire(blocking=False)

    def release_semaphore(self):
        """Releases engine semaphore

        Returns:
            boolean
        """
        return self._semaphore.release()
