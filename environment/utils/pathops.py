import os
from typing import List, Callable
import re


# A collection of methods for reading and checking the environment path


def get_path_from_env() -> str:
    """Gets the environment path as a string."""
    return os.getenv("PATH")


def get_paths() -> List[str]:
    """Returns a list of all path segments in the environment."""
    return get_path_from_env().split(":")


def has_path(matcher: Callable[[str], bool], paths: List[str] = None) -> bool:
    """
    Checks if the environment path contains a given match.

    :param matcher: Method to evaluate each path
    :param paths: The paths to check, defaults to using those from the environment.
    :return: True, if the matcher returns true on any of the paths.
    """
    if paths is None:
        paths = get_paths()
    return any(matcher(path) for path in paths)


def has_path_explicit(target: str, paths: List[str] = None) -> bool:
    """
    Checks if the environment path contains a given string.

    :param target: The path to search for.
    :param paths: The paths to check, defaults to using those from the environment.
    :return: True, if any of the paths equals the target path.
    """
    return has_path(lambda path: target == path, paths)


def has_path_reg(reg: str, paths: List[str] = None) -> bool:
    """
    Checks if the environment path contains an entry matching a given regex string.

    :param reg: regex string to search for. Note: complete matches only
    :param paths: The paths to check, defaults to using those from the environment.
    :return: True, if any of paths completely matches the target regex.
    """
    return has_path(lambda path: bool(re.fullmatch(reg, path)), paths)


def get_path_matching(matcher: Callable[[str], bool], paths: List[str] = None) -> str | None:
    """
    Searches for a path in the environment that matches a given filter.

    :param matcher: Method to evaluate each path
    :param paths: The paths to check, defaults to using those from the environment.
    :return: The first path segment that the matcher returns true for. Or None if no matches were found.
    """
    if paths is None:
        paths = get_paths()
    return next(filter(matcher, paths), None)


def find_path(reg: str, paths: List[str] = None) -> str | None:
    """
    Searches for a path in the environment that matches a given regex string.

    :param reg: regex string to search for. Note: complete matches only
    :param paths: The paths to check, defaults to using those from the environment.
    :return: The first path that completely matches the given regex string. Or None, if no matches were found.
    """
    return get_path_matching(lambda path: bool(re.fullmatch(reg, path)), paths)
