import os
from enum import Enum

default_home = os.path.expanduser("~")


class ExistsPolicy(Enum):
    FAIL = "fail"
    MERGE = "merge"
    REMOVE = "remove"


class Deploy:
    def __init__(self, home=default_home):
        self.home = home

    def log(self):
        print("Override log() please.")

    def run(self):
        raise NotImplementedError("Implement me")


class DeployList(Deploy):
    operations = []
    home = default_home
    propagate_home = False

    def __init__(self):
        super(DeployList, self).__init__(self.home)

    def get_operations(self):
        return self.operations

    def log(self):
        return

    def run(self):
        for op in self.get_operations():
            old_home = None

            if self.propagate_home:
                old_home = op.home
                op.home = self.home
            op.log()
            op.run()

            if self.propagate_home:
                op.home = old_home
