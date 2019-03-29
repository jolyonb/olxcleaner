"""
validator.py

Provides methods for validating an OLX course
"""
import os
from errors.errorstore import ErrorStore
from loader.xml import load_course
from parser import scan_course

def validate(filename, quiet=True, ignore=None):
    """
    Validate an OLX course

    :param filename: Location of course xml file or directory
    :param quiet: Output information to the console
    :param ignore: List of errors to ignore
    :return: course object, errorstore object
    """
    # Save current directory
    current_dir = os.getcwd()

    # Construct the error store
    if ignore is None:
        ignore = []
    errorstore = ErrorStore(ignore)

    # Load the course
    course = load_course(filename, errorstore, quiet)

    if course:
        # Load the policy file
        # TODO

        # Parse the course for errors
        scan_course(course, errorstore)

    # Change the directory back
    os.chdir(current_dir)

    # Return the course object and errorstore
    return course, errorstore
