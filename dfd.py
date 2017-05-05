#!/usr/bin/env python3
import os

import importlib.util

import sys

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/test")


def run_from_file(path):
    spec = importlib.util.spec_from_file_location("deployment_op", path)
    op_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(op_mod)
    op_mod.Operation().run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage {sys.argv[0]} path/to/config.py")
        sys.exit(1)

    run_from_file(sys.argv[1])

