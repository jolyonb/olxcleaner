# -*- coding: utf-8 -*-
"""
edxloader.py

Routines to load the XML of an edX course into a structure
"""
import os
from lxml import etree
from lxml.etree import XMLSyntaxError
from loader.objects import EdxCourse
from loader.utils import file_exists
from errors.errors import CourseXMLDoesNotExist

def load_course(filename, errorstore):
    """
    Loads a course, given a filename for the appropriate course.xml file.

    :param filename: Path and filename for course.xml (or equivalent)
    :param errorstore: ErrorStore object to store errors
    :return: EdxCourse object
    """
    print(f"Loading {filename}")
    # Ensure the file exists
    if not file_exists(filename):
        errorstore.add_error(CourseXMLDoesNotExist(filename))
        return

    # Change to the relevant directory
    directory, file = os.path.split(filename)
    if directory:
        os.chdir(directory)

    # Obtain the XML for the course.xml file
    tree = load_xml(file)

    # If everything is ok...
    course = EdxCourse()
    if tree:
        # Traverse the course!
        traverse_course(course, tree.getroot(), file)

    return course

def load_xml(filename):
    """
    Loads the file into an lxml elementtree.
    :param filename: The filename to load
    :return: lxml elementtree of the xml it contains
    """
    # TODO: Check if the file exists first
    try:
        return etree.parse(filename)
    except XMLSyntaxError as e:
        print("Bad course.xml file!")
        print(e.args[0])

def traverse_course(edxobj, node, filename):
    """
    Takes in the current EdxObject, the current lxml element, and the
    current filename. Reads from the element into the object, creating
    any children for that object, and recursing into them.

    :param edxobj: The current EdxObject
    :param node: The current lxml element
    :param filename: The current filename
    :return: None
    """
    # TODO: Make sure that the node matches the edxobj type

    # Start by copying the attributes from the node into the object
    edxobj.set_attribs(node.attrib)
    # Set the filename for the object
    edxobj.add_filename(filename)

    # Check if the node is empty
    if len(node) == 0 and node.text is None:
        # This may be a pointer tag - if so, follow it
        if edxobj.is_pointer:
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
