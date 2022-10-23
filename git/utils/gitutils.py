import subprocess
from typing import Tuple
import re


# Gets the name of the current branch
def run_git_func(func: str, check: bool = True) -> Tuple[str, str, int]:
    """
    Runs a shell command and returns its output
    :param func: bash command to run
    :param check: If this should throw when receiving non 0 exit codes.
    :return: the output of the command in form (stdout, stderr, exit code)
    :exception: CalledProcessError if check is enabled, and the command returned a non 0 exit code
    """
    res = subprocess.run([func], shell=True, check=check, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def validated_run_git_func(func: str) -> str:
    """
    Runs a shell command, and returns its output if it was successful.
    This will raise an exception if it encounters any output to stderr
    :param func: command to run
    :return: the output of the command if it completed with exitcode 0 and did not print to stderr
    """
    stdin, stderr, _ = run_git_func(func)
    if stderr:
        raise AssertionError("Unexpected output to stdout '" + stderr + "'")
    else:
        return stdin


def is_in_git() -> bool:
    """
    Checks that we are in a git repo
    :return: true if in a git repo
    """
    return validated_run_git_func("git rev-parse --is-inside-work-tree") == "true"


def get_branch_name() -> str | None:
    if not is_in_git():
        return None
    else:
        branches = validated_run_git_func("git branch --list").split("\n")
        current_branch = next(branch for branch in branches if branch.startswith("*"))
        if not current_branch:
            return None
        else:
            current_branch = current_branch[1:].strip()
            if " " not in current_branch:
                return current_branch
            else:
                match = re.search("^\\(no branch, rebasing (.+)\\)$", current_branch)
                return match.group(1)




