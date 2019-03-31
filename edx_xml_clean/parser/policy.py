"""
policy.py

Validation routines related to the policy file
"""
from edx_xml_clean.utils import traverse
from edx_xml_clean.parser.parser_exceptions import (
    MissingURLName,
    DuplicateURLName
)

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
                errorstore.add_error(MissingURLName(edxobj.filenames[0], tag=edxobj.type))
        else:
            # Record the name
            if url_name in results:
                # We have a collision!
                errorstore.add_error(DuplicateURLName(edxobj.filenames[0],
                                                      url_name=url_name,
                                                      tag1=results[url_name].type,
                                                      file1=results[url_name].filenames[0],
                                                      tag2=edxobj.type,
                                                      file2=edxobj.filenames[0]))
            else:
                results[url_name] = edxobj

    # Return the dictionary
    return results

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

def validate_grading_policy(grading_policy, course, errorstore):
    """
    Validates the grading policy of the course

    :param grading_policy: Grading policy file json
    :param course: EdxCourse object
    :param errorstore: ErrorStore object where errors are reported
    :return: None
    """
    # TODO
    pass
