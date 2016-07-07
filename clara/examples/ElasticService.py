# coding=utf-8
from datetime import datetime

import numpy as np
from elasticsearch import Elasticsearch

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType


class ElasticService(Engine):
    def __init__(self):
        super(ElasticService, self).__init__()
        self.es_client = Elasticsearch()
        self.count = 0

    def configure(self, engine_data):
        pass

    def execute(self, engine_data):
        timestamp = datetime.now()
        doc = {
            'author': engine_data.engine_name(),
            'result': np.random.uniform(1,111),
            'timestamp': timestamp,
        }
        self.count += 1
        self.es_client.index(index="services", doc_type='service_results',
                             id=self.count, body=doc)
        return engine_data

    def execute_group(self, data_array):
        pass

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def get_states(self):
        pass

    def get_description(self):
        return "Data creator for simulating histograms"

    def get_version(self):
        return "v1.0"

    def get_author(self):
        return "royarzun"

    def reset(self):
        pass

    def destroy(self):
        pass
