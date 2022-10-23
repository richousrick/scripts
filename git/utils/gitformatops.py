import re
from typing import Tuple

from gitutils import run_git_func, get_git_username, get_branch_name


# Utility methods for custom branch and commit name formatting.
# These are extracted to their own file to make changing the formatting easier due to being in a centralised location.

def format_branch_name(tag: str, description: str) -> str | None:
    """
    Creates a formatted branch name from the given tag and description.
    :param tag: Unique identifier for a group of related branches. e.g. JIRA ticket number
    :param description: Description of the purpose of the branch.
                        This provides the ability for multiple related branches to be grouped together.
    :return: The formatted branch name, or None, if a valid branch name was not possible from the given information.
    """
    username = get_git_username()
    branch_name = tag+"/"+username+"/"+description
    stdout, stderr, code = run_git_func("git check-ref-format --branch " + branch_name, check=False)
    if code != 0 or stderr or stdout != branch_name:
        return None
    else:
        return branch_name


def extract_branch_tag(branch_name: str) -> Tuple[str, bool] | None:
    """
    Attempts to extract metadata from a branch name
    :param branch_name: branch name to attempt to extract data from
    :return: (branch tag, is my branch) or None.
    """
    match = re.fullmatch("^([\\w-]+)/([^/]+)/.+$", branch_name)
    if match and len(match.groups()) == 2:
        username = get_git_username()
        return match.group(1), match.group(2) == username
    else:
        return None


def format_commit_title(commit_type: str, description: str, fallback_tag: str = "NOJIRA") -> str:
    """
    Attempts to generate a
    :param commit_type:
    :param description:
    :param fallback_tag:
    :return:
    """
    current_branch = get_branch_name()
    if current_branch:
        try:
            tag, _ = extract_branch_tag(current_branch)
        except TypeError:
            tag = fallback_tag
    else:
        tag = fallback_tag
    return tag + ":" + commit_type + ": " + description


