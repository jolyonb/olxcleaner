"""
test_validate.py

Tests the full validation pipeline
"""
from edx_xml_clean import validate
from tests.helpers import assert_caught_all_errors, assert_error
from tests.test_load_xml import handle_course2_errors, handle_nocourse_errors
from tests.test_load_policy import handle_course1_errors
from tests.test_parser import handle_course7_errors
from edx_xml_clean.parser.parser_exceptions import (InvalidSetting, DateOrdering, MissingURLName,
                                                    Obsolete, LTIError, MissingFile)
from edx_xml_clean.parser.policy import find_url_names

def test_validate_nocourse():
    course, errorstore, url_names = validate("testcourses/nocourse.xml", 2)
    handle_nocourse_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course1():
    course, errorstore, url_names = validate("testcourses/testcourse1", 2)
    handle_course1_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course2():
    course, errorstore, url_names = validate("testcourses/testcourse2/coursefile.xml", 1)
    handle_course2_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course7():
    course, errorstore, url_names = validate("testcourses/testcourse7/course.xml", 5)
    handle_course7_errors(errorstore)
    assert_caught_all_errors(errorstore)

def test_validate_course8():
    """This test includes individual component validation. Almost everything should pass."""
    course, errorstore, url_names = validate("testcourses/testcourse8", 6)
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "The <course> tag with url_name 'mycourseurl' does not have the required setting 'course_image'.")
    assert_caught_all_errors(errorstore)

def test_validate_course9():
    """This test includes individual component validation. This similar to course8, but riddled with errors."""
    course, errorstore, url_names = validate("testcourses/testcourse9", 6)
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The <problem> tag with url_name 'problem' has an invalid setting 'showanswer=bad'.")
    assert_error(errorstore, InvalidSetting, 'chapter/chapter.xml', "The <chapter> tag with url_name 'chapter' has an invalid date setting for start: 'Feb 20, 2019, 17:00zzz'.")
    assert_error(errorstore, DateOrdering, 'sequential/sequential.xml', "The <sequential> tag with url_name 'sequential' has a date out of order: start date cannot be before course start date")
    assert_error(errorstore, DateOrdering, 'vertical/vertical.xml', "The <vertical> tag with url_name 'vertical' has a date out of order: due date must be before course end date")
    assert_error(errorstore, DateOrdering, 'problem/problem.xml', "The <problem> tag with url_name 'problem' has a date out of order: start date must be before due date")
    assert_error(errorstore, MissingURLName, 'vertical/vertical.xml', "A <problem> tag has no url_name")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "A <problem> tag with no url_name has an invalid setting 'showanswer=hah!'.")
    assert_error(errorstore, DateOrdering, 'vertical/vertical.xml', "A <problem> tag with no url_name has a date out of order: due date must be before course end date")
    assert_error(errorstore, Obsolete, 'vertical/vertical.xml', "The <discussion> tag with url_name 'discussion' should be included inline rather than through the discussion directory.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The <discussion> tag with url_name 'discussion' does not have the required setting 'discussion_id'.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The <discussion> tag with url_name 'discussion' does not have the required setting 'discussion_target'.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The <discussion> tag with url_name 'discussion' does not have the required setting 'discussion_category'.")
    assert_error(errorstore, Obsolete, 'lti/lti.xml', "The <lti> tag with url_name 'lti' should be converted to the newer lti_consumer Xblock.")
    assert_error(errorstore, InvalidSetting, 'lti/lti.xml', "The <lti> tag with url_name 'lti' does not have the required setting 'launch_url'.")
    assert_error(errorstore, LTIError, 'lti/lti.xml', "Course policy does not include an 'lti_passports' entry for 'nothere', required for an <lti> block.")
    assert_error(errorstore, LTIError, 'lti/lti.xml', "Course policy does not include the 'lti' advanced module, required for an <lti> block.")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "The <lti_consumer> tag with url_name 'meep' does not have the required setting 'launch_url'.")
    assert_error(errorstore, LTIError, 'vertical/vertical.xml', "Course policy does not include an 'lti_passports' entry for 'nothere', required for an <lti_consumer> block.")
    assert_error(errorstore, LTIError, 'vertical/vertical.xml', "Course policy does not include the 'lti_consumer' advanced module, required for an <tli_consumer> block.")
    assert_error(errorstore, MissingFile, 'course/mycourseurl.xml', "Reference to a missing static file: course_image_small.jpg")
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "Unable to recognize graceperiod format.")
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The <problem> tag with url_name 'problem' has a negative problem weight.")
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "The <course> tag with url_name 'mycourseurl' should have a positive number of attempts.")
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The <problem> tag with url_name 'problem' should have a positive number of attempts.")
    assert_caught_all_errors(errorstore)

    # Ensure that we got the scripts from the problem file
    assert set(url_names['problem'].scripts) == {'python', 'perl', 'javascript'}
    # Also make sure we detected the problem types
    assert set(url_names['problem'].response_types) == {'customresponse', 'multiplechoiceresponse'}

# TODO: Get code coverage to 100%...
