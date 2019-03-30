"""
parsing_exceptions.py

Contains exception definitions for global course parsing
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class MissingURLName(CourseError):
    """A tag has no url_name"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING

class DuplicateURLName(CourseError):
    """Multiple tags have the same url_name"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class MissingDisplayName(CourseError):
    """A tag has no display_name attribute when one is suggested"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING
