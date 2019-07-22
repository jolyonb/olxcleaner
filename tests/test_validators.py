"""
test_validators.py

Tests for validators and slow validators
"""
from edx_xml_clean import validate
from edx_xml_clean.parser.validators import CheckDisplayNames
from tests.helpers import assert_caught_all_errors, assert_error
from edx_xml_clean.parser.parser_exceptions import MissingDisplayName, ExtraDisplayName

def test_display_names():
    # Perform all steps on course 10 up to validation steps
    course, errorstore, url_names = validate("testcourses/testcourse10", 6)
    # Everything should be clean (so far!)
    assert_caught_all_errors(errorstore)

    # Check the display names
    validator = CheckDisplayNames()
    validator(course, errorstore, url_names)

    # Catch everything!
    assert_error(errorstore, MissingDisplayName, 'course/mycourseurl.xml', "The tag <course: (Unnamed) (mycourseurl)> is missing the display_name attribute.")
    assert_error(errorstore, MissingDisplayName, 'course/mycourseurl.xml', "The tag <html: (Unnamed) (html)> is missing the display_name attribute.")
    assert_error(errorstore, ExtraDisplayName, 'vertical/oravert.xml', "The tag <openassessment: 'Hah!' (paper-draft)> has an erroneous display_name attribute.")

    assert_caught_all_errors(errorstore)
