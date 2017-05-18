import os

from configs.util import from_data
from operations.base import DeployList
from operations.combine_files import GenerateGitConfigFromChunks, GenerateHgRcFromChunks
from operations.directory import DeployDirectory, DeployDirectoryIfExists
from operations.git import DeployGitRepo, DeployFilesFromGitRepo


class Operation(DeployList):
    operations = [
        DeployGitRepo(
            repo="https://github.com/robbyrussell/oh-my-zsh.git",
            dst=".oh-my-zsh",
        ),
        DeployFilesFromGitRepo(
            repo="https://github.com/gagarski/bullet-train-oh-my-zsh-theme.git",
            checkout="my-version",
            dst=".oh-my-zsh/custom",
            file_list=("bullet-train.zsh-theme",)
        ),
        DeployDirectory(from_data("main")),
        DeployDirectory(from_data("work")),
        DeployDirectory(from_data("linux")),
        DeployDirectory(from_data("polyana")),
        DeployDirectoryIfExists(from_data("private")),
        GenerateGitConfigFromChunks(),
        GenerateHgRcFromChunks()
    ]