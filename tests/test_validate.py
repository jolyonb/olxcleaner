"""
test_validate.py

Tests the full validation pipeline
"""
from edx_xml_clean import validate
from tests.helpers import assert_caught_all_errors
from tests.test_load_xml import handle_course2_errors, handle_nocourse_errors
from tests.test_load_policy import handle_course1_errors
from tests.test_parser import handle_course7_errors

def test_validate_nocourse():
    course, errorstore = validate("testcourses/nocourse.xml", 2)
    handle_nocourse_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course1():
    course, errorstore = validate("testcourses/testcourse1", 2)
    handle_course1_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course2():
    course, errorstore = validate("testcourses/testcourse2/coursefile.xml", 1)
    handle_course2_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course7():
    course, errorstore = validate("testcourses/testcourse7/course.xml", 5)
    handle_course7_errors(errorstore)
    assert_caught_all_errors(errorstore)
