from abc import ABC, abstractmethod
from covid19 import tasks_qa_dir
from os import path


class Tasks(ABC):
    def __init__(self, tasks_dir):
        self.tasks_dir = tasks_dir
        self.tasks = list()
        self.total_tasks = ''
        self.cur_task = ''
        self.cur_task_num = None
        self.cur_sub_tasks = list()

    @abstractmethod
    def load_task(self, task_num):
        pass

    @abstractmethod
    def task_info(self):
        pass

    @abstractmethod
    def load_tasks_file_names(self):
        pass

    @abstractmethod
    def get_current_task(self):
        pass

    @abstractmethod
    def get_sub_tasks(self):
        pass
