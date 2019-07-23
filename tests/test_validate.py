"""
test_validate.py

Tests the full validation pipeline
"""
from edx_xml_clean import validate
from tests.helpers import assert_caught_all_errors, assert_error
from tests.test_load_xml import handle_course2_errors, handle_nocourse_errors
from tests.test_load_policy import handle_course1_errors
from tests.test_parser import handle_course7_errors
from tests.test_validators import (handle_discussion_id_errors_in_10, handle_display_name_errors_in_10,
                                   handle_general_errors_in_10, handle_link_errors_in_10)
from edx_xml_clean.parser.parser_exceptions import (InvalidSetting, DateOrdering, MissingURLName,
                                                    Obsolete, LTIError, MissingFile)

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
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "The tag <course: (Unnamed) (mycourseurl)> does not have the required setting 'course_image'.")
    assert_caught_all_errors(errorstore)

def test_validate_course9():
    """This test includes individual component validation. This similar to course8, but riddled with errors."""
    course, errorstore, url_names = validate("testcourses/testcourse9", 6)
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The tag <problem: (Unnamed) (problem)> has an invalid setting 'showanswer=bad'.")
    assert_error(errorstore, InvalidSetting, 'chapter/chapter.xml', "The tag <chapter: 'Hi there!' (chapter)> has an invalid date setting for start: 'Feb 20, 2019, 17:00zzz'.")
    assert_error(errorstore, DateOrdering, 'sequential/sequential.xml', "The tag <sequential: 'Hi there!' (sequential)> has a date out of order: start date cannot be before course start date")
    assert_error(errorstore, DateOrdering, 'vertical/vertical.xml', "The tag <vertical: 'Hi mom!' (vertical)> has a date out of order: due date must be before course end date")
    assert_error(errorstore, DateOrdering, 'problem/problem.xml', "The tag <problem: (Unnamed) (problem)> has a date out of order: start date must be before due date")
    assert_error(errorstore, MissingURLName, 'vertical/vertical.xml', "The tag <problem: 'no url_name' (no url_name)> has no url_name.")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "The tag <problem: 'no url_name' (no url_name)> has an invalid setting 'showanswer=hah!'.")
    assert_error(errorstore, DateOrdering, 'vertical/vertical.xml', "The tag <problem: 'no url_name' (no url_name)> has a date out of order: due date must be before course end date")
    assert_error(errorstore, Obsolete, 'vertical/vertical.xml', "The tag <discussion: (Unnamed) (discussion)> should be included inline rather than through the discussion directory.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The tag <discussion: (Unnamed) (discussion)> does not have the required setting 'discussion_id'.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The tag <discussion: (Unnamed) (discussion)> does not have the required setting 'discussion_target'.")
    assert_error(errorstore, InvalidSetting, 'discussion/discussion.xml', "The tag <discussion: (Unnamed) (discussion)> does not have the required setting 'discussion_category'.")
    assert_error(errorstore, Obsolete, 'lti/lti.xml', "The tag <lti: (Unnamed) (lti)> should be converted to the newer lti_consumer Xblock.")
    assert_error(errorstore, InvalidSetting, 'lti/lti.xml', "The tag <lti: (Unnamed) (lti)> does not have the required setting 'launch_url'.")
    assert_error(errorstore, LTIError, 'lti/lti.xml', "Course policy does not include an 'lti_passports' entry for 'nothere', required for <lti: (Unnamed) (lti)>.")
    assert_error(errorstore, LTIError, 'lti/lti.xml', "Course policy does not include the 'lti' advanced module, required for <lti: (Unnamed) (lti)>.")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "The tag <lti_consumer: (Unnamed) (meep)> does not have the required setting 'launch_url'.")
    assert_error(errorstore, LTIError, 'vertical/vertical.xml', "Course policy does not include an 'lti_passports' entry for 'nothere', required for <lti_consumer: (Unnamed) (meep)>.")
    assert_error(errorstore, LTIError, 'vertical/vertical.xml', "Course policy does not include the 'lti_consumer' advanced module, required for <lti_consumer: (Unnamed) (meep)>.")
    assert_error(errorstore, MissingFile, 'course/mycourseurl.xml', "The <course: (Unnamed) (mycourseurl)> tag contains a reference to a missing static file: course_image_small.jpg")
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "Unable to recognize graceperiod format in policy.")
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The tag <problem: (Unnamed) (problem)> has a negative problem weight.")
    assert_error(errorstore, InvalidSetting, 'course/mycourseurl.xml', "The tag <course: (Unnamed) (mycourseurl)> should have a positive number of attempts.")
    assert_error(errorstore, InvalidSetting, 'problem/problem.xml', "The tag <problem: (Unnamed) (problem)> should have a positive number of attempts.")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "The tag <drag-and-drop-v2: 'This is my title' (studio_mess2)> has an error in the data JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1).")
    assert_error(errorstore, InvalidSetting, 'vertical/vertical.xml', "The tag <drag-and-drop-v2: 'This is my title' (studio_mess3)> data JSON is not a dictionary.")
    assert_error(errorstore, InvalidSetting, 'sequential/examseq.xml', "The tag <sequential: 'Exam' (examseq)> is a timed exam, but the course policy does not have 'enable_timed_exams=true'.")
    assert_error(errorstore, DateOrdering, 'vertical/oravert.xml', "The tag <openassessment (paper-draft)> has a date out of order: assessment 1 due date must be before course end date")
    assert_caught_all_errors(errorstore)

    # Ensure that we got the scripts from the problem file
    assert set(url_names['problem'].scripts) == {'python', 'perl', 'javascript'}
    # Also make sure we detected the response types
    assert set(url_names['problem'].response_types) == {'customresponse', 'multiplechoiceresponse'}
    # as well as the input types
    assert set(url_names['problem'].input_types) == {'choicegroup', 'textline'}
    # We also found the solution
    assert url_names['problem'].has_solution

    # Make sure our exam sequential was detected
    assert url_names['examseq'].is_exam

def test_validate_course10():
    """This test includes all validation steps. The course is designed to test the validators and slow validators."""
    course, errorstore, url_names = validate("testcourses/testcourse10")
    handle_general_errors_in_10(errorstore)
    handle_display_name_errors_in_10(errorstore)
    handle_discussion_id_errors_in_10(errorstore)
    handle_link_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)
