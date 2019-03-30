"""
validate.py

Workhorse function that validates an OLX course
"""
import os
from edx_xml_clean.errorstore import ErrorStore
from edx_xml_clean.loader import load_course, load_policy
from edx_xml_clean.parser import (
    find_url_names,
    merge_policy,
    validate_grading_policy,
    checkers
)
from edx_xml_clean.utils import traverse

def validate(filename, quiet=True, ignore=None):
    """
    Validate an OLX course

    :param filename: Location of course xml file or directory
    :param quiet: Output information to the console
    :param ignore: List of errors to ignore
    :return: course object, errorstore object
    """
    # Create an error store
    if ignore is None:
        ignore = []
    errorstore = ErrorStore(ignore)

    # Validation Step #1: Load the course
    if os.path.isdir(filename):
        directory = os.path.join(filename)
        file = "course.xml"
    else:
        directory, file = os.path.split(filename)
    course = load_course(directory, file, errorstore, quiet)
    if not course:
        return course, errorstore

    # Validation Step #2: Load the policy files
    policy, grading_policy = load_policy(directory, course, errorstore)

    # Validation Step #3: Construct a dictionary of url_names
    url_names = find_url_names(course, errorstore)

    # Validation Step #4: Merge policy data into object attributes
    merge_policy(policy, url_names, errorstore)

    # Validation Step #5: Validate grading policy
    validate_grading_policy(grading_policy, errorstore)

    # Validation Step #6: Make every object validate itself
    for edxobj in traverse(course):
        edxobj.validate(errorstore)

    # Validation Step #7: Parse the course for global errors
    for checker in checkers:
        checker(course, errorstore, url_names)

    # Return the course object and errorstore
    return course, errorstore
