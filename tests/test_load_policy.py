"""
test_load_policy.py

Tests for XML policy loading
"""
from tests.helpers import assert_error, assert_caught_all_errors

from edx_xml_clean.errorstore import ErrorStore
from edx_xml_clean.loader import load_policy, load_course
from edx_xml_clean.loader.policy_exceptions import (
    NoRunName,
    PolicyNotFound,
    BadPolicy
)

def test_no_policy():
    errorstore = ErrorStore()
    # Load course (needed before loading policy)
    course = load_course("testcourses/testcourse1", "course.xml", errorstore, True)
    assert_caught_all_errors(errorstore)
    # Load the (nonexistent) policy files
    policy, grading_policy = load_policy("testcourses/testcourse1", course, errorstore)
    handle_course1_errors(errorstore)
    assert_caught_all_errors(errorstore)

def handle_course1_errors(errorstore):
    assert_error(errorstore, PolicyNotFound, 'policies/mycourseurl/policy.json', "The policy file 'policies/mycourseurl/policy.json' was not found.")
    assert_error(errorstore, PolicyNotFound, 'policies/mycourseurl/grading_policy.json', "The policy file 'policies/mycourseurl/grading_policy.json' was not found.")

def test_no_url_name():
    errorstore = ErrorStore()
    # Load course (needed before loading policy)
    course = load_course("testcourses/testcourse4", "course.xml", errorstore, True)
    assert_caught_all_errors(errorstore)
    # Load the (nonexistent) policy files
    policy, grading_policy = load_policy("testcourses/testcourse4", course, errorstore)
    assert_error(errorstore, NoRunName, 'course.xml', "The course tag has no url_name.")
    assert_caught_all_errors(errorstore)

def test_bad_json():
    errorstore = ErrorStore()
    # Load course (needed before loading policy)
    course = load_course("testcourses/testcourse5", "course.xml", errorstore, True)
    assert_caught_all_errors(errorstore)
    # Load the policy files
    policy, grading_policy = load_policy("testcourses/testcourse5", course, errorstore)
    assert_error(errorstore, BadPolicy, 'policies/mycourseurl/policy.json', "The policy file 'policies/mycourseurl/policy.json' has invalid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)")
    assert_error(errorstore, BadPolicy, 'policies/mycourseurl/grading_policy.json', "The policy file 'policies/mycourseurl/grading_policy.json' has invalid JSON: Expecting property name enclosed in double quotes: line 2 column 3 (char 4)")
    assert_caught_all_errors(errorstore)
