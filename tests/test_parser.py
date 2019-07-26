"""
test_parser.py

Test course parsing routines
"""
from tests.helpers import assert_error, assert_caught_all_errors

from olxcleaner.errorstore import ErrorStore
from olxcleaner.loader import load_policy, load_course
from olxcleaner.parser.policy import find_url_names, merge_policy, validate_grading_policy
from olxcleaner.parser.parser_exceptions import (
    MissingURLName,
    DuplicateURLName,
    BadPolicyFormat,
    PolicyRefNotFound,
    WrongObjectType,
    BadEntry,
    SettingOverride,
    GradingPolicyIssue
)

def test_url_names():
    errorstore = ErrorStore()

    # Load course
    course = load_course("testcourses/testcourse1", "course.xml", errorstore)
    assert_caught_all_errors(errorstore)

    # Make a dictionary of url_names
    url_names = find_url_names(course, errorstore)
    assert_caught_all_errors(errorstore)

    expected = [
        'mycourseurl',
        'chapter',
        'sequential',
        'vertical',
        'html'
    ]
    for i in expected:
        assert i in url_names

def test_course6_url():
    errorstore = ErrorStore()

    # Load course
    course = load_course("testcourses/testcourse6", "course.xml", errorstore)
    assert_caught_all_errors(errorstore)

    # Load policy
    policy, grading_policy = load_policy("testcourses/testcourse6", course, errorstore)
    assert_caught_all_errors(errorstore)

    # Make a dictionary of url_names
    url_names = find_url_names(course, errorstore)

    # Merge the policy file
    merge_policy(policy, url_names, errorstore)

    # Handle the errors
    handle_course6_errors(errorstore)
    assert_caught_all_errors(errorstore)

def handle_course6_errors(errorstore):
    assert_error(errorstore, MissingURLName, 'course/mycourseurl.xml', "The tag <vertical display_name='vertical name'> has no url_name.")
    assert_error(errorstore, MissingURLName, 'course/mycourseurl.xml', "The tag <vertical display_name='vertical name'> has no url_name.")
    assert_error(errorstore, DuplicateURLName, 'course/mycourseurl.xml', "Duplicate url_name found: 'html' appears as <html> in course/mycourseurl.xml and also as <html> in course/mycourseurl.xml")
    assert_error(errorstore, DuplicateURLName, 'course/mycourseurl.xml', "Duplicate url_name found: 'html' appears as <html> in course/mycourseurl.xml and also as <html> in course/mycourseurl.xml")
    assert_error(errorstore, DuplicateURLName, 'course/mycourseurl.xml', "Duplicate url_name found: 'html2' appears as <html> in course/mycourseurl.xml and also as <html> in course/mycourseurl.xml")
    assert_error(errorstore, BadPolicyFormat, 'policy.json', "The policy file is not a dictionary of values")

def test_course7_url():
    errorstore = ErrorStore()

    # Load course
    course = load_course("testcourses/testcourse7", "course.xml", errorstore)
    assert_caught_all_errors(errorstore)

    # Load policy
    policy, grading_policy = load_policy("testcourses/testcourse7", course, errorstore)
    assert_caught_all_errors(errorstore)

    # Make a dictionary of url_names
    url_names = find_url_names(course, errorstore)

    # Merge the policy file
    merge_policy(policy, url_names, errorstore)
    # Ensure that settings were indeed merged
    assert(url_names['sequential2'].attributes['setting'])

    # Validate the grading policy
    validate_grading_policy(grading_policy, errorstore)

    # Handle the errors
    handle_course7_errors(errorstore)
    assert_caught_all_errors(errorstore)

def handle_course7_errors(errorstore):
    assert_error(errorstore, DuplicateURLName, 'course/mycourseurl.xml', "Duplicate url_name found: 'html4' appears as <html> in course/mycourseurl.xml and also as <html> in course/mycourseurl.xml")
    assert_error(errorstore, PolicyRefNotFound, 'policy.json', "The policy file refers to <problem url_name='noexist'> which does not exist in the course structure")
    assert_error(errorstore, WrongObjectType, 'policy.json', "The policy file refers to a <video> tag with url_name 'html4'. However, that url_name points to a <html> tag.")
    assert_error(errorstore, BadEntry, 'policy.json', "The policy file entry for <vertical url_name='vertical3'> is not a dictionary")
    assert_error(errorstore, SettingOverride, 'policy.json', "The policy file entry for <sequential url_name='sequential2'> is overriding the setting for 'setting'")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is missing 'A'")

