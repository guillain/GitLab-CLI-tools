import os
import sys
import shutil


class Filing(object):
    def __init__(self, path):
        self.path = path

    def get_folders(self, path):
        return [os.path.join(path, o) for o in os.listdir(path)
                if os.path.isdir(os.path.join(path, o))]

    def create_folder(self, path):
        if not os.path.exists(path):
            return os.makedirs(path)

    def delete_folder(self, path):
        return shutil.rmtree(path, ignore_errors=True)
