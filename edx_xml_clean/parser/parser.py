# -*- coding: utf-8 -*-
"""
parser.py

Contains routines to parse a course for errors after loading
"""
from edx_xml_clean.parser.parser_exceptions import (
    MissingURLName,
    DuplicateURLName,
    MissingDisplayName
)
from edx_xml_clean.utils import traverse

def find_url_names(course, errorstore):
    """
    Constructs a dictionary of (url_name: EdxObject) references

    :param course: EdxCourse object with a loaded course
    :param errorstore: ErrorStore object where errors are reported
    :return: Dictionary of {'url_name': EdxObject} links
    """
    results = {}

    # Traverse the tree
    for edxobj in traverse(course):
        url_name = edxobj.attributes.get('url_name')

        if url_name is None:
            if edxobj.needs_url_name and not edxobj.broken:
                # Report the error
                msg = f"A <{edxobj.type}> tag has no url_name"
                errorstore.add_error(MissingURLName(edxobj.filenames[0], msg))
        else:
            # Record the name
            if url_name in results:
                # We have a collision!
                msg = (f"Duplicate url_name found: {url_name} appears as <{results[url_name].type}> in "
                       f"{results[url_name].filenames[0]} and also as <{edxobj.type}> in {edxobj.filenames[0]}")
                errorstore.add_error(DuplicateURLName(edxobj.filenames[0], msg))
            else:
                results[url_name] = edxobj

    # Return the dictionary
    return results

def check_display_names(course, errorstore, url_names):
    """
    Searches the course for missing display_name attributes

    :param course: EdxCourse object with a loaded course
    :param errorstore: ErrorStore object where errors are reported
    :param url_names: Dictionary of url_name to objects
    :return: None
    """
    for edxobj in traverse(course):
        display_name = edxobj.attributes.get('display_name')
        if edxobj.display_name and (display_name is None or display_name == ""):
            if not edxobj.broken:
                if 'url_name' in edxobj.attributes:
                    msg = f"The tag {edxobj} is missing the display_name attribute"
                else:
                    msg = f"A <{edxobj.type}> tag with no url_name is missing the display_name attribute"
                errorstore.add_error(MissingDisplayName(edxobj.filenames[-1], msg))
        # TODO: Check to make sure that objects that shouldn't have a display_name don't have one

def merge_policy(policy, url_names, errorstore):
    """
    Merges policy file data with course objects

    :param policy: Policy file json
    :param url_names: Dictionary of {urlname: EdxObject} pairings
    :param errorstore: ErrorStore object where errors are reported
    :return: None
    """
    if not isinstance(policy, dict):
        # TODO: Handle error
        return

    for entry in policy:
        # Split the entry into object type/url_name
        objtype, url_name = entry.split("/", 1)

        # Find the corresponding object in url_names
        edxobj = url_names.get(url_name, None)

        # Make sure we have an object
        if edxobj is None:
            # TODO: Handle error
            continue

        # Make sure the type matches
        if edxobj.type != objtype:
            # TODO: Handle error
            continue

        # Make sure the entry is a dictionary
        if not isinstance(policy[entry], dict):
            # TODO: Handle error
            continue

        # Copy data into the object
        for element in policy[entry]:
            # Make sure we're not overwriting anything
            if element in edxobj.attributes:
                # TODO: Handle error
                continue

            # Copy the data
            edxobj.attributes[element] = policy[entry][element]

def validate_grading_policy(grading_policy, errorstore):
    """
    Validates the grading policy of the course

    :param grading_policy: Grading policy file json
    :param errorstore: ErrorStore object where errors are reported
    :return: None
    """
    # TODO
    pass
