"""
policy_exceptions.py

Contains exception definitions for policy file loading
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class NoRunName(CourseError):
    """The course tag has no `url_name`, and hence no run name. This is a required parameter for a course."""
    _level = ErrorLevel.ERROR
    
    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The course tag has no url_name."

class PolicyNotFound(CourseError):
    """The file policy.json was not found."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The file policy.json was not found."
