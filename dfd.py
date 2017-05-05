#!/usr/bin/env python3

import importlib.util

import sys


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

