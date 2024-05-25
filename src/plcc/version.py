import subprocess
from pathlib import Path


def get_version():
    try:
        return get_version_from_git_tag()
    except:
        pass

    try:
        return read_version_file()
    except:
        pass

    return "Unknown"


def get_version_from_git_tag():
    completedProcess = subprocess.run([
            'git',
            '--git-dir=' + str(Path(__file__).parent.parent.parent/'.git'),
            'describe',
            '--tags'
        ],
        capture_output=True,
        text=True
        )
    if completedProcess.returncode == 0:
        return completedProcess.stdout.strip()
    raise Nope()


class Nope(Exception):
    pass


def read_version_file():
    with open(Path(__file__).parent/'VERSION') as file:
        return file.read().strip()


if __name__ == '__main__':
    print(get_version())
