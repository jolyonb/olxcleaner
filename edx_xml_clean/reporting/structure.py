# -*- coding: utf-8 -*-
"""
structure.py

Routines to represent the structure of a course
"""

def write_tree(course, filename, maxdepth=None):
    """
    Outputs a tree version of the course structure to file.

    :param course: EdxCourse object
    :param filename: File to output to
    :param maxdepth: Maximum depth to display:
        0 = course
        1 = chapter
        2 = sequential
        3 = vertical
        4 = content
        Note that conditionals and AB tests are treated as living
        in-between the integers here.
    :return: None
    """
    with open(filename, "w") as f:
        _write_tree(course, f, maxdepth)

def _write_tree(obj, handle, maxdepth, indent=0):
    """
    Recursively writes a tree version of the course structure to the file handle.

    :param obj: Current object to display
    :param handle: File handle to output to
    :param maxdepth: The maximum depth to display
    :param indent: Current indentation level
    :return: None
    """
    if maxdepth is not None and obj.depth > maxdepth:
        return
    handle.write(f'{" " * indent * 4}{obj}\n')
    for child in obj.children:
        _write_tree(child, handle, maxdepth, indent + 1)