def test_grading_policy():
    # Test grading policy entries in isolation
    errorstore = ErrorStore()

    # Set up the policy
    policy = {}
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'GRADER' entry not found in grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'GRADE_CUTOFFS' entry not found in grading policy")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': {},
        'GRADE_CUTOFFS': []
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'GRADER' entry not in grading policy is not a list")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'GRADE_CUTOFFS' entry not in grading policy is not a dictionary")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Lab",
                "short_label": 15,
                "weight": 0.15
            },
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 0.15
            },
        ],
        'GRADE_CUTOFFS': {
            'Pass': -1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'weight' settings do not add up to 1")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'short_label' setting is not a string for entry 1 in the grading policy")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 'hi',
                "min_count": 'hi',
                "type": 0,
                "weight": 'hi'
            },
            {
                "drop_count": -1,
                "min_count": 0,
                "type": "Something",
                "weight": 1.1
            },
            {
            },
        ],
        'GRADE_CUTOFFS': {
            'Pass': 2
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'drop_count' setting is not an integer for entry 1 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'min_count' setting is not an integer for entry 1 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'type' setting is not a string for entry 1 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'weight' setting is not a number between 0 and 1 for entry 1 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'drop_count' setting is negative for entry 2 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'min_count' setting is less than 1 for entry 2 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'weight' setting is not a number between 0 and 1 for entry 2 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'drop_count' setting is omitted for entry 3 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'min_count' setting is omitted for entry 3 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'type' setting is omitted for entry 3 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'weight' setting is omitted for entry 3 in the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'weight' settings do not add up to 1")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json',
                 "'Pass' entry is not between 0 and 1 in the GRADE_CUTOFFS part of the grading policy")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 0.6
            },
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 0.4
            },
        ],
        'GRADE_CUTOFFS': {
            'A': -1,
            'C': 3,
            'D': 0.5,
            'Pass': 'ok',
            'pass': 1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'A' entry is not between 0 and 1 in the GRADE_CUTOFFS part of the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'C' entry is not between 0 and 1 in the GRADE_CUTOFFS part of the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'pass' is not allowed in the GRADE_CUTOFFS part of the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "'Pass' entry is not a number in the GRADE_CUTOFFS part of the grading policy")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "Assessment type 'Something' appears multiple times in the grading policy")
    assert_caught_all_errors(errorstore)


    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'A': 0,
            'C': 0.2,
            'D': 0.5,
            'Pass': 0.6,
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS should have either 'Pass' or letters, not both")
    assert_caught_all_errors(errorstore)


    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'A': 0,
            'C': 0.2,
            'D': 0.5
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is missing 'B'")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is entry 'C' is not decreasing")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is entry 'D' is not decreasing")
    assert_caught_all_errors(errorstore)


    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'A': 0,
            'B': 0.1,
            'C': 0.2,
            'D': 0.5
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is entry 'B' is not decreasing")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is entry 'C' is not decreasing")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is entry 'D' is not decreasing")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
        ],
        'GRADE_CUTOFFS': {
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADER entry in grading policy should not be empty")
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS entry in grading policy should not be empty")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'A': 1,
            'C': 0.1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is missing 'B'")
    assert_caught_all_errors(errorstore)

    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'B': 1,
            'C': 0.1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is missing 'A'")
    assert_caught_all_errors(errorstore)


    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'B': 1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS is missing 'A'")
    assert_caught_all_errors(errorstore)


    # Set up the policy
    policy = {
        'GRADER': [
            {
                "drop_count": 2,
                "min_count": 12,
                "type": "Something",
                "weight": 1
            },
        ],
        'GRADE_CUTOFFS': {
            'A': 1
        }
    }
    # Validate it
    validate_grading_policy(policy, errorstore)
    # Handle errors
    assert_error(errorstore, GradingPolicyIssue, 'grading_policy.json', "GRADE_CUTOFFS should use 'Pass' instead of 'A'")
    assert_caught_all_errors(errorstore)
