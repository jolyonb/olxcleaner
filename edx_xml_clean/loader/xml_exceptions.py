"""
xml_exceptions.py

Contains exception definitions for XML loading
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class CourseXMLDoesNotExist(CourseError):
    """The course.xml file provided does not exist"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR
        self._description = f"The file '{filename}' does not exist."

class InvalidXML(CourseError):
    """The specified XML file has a syntax error"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class InvalidHTML(CourseError):
    """The specified HTML file has a syntax error"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class CourseXMLName(CourseError):
    """The course file is not named course.xml"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING
        self._description = f"The course file, {filename}, is not named course.xml"

class TagMismatch(CourseError):
    """A pointer tag points to a file that opens with a different tag"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class EmptyTag(CourseError):
    """A tag is unexpectedly empty"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING

class ExtraURLName(CourseError):
    """The target of a pointer tag has a url_name of its own"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class InvalidPointer(CourseError):
    """A tag appears to be an invalid pointer tag"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class FileDoesNotExist(CourseError):
    """A tag points to a nonexistent file"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class SelfPointer(CourseError):
    """A tag appears to be pointing to itself"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class UnexpectedTag(CourseError):
    """An unexpected tag has been used"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class PossiblePointer(CourseError):
    """A non-pointer tag has a file that it could point to"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING

class UnexpectedContent(CourseError):
    """A tag that shouldn't contain text does for some reason"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.ERROR

class NonFlatURLName(CourseError):
    """A URL name is not flat; i.e., it contains a : to indicate subdirectories"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING

class NonFlatFilename(CourseError):
    """A filename pointer for an HTML file is not flat; i.e., it contains a : to indicate subdirectories"""
    def __init__(self, filename=None, message=None):
        super().__init__(filename, message)
        self._level = ErrorLevel.WARNING
