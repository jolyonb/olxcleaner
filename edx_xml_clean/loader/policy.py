# -*- coding: utf-8 -*-
"""
policyloader.py

Routines to load the policy files of an edX course
"""
import os
from os.path import isfile
import json
from edx_xml_clean.loader.policy_exceptions import (
    NoRunName,
    PolicyNotFound,
    BadPolicy
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
        errorstore.add_error(NoRunName(course.filenames[0]))
        return {}, {}

    # Construct filenames for policy files
    policyfile = os.path.join("policies", runname, "policy.json")
    gradingfile = os.path.join("policies", runname, "grading_policy.json")

    # Load the policy files
    policy = load_json(directory, policyfile, errorstore)
    grading_policy = load_json(directory, gradingfile, errorstore)

    # Return the results
    return policy, grading_policy

def load_json(directory, filename, errorstore):
    """
    Load json from a file, storing any loading errors in the errorstore

    :param directory: Course directory
    :param filename: File to load
    :param errorstore: ErrorStore object to store errors
    :return: Contents of json file
    """
    fullfile = os.path.join(directory, filename)

    if not isfile(fullfile):
        errorstore.add_error(PolicyNotFound(filename))
        return {}

    try:
        with open(fullfile) as f:
            return json.load(f)
    except json.decoder.JSONDecodeError as err:
        errorstore.add_error(BadPolicy(filename, msg=str(err)))
        return {}
