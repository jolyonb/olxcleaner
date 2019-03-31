# -*- coding: utf-8 -*-
"""
policyloader.py

Routines to load the policy files of an edX course
"""
import os
from os.path import isfile
import json
from edx_xml_clean.loader.policy_exceptions import (
    NoRunName
)

def load_policy(directory, course, errorstore):
    """
    Loads the policy file for a course. If loading fails, empty
    dictionaries are returned.

    :param directory: Path for course.xml (or equivalent)
    :param course: EdxCourse object from parsed course
    :param errorstore: ErrorStore object to store errors
    :return: policy, grading_policy objects
    """
    # Get the run name for the course
    runname = course.attributes.get("url_name")
    if runname is None:
        errorstore.add_error(NoRunName(course.filenames[0], None))
        return {}, {}

    # Construct filenames for policy files
    policyfile = os.path.join(directory, "policies", runname, "policy.json")
    gradingfile = os.path.join(directory, "policies", runname, "grading_policy.json")

    # Load the policy files
    policy = load_json(policyfile, errorstore)
    grading_policy = load_json(gradingfile, errorstore)

    # Return the results
    return policy, grading_policy

def load_json(filename, errorstore):
    """
    Load json from a file, storing any loading errors in the errorstore

    :param filename: File to load
    :param errorstore: ErrorStore object to store errors
    :return: Contents of json file
    """
    if not isfile(filename):
        # TODO: Error handling (file error)
        return {}

    try:
        with open(filename) as f:
            return json.load(f)
    except Exception:
        # TODO: Error handling (json error, file error)
        return {}
