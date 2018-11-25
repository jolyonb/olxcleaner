# -*- coding: utf-8 -*-
"""
errorstore.py

Structures to accumulate and track errors in a course
"""

class ErrorStore(object):
    """Class to store all errors in an import"""

    def __init__(self):
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)
