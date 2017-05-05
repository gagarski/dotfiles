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
