"""
testload.py

Tests for XML course loading
"""
from edx_xml_clean.loader.xml import load_course
from edx_xml_clean.errorstore import ErrorStore
from edx_xml_clean.loader.xml_exceptions import (
    CourseXMLDoesNotExist,
    InvalidXML,
    CourseXMLName,
    TagMismatch,
    SelfPointer,
    FileDoesNotExist,
    NonFlatURLName,
    NonFlatFilename,
    InvalidPointer,
    UnexpectedTag,
    InvalidHTML,
    ExtraURLName,
    UnexpectedContent,
    EmptyTag,
    PossiblePointer
)

def test_no_course():
    errorstore = ErrorStore()
    course = load_course("testcourses", "nocourse.xml", errorstore, True)
    assert len(errorstore.errors) == 1
    assert isinstance(errorstore.errors[0], CourseXMLDoesNotExist)
    assert errorstore.errors[0].filename == "testcourses/testcourse1/nocourse.xml"

def test_course1():
    errorstore = ErrorStore()
    course = load_course("testcourses/testcourse1", "course.xml", errorstore, True)
    assert errorstore.errors == []
