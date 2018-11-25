# -*- coding: utf-8 -*-
"""
errors.py

Errors that are checked for
"""
from enum import Enum

class ErrorLevel(Enum):
    """Levels of errors"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

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
    def name(self):
        return type(self).__name__

class CourseXMLDoesNotExist(CourseError):
    """The course.xml file provided does not exist"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.CRITICAL
        self._description = f"The file '{filename}' does not exist."
