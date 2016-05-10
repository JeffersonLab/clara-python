# coding=utf-8

from enum import Enum


class ClaraLang(Enum):
    JAVA = "java"
    PYTHON = "python"
    CPP = "cpp"

    def __init__(self, lang_value):
        self.lang_value = lang_value

    def __str__(self):
        return self.lang_value
