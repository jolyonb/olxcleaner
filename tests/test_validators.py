"""
test_validators.py

Tests for validators and slow validators
"""
from edx_xml_clean import validate
from edx_xml_clean.loader.xml_exceptions import TagMismatch
from edx_xml_clean.parser.validators import CheckDisplayNames, CheckDiscussionIDs
from edx_xml_clean.parser.slowvalidators import CheckLinks
from tests.helpers import assert_caught_all_errors, assert_error
from edx_xml_clean.parser.parser_exceptions import MissingDisplayName, ExtraDisplayName, DuplicateID

def test_display_names():
    # Perform all steps on course 10 up to validation steps
    course, errorstore, url_names = validate("testcourses/testcourse10", 6)
    handle_general_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

    # Check the display names
    validator = CheckDisplayNames()
    validator(course, errorstore, url_names)

    # Catch everything!
    handle_display_name_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

def handle_general_errors_in_10(errorstore):
    assert_error(errorstore, TagMismatch, 'chapter/broken_chapter.xml', "The file is of type <chapter> but opens with a <sequential> tag")

def handle_display_name_errors_in_10(errorstore):
    assert_error(errorstore, MissingDisplayName, 'course/mycourseurl.xml', "The tag <course: (Unnamed) (mycourseurl)> is missing the display_name attribute.")
    assert_error(errorstore, MissingDisplayName, 'course/mycourseurl.xml', "The tag <html: (Unnamed) (html)> is missing the display_name attribute.")
    assert_error(errorstore, ExtraDisplayName, 'vertical/oravert.xml', "The tag <openassessment: 'Hah!' (paper-draft)> has an erroneous display_name attribute.")

def test_discussion_ids():
    # Perform all steps on course 10 up to validation steps
    course, errorstore, url_names = validate("testcourses/testcourse10", 6)
    handle_general_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

    # Check the discussion IDs
    validator = CheckDiscussionIDs()
    validator(course, errorstore, url_names)

    # Catch everything!
    handle_discussion_id_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

def handle_discussion_id_errors_in_10(errorstore):
    assert_error(errorstore, DuplicateID, 'course/mycourseurl.xml', "The <discussion: 'Here's a discussion' (no url_name)> tag and the <discussion: 'Here's a discussion' (no url_name)> tag both use the same discussion id: Me")

def test_link_checkking():
    """Checks for broken internal links"""
    # Perform all steps on course 10 up to validation steps
    course, errorstore, url_names = validate("testcourses/testcourse10", 6)
    handle_general_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

    # Check the link-finding routines

    # Check the discussion IDs
    validator = CheckLinks()
    validator(course, errorstore, url_names)

    # Catch everything!
    handle_link_errors_in_10(errorstore)
    assert_caught_all_errors(errorstore)

def handle_link_errors_in_10(errorstore):
    pass
