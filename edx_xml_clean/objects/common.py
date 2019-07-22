"""
common.py

Contains abstract base classes to describe various edX objects
"""
from abc import ABC, ABCMeta, abstractmethod

class EdxObject(ABC):
    """Abstract base class for edX structure objects"""

    def __init__(self):
        """Initialize storage"""
        # Stores the children objects of this object
        self.children = []

        # Stores the attributes of this object
        self.attributes = {}

        # Stores the filenames associated with this object
        # If this file is loaded using a url_name pointer, will
        # contain two entries: [pointerfile, contentfile]
        # If not, will just contain one entry: [contentfile]
        self.filenames = []

    # Default settings

    # Can this object store content?
    content_store = False

    # Can this object be referenced using pointer tags?
    can_be_pointer = True
    # What attributes are needed to be a pointer tag?
    pointer_attr = {'url_name'}

    # What depth does this object typically appear at? (used for reporting)
    depth = 0

    # What is the name of the tag? (also the directory that stores this content type)
    type = None

    # Can this tag be empty?
    can_be_empty = False

    # Does this tag need a display_name attribute? Options are True, False and 'optional'
    display_name = False

    # Does this tag need a url_name attribute?
    needs_url_name = True

    # Is this element broken (and hence needs no further errors reported?)
    broken = False

    @property
    def allowed_children(self):
        """
        What children object types can this object contain?
        Note: implemented as property to avoid forward reference problems.
        """
        return []

    def add_child(self, node):
        """Adds a child to this object"""
        self.children.append(node)

    def add_attribs(self, attribs):
        """Adds to the attributes for this object"""
        self.attributes.update(attribs)

    def add_filename(self, value):
        """Adds a filename to the filename list for this object"""
        self.filenames.append(value)

    def __repr__(self):
        """Produce a string representation of this object"""
        name = self.attributes.get("display_name")
        if not name:
            name = self.attributes.get("url_name")
        return f"<{self.type}: {name}>"

    def is_pointer(self, attribs=None):
        """
        Returns True if the attributes for this object imply that it
        is a pointer object, pointing to a new file

        Uses attribs if passed in, or self.attributes if not
        """
        if attribs is None:
            attribs = self.attributes
        # Follows pointer convention in edX: is_pointer_tag in
        # https://github.com/edx/edx-platform/blob/master/common/lib/xmodule/xmodule/xml_module.py
        # Also needs to have no children and no text (not tested)
        return set(attribs.keys()) == self.pointer_attr and self.can_be_pointer

    @abstractmethod
    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        Objects should validate their contents other than those tags
        contained in allowed_children.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass

    # List of subclasses of EdxObject
    _subclasses = []

    @staticmethod
    def get_object(object_type):
        """
        Returns a class instance that has type object_type

        :param object_type: type parameter for the desired class
        :return: Class with type object_type
        """
        # If it doesn't already exist, construct the list of subclasses
        if not EdxObject._subclasses:
            subclasses = set()
            work = [EdxObject]
            while work:
                parent = work.pop()
                for child in parent.__subclasses__():
                    if child not in subclasses:
                        subclasses.add(child)
                        work.append(child)
            EdxObject._subclasses = list(subclasses)

        for cls in EdxObject._subclasses:
            if cls.type == object_type:
                return cls()
        raise ValueError(f"Cannot instantiate object of unknown type <{object_type}>")

class EdxContent(EdxObject, metaclass=ABCMeta):
    """Abstract class for edX content objects"""

    # Can this object store content?
    content_store = True

    # What depth does this object typically appear at? (used for reporting)
    depth = 4

    # Contains the content of the tag, including the tag itself
    content = None
