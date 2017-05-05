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

    def run(self):
        raise NotImplementedError("Override me")


class DeployList(Deploy):
    operations = []
    home = default_home

    def __init__(self, propagate_home=False):
        super(DeployList, self).__init__(self.home)
        self.propagate_home = propagate_home

    def run(self):
        for op in self.operations:
            old_home = None

            if self.propagate_home:
                old_home = op.home

            op.run()

            if self.propagate_home:
                op.home = old_home
