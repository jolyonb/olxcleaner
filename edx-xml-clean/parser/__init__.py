# -*- coding: utf-8 -*-
"""
parser submodule

Handles error sleuthing after course load
"""
from parser.parser import find_url_names, find_display_names

def scan_course(course, errorstore):
    """
    Performs a complete scan of a loaded course.

    :param course: EdxCourse object loaded with content
    :param errorstore: ErrorStore object for error reporting
    :return: None
    """
    # Step 1: Construct a dictionary of url_names
    url_names = find_url_names(course, errorstore)

    # Step 2: Look for missing display_name attributes
    find_display_names(course, errorstore)
