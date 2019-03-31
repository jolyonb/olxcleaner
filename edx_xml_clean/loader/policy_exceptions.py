"""
policy_exceptions.py

Contains exception definitions for policy file loading
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class NoRunName(CourseError):
    """The course object has no url_name and hence no run name"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR
        self._description = f"The course tag has no url_name"

class PolicyNotFound(CourseError):
    """A policy file was not found"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR
