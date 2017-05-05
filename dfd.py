#!/usr/bin/env python3
import os

from operations import DeployGitRepo
from operations.combine_files import GenerateGitConfigFromChunks, GenerateHgRcFromChunks
from operations.directory import DeployDirectory
from operations.git import DeployFilesFromGitRepo

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/test")

if __name__ == "__main__":
    # DeployGitRepo(repo="git@github.com:gagarski/bullet-train-oh-my-zsh-theme.git",
    #               dst="tmp/shittyshit").run()
    # DeployDirectory(BASE_DIR, file_list=("test/sss/*.html",)).run()
    # DeployFilesFromGitRepo(repo="https://github.com/gagarski/bullet-train-oh-my-zsh-theme.git",
    #                        dst="tmp/shittyshit",
    #                        file_list=("bullet-train.zsh-theme",)
    #                        ).run()
    GenerateGitConfigFromChunks(dst="fake_git_config").run()
    GenerateHgRcFromChunks(dst="fake_hg_rc").run()
