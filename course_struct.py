import os
from enum import auto
import configparser

import utils

class Course:
    _modules = []
    path = ""
    id = -1

    def __init__(self, path):
        self.path = path
        utils.parse_json_props(self)
        self._modules = [Module(module_path) for module_path in utils.get_dirs(path)]

    def modules(self):
        return self._modules


class Module:
    _lessons = []
    path = ""
    parent_id = -1
    id = -1
    position = -1

    def __init__(self, path):
        self.path = path
        utils.parse_json_props(self)
        self._lessons = [Lesson(item_path) for item_path in utils.get_dirs(path)]

    def lessons(self):
        return self._lessons


class Lesson:
    _tasks = []
    path = ""
    id = None
    parent_id = None
    position = -1

    def __init__(self, path):
        self.path = path
        utils.parse_json_props(self)
        self._tasks = [Task(item_path) for item_path in utils.get_dirs(path)]

    def tasks(self):
        return self._tasks


class taskTypes:
    Program = auto()
    Text = auto()
    Test = auto()


PROGRAM_TEST_DIR = "tests"
PROGRAM_SOLUTION_DIR = "solution"
PROGRAM_TEMPLATE_DIR = "template"


class Task:
    """
    Class for task info
    """
    path = ""
    taskType = None
    id = None
    parent_id = None
    position = -1

    def __init__(self, path):
        self.path = path
        utils.parse_json_props(self)
        self.taskType = taskTypes.Program
