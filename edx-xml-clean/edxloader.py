#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edxloader.py

Routines to load the XML of an edX course into a structure
"""
import os
from lxml import etree
from lxml.etree import XMLSyntaxError

class edXobject(object):
    """Abstract base class for edX structure objects"""

    def __init__(self):
        """Initialize storage"""
        self.children = []
        self.attributes = {}
        self._filenames = []

    @property
    def type(self):
        raise NotImplementedError()

    @property
    def content_store(self):
        return False

    @property
    def allowed_children(self):
        return {}

    def add_child(self, node):
        """Adds a child to this object"""
        self.children.append(node)

    def set_attribs(self, attribs):
        """Sets the attributes for this node"""
        self.attributes.update(attribs)

    @property
    def filenames(self):
        return self._filenames

    def add_filename(self, value):
        self._filenames.append(value)

    def __repr__(self):
        name = self.attributes.get("display_name")
        if not name:
            name = self.attributes.get("url_name")
        return f"<{self.type}: {name}>"

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        raise NotImplementedError()


class edXcontent(edXobject):
    """Abstract class for edX content objects"""
    @property
    def content_store(self):
        return True

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        return 4

class edXcourse(edXobject):
    """edX course object"""

    @property
    def type(self):
        return "course"

    @property
    def allowed_children(self):
        return {"chapter": edXchapter}

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        return 0

class edXchapter(edXobject):
    """edX chapter object"""

    @property
    def type(self):
        return "chapter"

    @property
    def allowed_children(self):
        return {'sequential': edXsequential}

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        return 1

class edXsequential(edXobject):
    """edX sequential object"""

    @property
    def type(self):
        return "sequential"

    @property
    def allowed_children(self):
        return {'vertical': edXvertical}

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        return 2

class edXvertical(edXobject):
    """edX vertical object"""

    @property
    def type(self):
        return "vertical"

    @property
    def allowed_children(self):
        return {'html': edXhtml,
                'video': edXvideo,
                'discussion': edXdiscussion,
                'problem': edXproblem}

    @property
    def depth(self):
        """Returns an integer indicating the typical depth of this object"""
        return 3

class edXhtml(edXcontent):
    """edX html object"""

    @property
    def type(self):
        return "html"

class edXvideo(edXcontent):
    """edX video object"""

    @property
    def type(self):
        return "video"

class edXdiscussion(edXcontent):
    """edX discussion object"""

    @property
    def type(self):
        return "discussion"

class edXproblem(edXcontent):
    """edX problem object"""

    @property
    def type(self):
        return "problem"

def traverse_course(edxobj, node, filename):
    """
    Takes in the current edXobject, the current lxml element, and the
    current filename. Reads from the element into the object, creating
    any children for that object, and recursing into them.

    :param edxobj: The current edXobject
    :param node: The current lxml element
    :param filename: The current filename
    :return: None
    """
    # Make sure that the node matches the edxobj type

    # Start by copying the attributes from the node into the object
    edxobj.set_attribs(node.attrib)
    # Set the filename for the object
    edxobj.add_filename(filename)

    # Check if the node is empty
    if len(node) == 0 and node.text is None:
        # Node is empty
        # Follow any url_name pointers
        if 'url_name' in edxobj.attributes:
            new_file = edxobj.type + "/" + edxobj.attributes['url_name'] + ".xml"
            if filename != new_file:
                new_node = load_xml(new_file).getroot()
                if new_node is not None:
                    traverse_course(edxobj, new_node, new_file)
        return

    # Recurse into each child
    for child in node:
        # If it's an allowed child, recurse on that node
        if child.tag in edxobj.allowed_children:
            newobj = edxobj.allowed_children[child.tag]()
            edxobj.add_child(newobj)
            traverse_course(newobj, child, filename)

def load_xml(filename):
    """
    Loads the file into an lxml elementtree.
    :param filename: The filename to load
    :return: lxml elementtree of the xml it contains
    """
    try:
        return etree.parse(filename)
    except XMLSyntaxError as e:
        print("Bad course.xml file!")
        print(e.args[0])

def load_course(filename):
    """
    Loads a course, given a filename for the appropriate course.xml file.

    :param filename: Path and filename for course.xml (or equivalent)
    :return: edXcourse object
    """
    if not os.path.isfile(filename):
        print(f"Unable to load {filename}. It looks like the file doesn't exist.")
        return

    # Grab the directory and filename
    directory, file = os.path.split(filename)
    # Change directory
    if directory:
        os.chdir(directory)

    # Set up the course
    course = edXcourse()

    # Obtain the XML for the course.xml file
    tree = load_xml(file)

    # If everything is ok...
    if tree:
        # Traverse the course!
        traverse_course(course, tree.getroot(), file)

    return course
