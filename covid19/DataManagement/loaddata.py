from covid19 import data_dir_paths
import json
from os import path, fsdecode, listdir


class LoadData:
    """
    providing functions to deal with the given data
    """

    def __init__(self, data_dirs=data_dir_paths):
        for data_dir in data_dirs:
            if not path.isdir(data_dir):
                raise NotADirectoryError("{}".format(data_dir))
        self.data_dir_paths = data_dirs

    def get_datum(self):
        """
        generator function that returns the research paper in json format
        :return:
        """
        for data_dir in self.data_dir_paths:
            # r=root, d=directories, f = files
            for f in listdir(data_dir):
                filename = fsdecode(f)
                if filename.endswith(".json"):
                    file_path = path.join(data_dir, filename)
                    with open(file_path) as json_file:
                        yield json.load(json_file)

    @staticmethod
    def get_research_paper_by_id(uid=None):
        if len(uid) == 0:
            raise ValueError("'uid' should not be valid string")
        for data_dir in data_dir_paths:
            filename = uid + '.json'
            file_path = path.join(data_dir, filename)
            if path.isfile(file_path):
                with open(file_path) as json_file:
                    return json.load(json_file)

        raise FileNotFoundError('{} not found in {}'.format(file_path, data_dir_paths))
