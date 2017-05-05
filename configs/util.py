import os


def from_data(name):
    up = os.path.dirname
    down = os.path.join
    return down(up(up(os.path.abspath(__file__))), "data", name)
