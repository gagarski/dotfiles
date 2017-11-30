from configs.util import from_data
from operations.base import DeployList
from operations.combine_files import GenerateGitConfigFromChunks, GenerateHgRcFromChunks
from operations.directory import DeployDirectory, DeployDirectoryIfExists
from operations.vcs.git import DeployGitRepo, DeployFilesFromGitRepo
from operations.vcs.hg import DeployHgRepo


class Operation(DeployList):
    operations = [
        DeployGitRepo(
            repo="https://github.com/robbyrussell/oh-my-zsh.git",
            dst=".oh-my-zsh",
        ),
        DeployGitRepo(
            repo="https://github.com/Tarrasch/zsh-autoenv",
            dst=".dotfiles/lib/zsh-autoenv",
        ),
        DeployHgRepo(
            repo="https://bitbucket.org/sjl/hg-prompt/",
            dst=".hg_ext/hg-prompt"
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
