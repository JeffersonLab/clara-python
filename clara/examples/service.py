# coding=utf-8

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype


class Engine1(Engine):
    def __init__(self):
        super(Engine1, self).__init__()

    def configure(self, engine_data):
        print "Engine1 received instruction configure itself"

    def execute(self, engine_data):
        print "Engine1 received <%s>" % engine_data.get_data()
        return engine_data

    def execute_group(self, data_array):
        print "Engine1 received multiple data"
        for data in data_array:
            print "Engine1 received <%s> from : %s" % (data.mimetype,
                                                       data.metadata.sender)
        return data_array

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_states(self):
        pass

    def get_description(self):
        return "Some engine1 description"

    def get_version(self):
        return "v1.0"

    def get_author(self):
        return "royarzun"

    def reset(self):
        pass

    def destroy(self):
        pass


class Engine2(Engine):

    def __init__(self):
        super(Engine2, self).__init__()

    def configure(self, engine_data):
        print "Engine2 received instruction configure itself"

    def execute(self, engine_data):
        print "Engine2 : " + str(engine_data.get_data())
        return_str = str(engine_data.get_data()) + ">>THIS WAS ADDED<<"
        print "Engine2 returns : " + return_str
        engine_data.set_data(Mimetype.STRING, return_str)
        return engine_data

    def execute_group(self, data_array):
        print "Engine2 received multiple data"
        for data in data_array:
            print "Engine2 received <%s> from : %s" % (data.mimetype,
                                                       data.metadata.sender)
        return data_array

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_states(self):
        pass

    def get_description(self):
        return "Some engine2 description"

    def get_version(self):
        return "v1.1"

    def get_author(self):
        return "royarzun"

    def reset(self):
        pass

    def destroy(self):
        pass
