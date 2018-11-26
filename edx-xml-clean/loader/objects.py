# -*- coding: utf-8 -*-
"""
objects.py

Contains classes to describe various edX objects
"""
class EdxObject(object):
    """Abstract base class for edX structure objects"""

    def __init__(self):
        """Initialize storage"""
        self.children = []
        self.attributes = {}
        self.filenames = []

    # Can this object store content?
    content_store = False
    # What attributes are needed to be a pointer tag?
    pointer_attr = {'url_name'}
    # What depth does this object typically appear at?
    depth = 0
    # Can this object have pointer tags?
    can_be_pointer = True
    # If this object is obsolete, what message should be displayed?
    obsolete_msg = None
    # What is the name of the directory that stores this content type?
    type = None
    # Can this tag be empty?
    can_be_empty = False

    @property
    def allowed_children(self):
        """
        What children tags can this object contain?
        Note: implemented as property to avoid forward reference problems.
        """
        return {}

    def add_child(self, node):
        """Adds a child to this object"""
        self.children.append(node)

    def set_attribs(self, attribs):
        """Sets the attributes for this node"""
        self.attributes.update(attribs)

    def add_filename(self, value):
        """Adds a filename to the filename list"""
        self.filenames.append(value)

    def __repr__(self):
        """Produce a string representation of this object"""
        name = self.attributes.get("display_name")
        if not name:
            name = self.attributes.get("url_name")
        return f"<{self.type}: {name}>"

    def is_pointer(self, attribs=None):
        """
        Returns True if the attributes allow this node to point to a new file

        Uses attribs if not none, or self.attributes is so
        """
        if attribs is None:
            attribs = self.attributes
        # Follows pointer convention in edX: is_pointer_tag in
        # https://github.com/edx/edx-platform/blob/master/common/lib/xmodule/xmodule/xml_module.py
        # Also needs to have no children and no text
        return set(attribs.keys()) == self.pointer_attr and self.can_be_pointer

class EdxCourse(EdxObject):
    """edX course object"""
    type = "course"
    depth = 0
    # course pointer tags need three attributes:
    pointer_attr = {'url_name', 'course', 'org'}

    @property
    def allowed_children(self):
        return {"chapter": EdxChapter}

class EdxChapter(EdxObject):
    """edX chapter object"""
    type = 'chapter'
    depth = 1

    @property
    def allowed_children(self):
        return {'sequential': EdxSequential}

class EdxSequential(EdxObject):
    """edX sequential object"""
    type = "sequential"
    depth = 2

    @property
    def allowed_children(self):
        return {'vertical': EdxVertical}

class EdxVertical(EdxObject):
    """edX vertical object"""
    type = "vertical"
    depth = 3

    @property
    def allowed_children(self):
        return {'html': EdxHtml,
                'video': EdxVideo,
                'discussion': EdxDiscussion,
                'problem': EdxProblem,
                'lti': EdxLti,
                'lti_consumer': EdxLtiConsumer}

class EdxDiscussion(EdxObject):
    """edX discussion object"""
    type = "discussion"
    depth = 4
    can_be_empty = True

class EdxLti(EdxObject):
    """edX lti object (obsolete)"""
    type = "lti"
    depth = 4
    obsolete_msg = "<lti> entries are obsolete and should be replaced by <lti_consumer>"
    can_be_empty = True

class EdxLtiConsumer(EdxObject):
    """edX lti_consumer object"""
    can_be_pointer = False
    type = "lti_consumer"
    depth = 4
    can_be_empty = True

class EdxContent(EdxObject):
    """Abstract class for edX content objects"""
    content_store = True
    depth = 4
    content = None  # Contains the content of the tag, including the tag itself

class EdxHtml(EdxContent):
    """edX html object"""
    type = "html"
    html_content = False  # Was the content set by slurping up an HTML file directly?
    # If True, content does not contain the wrapping html tag

class EdxProblem(EdxContent):
    """edX problem object"""
    type = "problem"

class EdxVideo(EdxContent):
    """edX video object"""
    type = "video"
    can_be_empty = True
