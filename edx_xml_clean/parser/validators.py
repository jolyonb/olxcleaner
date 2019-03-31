"""
validators.py

Validation routines that act on the course as a whole
"""
import inspect
from abc import ABC, abstractmethod
from edx_xml_clean.utils import traverse
from edx_xml_clean.parser.parser_exceptions import (
    MissingDisplayName
)

class GlobalValidator(ABC):
    """
    Abstract base class describing global validation routines.
    Only the __call__ method needs to be implemented.
    """

    @abstractmethod
    def __call__(self, course, errorstore, url_names):
        """
        Abstract method to perform validation

        :param course: EdxCourse object with a loaded course
        :param errorstore: ErrorStore object where errors are reported
        :param url_names: Dictionary of url_name to objects
        :return: None
        """

    @classmethod
    def validators(cls):
        """
        Yield an iterable of instances of immediate subclasses of this class
        """
        for child in cls.__subclasses__():
            # Only attempt instantiation if not an abstract base class
            if not inspect.isabstract(child):
                yield child()

class CheckDisplayNames(GlobalValidator):
    """Searches the course for missing display_name attributes"""

    def __call__(self, course, errorstore, url_names):
        for edxobj in traverse(course):
            display_name = edxobj.attributes.get('display_name')
            if edxobj.display_name and (display_name is None or display_name == ""):
                if not edxobj.broken:
                    errorstore.add_error(MissingDisplayName(edxobj.filenames[-1], edxobj=edxobj))
            # TODO: Check to make sure that objects that shouldn't have a display_name don't have one
