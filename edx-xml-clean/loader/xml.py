# -*- coding: utf-8 -*-
"""
edxloader.py

Routines to load the XML of an edX course into a structure
"""
import os
from lxml import etree
from lxml.etree import XMLSyntaxError
from loader.objects import EdxCourse
from errors.errors import *

def file_exists(filename):
    """Returns True if filename exists, or False if not"""
    if os.path.isfile(filename):
        return True
    return False

def load_course(filename, errorstore, quiet):
    """
    Loads a course, given a filename for the appropriate course.xml file.

    :param filename: Path and filename for course.xml (or equivalent)
    :param errorstore: ErrorStore object to store errors
    :param quiet: Flag for quiet mode
    :return: EdxCourse object, or None on failure
    """
    # If we've been given a directory, add on 'course.xml'
    if os.path.isdir(filename):
        if not quiet:
            print(f"Received directory: {filename}. Looking for 'course.xml'...")
        filename = os.path.join(filename, "course.xml")

    # Ensure the file exists
    if not file_exists(filename):
        errorstore.add_error(CourseXMLDoesNotExist(filename))
        return

    if not quiet:
        print(f"Loading {filename}")

    # Change to the relevant directory
    directory, file = os.path.split(filename)
    if directory:
        os.chdir(directory)

    # Check file name
    if file != "course.xml":
        errorstore.add_error(CourseXMLName(filename))

    # Obtain the XML for the course.xml file
    try:
        tree = etree.parse(file)
    except XMLSyntaxError as e:
        errorstore.add_error(InvalidXML(filename, e.args[0]))
        return

    # Initialize the course object
    course = EdxCourse()

    # Load the course!
    traverse_course(course, tree.getroot(), file, errorstore)

    return course

