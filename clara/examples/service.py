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
        # counter for execution
        data = engine_data.get_data() + 1
        engine_data.set_data(Mimetype.SINT32, data)
        return engine_data

    def execute_group(self, data_array):
        pass

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

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


class FactorialEngine(Engine):

    def __init__(self):
        super(FactorialEngine, self).__init__()

    def configure(self, engine_data):
        pass

    @staticmethod
    def _fact(n):
        fact = 0
        for i in range(n):
            if i == 0:
                fact = 1
            else:
                fact *= i
        return fact

    def execute(self, engine_data):
        FactorialEngine._fact(2000)
        return engine_data

    def execute_group(self, data_array):
        pass

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

    def get_states(self):
        pass

    def get_description(self):
        return "Calculates a big factorial!!!"

    def get_version(self):
        return "v1.1"

    def get_author(self):
        return "royarzun"

    def reset(self):
        pass

    def destroy(self):
        pass
