import os
from abc import abstractmethod
from enum import auto

from watchdog.utils.dirsnapshot import DirectorySnapshotDiff, DirectorySnapshot

import utils
from api import ApiAdapter


class Syncable:
    def __init__(self, path, api: ApiAdapter):
        pushed_snapshot_path   = os.path.join(path, os.path.join(".course_git", "pushed_snapshot.pkl"))
        commited_snapshot_path = os.path.join(path, os.path.join(".course_git", "commited_snapshot.pkl"))

        if not os.path.exists(".course_git"):
            raise Exception("There is no repository in this directory")
        if not os.path.exists(pushed_snapshot_path) or not os.path.exists(commited_snapshot_path):
            raise Exception("Invalid sync directory")

        self.pushed_snapshot = utils.load_object(pushed_snapshot_path)
        self.commited_snapshot = utils.load_object(commited_snapshot_path)


    def push(self):
        diff = DirectorySnapshotDiff(self.pushed_snapshot, self.commited_snapshot)
        for dir in diff.dirs_modified:
            if dir in self.parts():
                self.get_part(dir).push()
        self.push_self()

    def commit(self):
        new_snapshot = DirectorySnapshot(self.path)
        commited_snapshot_path = os.path.join(self.path, os.path.join(".course_git", "commited_snapshot.pkl"))
        self.commited_snapshot = utils.save_object(new_snapshot, commited_snapshot_path)

    @abstractmethod
    def parts(self):
        """
        Return subparts dict : path -> subpart class
        :return:
        """
        pass

    @abstractmethod
    def get_part(self, path):
        """
        Return subpart by it's path
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def push_self(self):
        """
        Push self state
        :return:
        """
        pass


class Course(Syncable):
    _modules = {}
    path = ""
    id = -1

    def __init__(self, path):
        super(Course, self).__init__(path)
        self.path = path
        utils.parse_json_props(self)
        self._modules = {module_path: Module(module_path) for module_path in utils.get_dirs(path)}

    def modules(self):
        return self._modules

    def get_part(self, path):
        return  self._modules[path]

    def parts(self):
        return self.modules()


class Module(Syncable):
    _lessons = {}
    path = ""
    parent_id = -1
    id = -1
    position = -1

    def __init__(self, path):
        super(Module, self).__init__(path)
        self.path = path
        utils.parse_json_props(self)
        self._lessons = {item_path: Lesson(item_path) for item_path in utils.get_dirs(path)}

    def lessons(self):
        return self._lessons

    def get_part(self, path):
        return self._lessons[path]

    def parts(self):
        return self.lessons()

class Lesson(Syncable):
    _tasks = []
    path = ""
    id = None
    parent_id = None
    position = -1

    def __init__(self, path):
        super(Lesson, self).__init__(path)
        self.path = path
        utils.parse_json_props(self)
        self._tasks = {item_path: Task(item_path) for item_path in utils.get_dirs(path)}

    def tasks(self):
        return self._tasks

    def get_part(self, path):
        return self._tasks[path]

    def parts(self):
        return self.tasks()

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

    def push(self):
        print("Pushing task {}".format(self.path))

