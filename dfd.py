#!/usr/bin/env python3
import argparse

import os

def copy_folder(name, home, base):
    pass


def git_clone_oh_my_zsh(home):
    pass


def git_clone_zsh_autoenv(home):
    pass


def get_clone_bullet


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy dotfiles into home folder")
    parser.add_argument("-m",
                        "--home",
                        dest="home",
                        type=str,
                        help="Home folder (default: current user home)",
                        default=os.path.expanduser("~"))
    parser.add_argument("-s",
                        "--src",
                        dest="src",
                        type=str,
                        help="Source folder for dotfiles (default: current folder)",
                        default=os.getcwd())
    parser.add_argument("-e",
                        "--environment",
                        dest=envs,
                        type=str,
                        nargs="*",
                        help="Environments (subfolders) to load")
    parser.add_argument("-n",
                        "--no-default",
                        dest="default",
                        action="store_false"
                        )


