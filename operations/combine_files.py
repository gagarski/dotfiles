import os

from operations.base import Deploy, default_home, ExistsPolicy


class GenerateGitConfigFromChunks(Deploy):
    def __init__(self, home=default_home,
                 exists_policy=ExistsPolicy.REMOVE,
                 dst=".gitconfig",
                 src=".gitconfig.d"):
        super(GenerateGitConfigFromChunks, self).__init__(home)
        self.exists_policy = exists_policy
        self.dst = dst
        self.src = src

    def log(self):
        print("=" * 80)
        print(f"Generating {self.dst} at {self.home} from {self.src}")
        print(f"Policy is {self.exists_policy}.")
        print("=" * 80)

    def run(self):
        src_path = os.path.join(self.home, self.src)
        dst_path = os.path.join(self.home, self.dst)
        if self.exists_policy == ExistsPolicy.MERGE:
            raise ValueError("{} is not applcable here".format(self.exists_policy))
        elif self.exists_policy == ExistsPolicy.REMOVE and os.path.exists(dst_path):
            os.remove(dst_path)
        elif os.path.exists(dst_path):
            raise FileExistsError("{} already exists".format(dst_path))

        with open(dst_path, "w") as gitconfig:
            print("[include]", file=gitconfig)
            ls = os.listdir(src_path)
            ls.sort()
            for f in ls:
                home = "~" if self.home == default_home else self.home
                chunk_path = os.path.join(home, self.src, f)
                print("\tpath = {}".format(chunk_path), file=gitconfig)


class GenerateHgRcFromChunks(Deploy):
    def __init__(self, home=default_home,
                 exists_policy=ExistsPolicy.REMOVE,
                 dst=".hgrc",
                 src=".hgrc.d"):
        super(GenerateHgRcFromChunks, self).__init__(home)
        self.exists_policy = exists_policy
        self.dst = dst
        self.src = src

    def log(self):
        print("=" * 80)
        print(f"Generating {self.dst} at {self.home} from {self.src}")
        print(f"Policy is {self.exists_policy}.")
        print("=" * 80)

    def run(self):
        src_path = os.path.join(self.home, self.src)
        dst_path = os.path.join(self.home, self.dst)
        if self.exists_policy == ExistsPolicy.MERGE:
            raise ValueError("{} is not applcable here".format(self.exists_policy))
        elif self.exists_policy == ExistsPolicy.REMOVE and os.path.exists(dst_path):
            os.remove(dst_path)
        elif os.path.exists(dst_path):
            raise FileExistsError("{} already exists".format(dst_path))

        with open(dst_path, "w") as gitconfig:
            ls = os.listdir(src_path)
            ls.sort()
            for f in ls:
                home = "~" if self.home == default_home else self.home
                chunk_path = os.path.join(home, self.src, f)
                print("%include {}".format(chunk_path), file=gitconfig)
