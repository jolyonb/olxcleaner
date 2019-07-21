"""
parsing_exceptions.py

Contains exception definitions for global course parsing
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class MissingURLName(CourseError):
    """A tag is missing the `url_name` attribute. edX will provide a garbage 32-character name for you, but everything is cleaner if you provide a nice name yourself."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag, describing the tag name
        """
        super().__init__(filename)
        self._description = f"A <{kwargs['tag']}> tag has no url_name"

class DuplicateURLName(CourseError):
    """Two tags have the same `url_name` attribute. This can lead to the wrong content loading."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - url_name
        - tag1
        - file1
        - tag2
        - file2
        """
        super().__init__(filename)
        self._description = (f"Duplicate url_name found: '{kwargs['url_name']}' appears as <{kwargs['tag1']}> in "
                             f"{kwargs['file1']} and also as <{kwargs['tag2']}> in {kwargs['file2']}")

class MissingDisplayName(CourseError):
    """A tag is missing the `display_name` attribute. edX will fill a generic name for you."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - edxobj, the object that is missing the display name
        """
        super().__init__(filename)
        edxobj = kwargs['edxobj']
        if 'url_name' in edxobj.attributes:
            self._description = f"The tag {edxobj} is missing the display_name attribute"
        else:
            self._description = f"A <{edxobj.type}> tag with no url_name is missing the display_name attribute"

class BadPolicyFormat(CourseError):
    """The policy file didn't have the expected structure."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The policy file is not a dictionary of values"

class ObjectNotFound(CourseError):
    """The policy file references an object that doesn't exist."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The policy file refers to <{kwargs['objtype']} url_name='{kwargs['url_name']}'> which does not exist in the course structure"

class WrongObjectType(CourseError):
    """The policy file references an object of one type, but that object is found in the course with another type."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The policy file refers to a <{kwargs['objtype']}> tag with url_name '{kwargs['url_name']}'. However, that url_name points to a <{kwargs['objtypefound']}> tag."

class BadEntry(CourseError):
    """The policy file contains an entry that is not a dictionary."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The policy file entry for <{kwargs['objtype']} url_name='{kwargs['url_name']}'> is not a dictionary"

class SettingOverride(CourseError):
    """The policy file is overriding a setting specified in a file."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The policy file entry for <{kwargs['objtype']} url_name='{kwargs['url_name']}'> is overriding the setting for '{kwargs['setting']}'"

class GradingPolicyIssue(CourseError):
    """A catch-all error for issues in the grading policy."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = kwargs['msg']
