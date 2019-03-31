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
        self._description = (f"Duplicate url_name found: {kwargs['url_name']} appears as <{kwargs['tag1']}> in "
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
