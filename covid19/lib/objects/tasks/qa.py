from covid19.lib.objects.tasks.tasks import Tasks
from covid19 import tasks_qa_dir
from os import listdir
from os.path import isfile, join, splitext
import yaml


class QATask(Tasks):
    def __init__(self, tasks_dir=tasks_qa_dir):
        super().__init__(tasks_dir=tasks_dir)
        self.tasks = self.load_tasks_file_names(tasks_dir=self.tasks_dir)
        self.total_tasks = len(self.tasks)

    def load_tasks_file_names(self, tasks_dir = tasks_qa_dir, strip_file_extension=True):
        file_names = [fp for fp in listdir(tasks_dir) if isfile(join(tasks_dir, fp))]
        if strip_file_extension:
            return [splitext(f_name)[0] for f_name in file_names]
        else:
            return file_names

    def get_tasks(self, numbers=True):
        if numbers:
            return [task[len(task):] for task in self.tasks]
        return self.tasks

    def load_task(self, task_num):
        if not isinstance(task_num, int):
            raise TypeError("kw_arg: 'task_num' should be of type 'int' ")

        if task_num < 0:
            raise ValueError("'task_num' parameter should be a positive integer")

        task = 'task' + str(task_num)
        if task not in self.tasks:
            raise FileNotFoundError('{} not found in {}'.format(task, self.tasks_dir))

        with open(file=join(self.tasks_dir, task + '.yml')) as f:
            task_details = yaml.load(f, yaml.Loader)

        self.cur_task = task_details['title']
        self.cur_task_num = task_num
        self.cur_sub_tasks = task_details['sub_tasks']

    def get_current_task(self):
        return 'task' + str(self.cur_task_num) + ' : ' + self.cur_task

    def get_current_task_title(self):
        return self.cur_task

    def get_sub_tasks(self):
        return self.cur_sub_tasks

    def get_total_tasks(self):
        return self.total_tasks

    def sub_tasks_to_dict(self):
        sub_tasks_dict = dict()
        for index, sub_task in enumerate(self.cur_sub_tasks):
            sub_tasks_dict[index] = sub_task
        return sub_tasks_dict

    def task_info(self):
        return {
            'task' + str(self.cur_task_num): {
                'title': self.get_current_task_title(),
                'sub_tasks': self.get_sub_tasks()
            }
        }

