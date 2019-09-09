import pyinotify


class TaskHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Created something in task", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Modifyed something in task", event.pathname)


class LessonHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Task created", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Task modifyed", event.pathname)


class ModuleHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Lesson created", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Lesson modifyed", event.pathname)


class CourseHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Module created", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Module modifyed", event.pathname)
