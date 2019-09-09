import argparse
import pyinotify
import os
import asyncore

from termcolor import colored

from course_struct import Course, Module, Lesson, Task
from stepik_handlers import TaskHandler, LessonHandler, ModuleHandler, CourseHandler

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='root_path', action="store")


def setup_watchers(course: Course):
    taskwmngr = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(taskwmngr, TaskHandler())

    lessonmngr = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(lessonmngr, LessonHandler())

    modulemngr = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(modulemngr, ModuleHandler())

    coursemngr = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(coursemngr, CourseHandler())

    coursemngr.add_watch(course.path, pyinotify.ALL_EVENTS)
    for module in course.modules():
        modulemngr.add_watch(module.path, pyinotify.ALL_EVENTS)
        for lesson in module.lessons():
            lessonmngr.add_watch(lesson.path, pyinotify.ALL_EVENTS)
            for task in lesson.tasks():
                taskwmngr.add_watch(task.path, pyinotify.ALL_EVENTS, rec=True)


def main():
    args = parser.parse_args()
    root_path = args.root_path

    course = Course(root_path)

    setup_watchers(course)
    asyncore.loop()


main()
# print(colored("Hello ", "blue") + colored("world", "green"))
