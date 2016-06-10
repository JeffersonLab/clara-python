# coding=utf-8


class EngineLoader(object):

    def __init__(self, class_name, engine_name):
        self._class_name = class_name
        self._engine_name = engine_name

    def load_engine(self):
        try:
            loaded_module = __import__(self._class_name,
                                       fromlist=[self._engine_name])
            return getattr(loaded_module, self._engine_name)()

        except ImportError as e:
            # do something else here!!!
            raise e
