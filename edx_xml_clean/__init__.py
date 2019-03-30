"""
edX XML Cleaner

A validator for XML edX courses
Copyright (C) 2018-2019 Jolyon Bloomfield

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
from edx_xml_clean.errors import ErrorStore
from edx_xml_clean.loader import load_course, load_policy
from edx_xml_clean.parser import find_url_names, checkers

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

    # Create an error store
    if ignore is None:
        ignore = []
    errorstore = ErrorStore(ignore)

    # Validation Step #1: Load the course
    course = load_course(filename, errorstore, quiet)
    if not course:
        return course, errorstore

    # Validation Step #2: Load and validate the policy file
    # TODO

    # Validation Step #3: Construct a dictionary of url_names
    url_names = find_url_names(course, errorstore)

    # Validation Step #4: Copy policy data into object attributes

    # Validation Step #5: Make every object validate itself
    # TODO

    # Validation Step #6: Parse the course for global errors
    for checker in checkers:
        checker(course, errorstore, url_names)

    # Change the directory back to where we started
    os.chdir(current_dir)

    # Return the course object and errorstore
    return course, errorstore
