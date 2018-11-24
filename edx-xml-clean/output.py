#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output.py

Routines to represent the structure of a course in various ways
"""

def print_tree(course, maxdepth=None):
    """
    Outputs a tree version of the course structure to screen.

    :param course: edXcourse object
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
    _print_tree(course, maxdepth)

def _print_tree(obj, maxdepth, indent=0):
    """
    Recursively outputs a tree version of the course structure to screen.

    :param obj: Current object to display
    :param indent: Current indentation level
    :param maxdepth: The maximum depth to display
    :return: None
    """
    if maxdepth is not None and obj.depth > maxdepth:
        return
    print(f'{" " * indent * 4}{obj}')
    for child in obj.children:
        _print_tree(child, maxdepth, indent + 1)
