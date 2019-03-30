# -*- coding: utf-8 -*-
"""
exceptions.py

Contains base classes and supporting structures for describing errors
"""
from enum import Enum

class ErrorLevel(Enum):
    """Levels of errors"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

class CourseError(object):
    """Abstract class describing an error"""
    def __init__(self, filename=None, message=None):
        """
        Initializing an error requires three pieces:
        * Set the error level
        * Store the relevant filename
        * Construct the error message
        """
        self._filename = filename
        self._description = message
        self._level = ErrorLevel.DEBUG

    @property
    def filename(self):
        return self._filename

    @property
    def description(self):
        return self._description

    @property
    def level(self):
        return self._level.name

    @property
    def level_val(self):
        return self._level.value

    @property
    def name(self):
        return type(self).__name__