def traverse_course(edxobj, node, filename, errorstore, pointer=False):
    """
    Takes in the current EdxObject, the current lxml element, and the
    current filename. Reads from the element into the object, creating
    any children for that object, and recursing into them.

    :param edxobj: The current EdxObject
    :param node: The current lxml element
    :param filename: The current filename
    :param errorstore: An ErrorStore object that is collecting errors
    :param pointer: True if we've arrived at this node due to a pointer tag
    :return: None
    """
    # Make sure that the node matches the edxobj type
    if edxobj.type != node.tag:
        msg = (f"A file is of type <{edxobj.type}> but "
               f"opens with a <{node.tag}> tag")
        errorstore.add_error(TagMismatch(filename, msg))
        return

    # Start by copying the attributes from the node into the object
    edxobj.set_attribs(node.attrib)
    # Set the filename for the object
    edxobj.add_filename(filename)

    # Is the tag an empty tag? (contains only attributes)
    empty = (len(node) == 0 and node.text is None)

    # Check for a pointer tag
    if empty and edxobj.is_pointer(node.attrib):
        if pointer:
            # The target of a pointer tag cannot be a pointer itself
            msg = (f"The tag <{node.tag}> with url_name {edxobj.attributes['url_name']} "
                   "appears to be pointing to itself")
            errorstore.add_error(SelfPointer(filename, msg))
            node.broken = True
            return

        # We have a valid pointer tag
        urlname = edxobj.attributes['url_name']
        if ":" in urlname:
            msg = (f"The <{node.tag}> tag with url_name {urlname} "
                   "uses obsolete colon notation in the url_name to point to a subdirectory")
            errorstore.add_error(NonFlatURLName(filename, msg))
            urlname = urlname.replace(":", "/")
        new_file = edxobj.type + "/" + urlname + ".xml"

        # Ensure the file exists
        if not file_exists(new_file):
            msg = (f"The <{node.tag}> tag with url_name {edxobj.attributes['url_name']} points to "
                   f"the file {new_file} that does not exist")
            errorstore.add_error(FileDoesNotExist(filename, msg))
            node.broken = True
            return

        try:
            new_node = etree.parse(new_file).getroot()
        except XMLSyntaxError as e:
            errorstore.add_error(InvalidXML(filename, e.args[0]))
            return
        else:
            traverse_course(edxobj, new_node, new_file, errorstore, pointer=True)
            return

    # Next, check if the tag shouldn't be empty, and hence should be a pointer
    # but for some reason was an invalid pointer
    if empty and not edxobj.can_be_empty and "url_name" in node.attrib:
        # Likely to be an invalid pointer tag due to too many attributes
        msg = (f"The <{node.tag}> tag with url_name '{edxobj.attributes['url_name']}' "
               f"in {filename} looks like it is an invalid pointer tag")
        errorstore.add_error(InvalidPointer(filename, msg))
        node.broken = True
        return

    # At this stage, we've checked for pointer tags and associated errors

    # The target of a pointer should have no url_name attribute
    if pointer and "url_name" in node.attrib:
        msg = f"The opening <{node.tag}> tag shouldn't have a url_name attribute"
        errorstore.add_error(ExtraURLName(filename, msg))

    # Special case: HTML files can point to an actual HTML file with their 'filename' attribute
    if node.tag == "html" and "filename" in edxobj.attributes:
        filename = edxobj.attributes['filename']
        if ":" in filename:
            if 'url_name' in edxobj.attributes:
                msg = (f"The <html> tag with url_name {edxobj.attributes['url_name']} "
                       "uses obsolete colon notation to point to a subdirectory for filename {filename}")
            else:
                msg = (f"An <html> tag with no "
                       "uses obsolete colon notation to point to a subdirectory for filename {filename}")
            errorstore.add_error(NonFlatFilename(filename, msg))
            filename = filename.replace(":", "/")
        new_file = "html/" + filename + ".html"

        # Ensure the file exists
        if not file_exists(new_file):
            if 'url_name' in edxobj.attributes:
                msg = (f"The tag <{node.tag}> with url_name {edxobj.attributes['url_name']} points to "
                       f"the file {new_file} that does not exist")
            else:
                msg = (f"A tag <{node.tag}> with no url_name points to "
                       f"the file {new_file} that does not exist")
            errorstore.add_error(FileDoesNotExist(filename, msg))
            return

        try:
            with open(new_file) as f:
                html = f.read()
            parser = etree.HTMLParser()
            etree.fromstring(html, parser)
        except Exception as e:
            errorstore.add_error(InvalidHTML(filename, e.args[0]))
            node.broken = True
            return
        else:
            edxobj.content = html
            edxobj.html_content = True
            return

    # Is the tag unexpectedly empty?
    if empty and not edxobj.can_be_empty:
        if 'url_name' in edxobj.attributes:
            msg = (f"The <{node.tag}> tag with url_name '{edxobj.attributes['url_name']}' "
                   f"is unexpectedly empty")
        else:
            msg = f"A <{node.tag}> tag with no url_name is unexpectedly empty"
        errorstore.add_error(EmptyTag(filename, msg))
        return

    # If we get here, we have a non-empty tag

    # Check to see if there is a pointer target file that is not being used
    if not pointer and 'url_name' in edxobj.attributes and edxobj.can_be_pointer:
        new_file = edxobj.type + "/" + edxobj.attributes['url_name'] + ".xml"
        if file_exists(new_file):
            msg = (f"The <{node.tag}> tag with url_name '{edxobj.attributes['url_name']}' "
                   f"is not a pointer, but a file that it could point to exists ({new_file})")
            errorstore.add_error(PossiblePointer(filename, msg))

    if edxobj.content_store:
        # Store content from content tags
        edxobj.content = etree.tostring(node, pretty_print=True)
    else:
        # Check for content in non-content tag
        if node.text and node.text.strip():
            if 'url_name' in edxobj.attributes:
                msg = (f"The <{node.tag}> tag with url_name '{edxobj.attributes['url_name']}' "
                       f"should not contain any text ({node.text.strip()[:10]})")
            else:
                msg = (f"A <{node.tag}> tag with no url_name "
                       f"should not contain any text ({node.text.strip()[:10]})")
            errorstore.add_error(UnexpectedContent(filename, msg))
        else:
            for child in node:
                if child.tail and child.tail.strip():
                    if 'url_name' in edxobj.attributes:
                        msg = (f"The <{node.tag}> tag with url_name '{edxobj.attributes['url_name']}' "
                               f"should not contain any text ({child.tail.strip()[:10]})")
                    else:
                        msg = (f"A <{node.tag}> tag with no url_name "
                               f"should not contain any text ({child.tail.strip()[:10]})")
                    errorstore.add_error(UnexpectedContent(filename, msg))
                    break

        # Recurse into each child
        for child in node:
            if child.tag is etree.Comment:
                # Ignore comments
                pass
            elif child.tag in edxobj.allowed_children:
                # Recurse on that node
                newobj = edxobj.allowed_children[child.tag]()
                edxobj.add_child(newobj)
                traverse_course(newobj, child, filename, errorstore)
            else:
                if 'url_name' in edxobj.attributes:
                    msg = (f"A <{child.tag}> tag was unexpectedly found inside the <{node.tag}> tag with "
                           f"url_name {edxobj.attributes['url_name']}")
                else:
                    msg = (f"A <{child.tag}> tag was unexpectedly found inside a <{node.tag}> tag with "
                           f"no url_name")
                errorstore.add_error(UnexpectedTag(filename, msg))
