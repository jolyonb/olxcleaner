"""
test_reporting.py

Test the reporting routines by running them over the test courses
"""
from edx_xml_clean.validate import validate
from edx_xml_clean.reporting import (construct_tree,
                                     report_statistics,
                                     report_error_summary,
                                     report_errors)

def test_construct_tree():
    course, _, _ = validate("testcourses/testcourse1")
    tree = construct_tree(course)
    assert tree == ["<course url_name='mycourseurl'>",
                    "    <chapter url_name='chapter' display_name='chapter name'>",
                    "        <sequential url_name='sequential' display_name='display name'>",
                    "            <vertical url_name='vertical' display_name='vertical name'>",
                    "                <html url_name='html' display_name='html name'>"]

    course, _, _ = validate("testcourses/testcourse1")
    tree = construct_tree(course, maxdepth=2)
    assert tree == ["<course url_name='mycourseurl'>",
                    "    <chapter url_name='chapter' display_name='chapter name'>",
                    "        <sequential url_name='sequential' display_name='display name'>"]

    course, _, _ = validate("testcourses/testcourse9")
    tree = construct_tree(course)
    assert tree == ["<course url_name='mycourseurl'>",
                    "    <chapter url_name='chapter' display_name='Hi there!'>",
                    "        <sequential url_name='sequential' display_name='Hi there!'>",
                    "            <vertical url_name='vertical' display_name='Hi mom!'>",
                    "                <html url_name='html'>",
                    "                <problem url_name='problem'>",
                    "                <video url_name='video1'>",
                    "                <video url_name='video2'>",
                    "                <discussion url_name='discussion'>",
                    "                <discussion url_name='Meep' display_name='Something here'>",
                    "                <lti url_name='lti'>",
                    "                <lti_consumer url_name='meep'>",
                    "                <problem display_name='no url_name'>",
                    "                <drag-and-drop-v2 url_name='studio_mess' display_name='This is my title'>",
                    "                <drag-and-drop-v2 url_name='studio_mess2' display_name='This is my title'>",
                    "                <drag-and-drop-v2 url_name='studio_mess3' display_name='This is my title'>",
                    "                <drag-and-drop-v2 url_name='studio_mess4'>",
                    "            <vertical url_name='oravert' display_name='ORA Vertical'>",
                    "                <openassessment url_name='paper-draft'>",
                    "        <sequential url_name='examseq' display_name='Exam'>",
                    "            <vertical url_name='v-exam'>",
                    "                <problem url_name='examproblem'>"]

def test_report_errors():
    course, errorstore, _ = validate("testcourses/testcourse1")
    errors = report_errors(errorstore)
    assert errors == ["ERROR (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> does not have the required setting 'course_image'. (InvalidSetting)",
                      "ERROR (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> does not have the required setting 'end'. (InvalidSetting)",
                      "ERROR (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> does not have the required setting 'start'. (InvalidSetting)",
                      "WARNING (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> is missing the display_name attribute. (MissingDisplayName)",
                      "ERROR (policies/mycourseurl/grading_policy.json): The policy file 'policies/mycourseurl/grading_policy.json' was not found. (PolicyNotFound)",
                      "ERROR (policies/mycourseurl/policy.json): The policy file 'policies/mycourseurl/policy.json' was not found. (PolicyNotFound)"]

    course, errorstore, _ = validate("testcourses/testcourse9")
    errors = report_errors(errorstore)
    assert errors == ["ERROR (chapter/chapter.xml): The tag <chapter url_name='chapter' display_name='Hi there!'> has an invalid date setting for start: 'Feb 20, 2019, 17:00zzz'. (InvalidSetting)",
                      "ERROR (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> should have a positive number of attempts. (InvalidSetting)",
                      'ERROR (course/mycourseurl.xml): Unable to recognize graceperiod format in policy. (InvalidSetting)',
                      "WARNING (course/mycourseurl.xml): The <course url_name='mycourseurl'> tag contains a reference to a missing static file: course_image_small.jpg (MissingFile)",
                      "WARNING (course/mycourseurl.xml): The tag <course url_name='mycourseurl'> is missing the display_name attribute. (MissingDisplayName)",
                      "ERROR (discussion/discussion.xml): The tag <discussion url_name='discussion'> does not have the required setting 'discussion_category'. (InvalidSetting)",
                      "ERROR (discussion/discussion.xml): The tag <discussion url_name='discussion'> does not have the required setting 'discussion_id'. (InvalidSetting)",
                      "ERROR (discussion/discussion.xml): The tag <discussion url_name='discussion'> does not have the required setting 'discussion_target'. (InvalidSetting)",
                      "WARNING (html/html.xml): The tag <html url_name='html'> is missing the display_name attribute. (MissingDisplayName)",
                      "ERROR (lti/lti.xml): Course policy does not include an 'lti_passports' entry for 'nothere', required for <lti url_name='lti'>. (LTIError)",
                      "ERROR (lti/lti.xml): Course policy does not include the 'lti' advanced module, required for <lti url_name='lti'>. (LTIError)",
                      "ERROR (lti/lti.xml): The tag <lti url_name='lti'> does not have the required setting 'launch_url'. (InvalidSetting)",
                      "INFO (lti/lti.xml): The tag <lti url_name='lti'> should be converted to the newer lti_consumer Xblock. (Obsolete)",
                      "WARNING (lti/lti.xml): The tag <lti url_name='lti'> is missing the display_name attribute. (MissingDisplayName)",
                      "ERROR (problem/problem.xml): The tag <problem url_name='problem'> has a negative problem weight. (InvalidSetting)",
                      "ERROR (problem/problem.xml): The tag <problem url_name='problem'> has an invalid setting 'showanswer=bad'. (InvalidSetting)",
                      "ERROR (problem/problem.xml): The tag <problem url_name='problem'> should have a positive number of attempts. (InvalidSetting)",
                      "WARNING (problem/problem.xml): The tag <problem url_name='problem'> has a date out of order: start date must be before due date (DateOrdering)",
                      "WARNING (problem/problem.xml): The tag <problem url_name='problem'> is missing the display_name attribute. (MissingDisplayName)",
                      "ERROR (sequential/examseq.xml): The tag <sequential url_name='examseq' display_name='Exam'> is a timed exam, but the course policy does not have 'enable_timed_exams=true'. (InvalidSetting)",
                      "WARNING (sequential/examseq.xml): The tag <problem url_name='examproblem'> is missing the display_name attribute. (MissingDisplayName)",
                      "WARNING (sequential/examseq.xml): The tag <vertical url_name='v-exam'> is missing the display_name attribute. (MissingDisplayName)",
                      "WARNING (sequential/sequential.xml): The tag <sequential url_name='sequential' display_name='Hi there!'> has a date out of order: start date cannot be before course start date (DateOrdering)",
                      "WARNING (vertical/oravert.xml): The tag <openassessment url_name='paper-draft'> has a date out of order: assessment 1 due date must be before course end date (DateOrdering)",
                      "ERROR (vertical/vertical.xml): Course policy does not include an 'lti_passports' entry for 'nothere', required for <lti_consumer url_name='meep'>. (LTIError)",
                      "ERROR (vertical/vertical.xml): Course policy does not include the 'lti_consumer' advanced module, required for <lti_consumer url_name='meep'>. (LTIError)",
                      "ERROR (vertical/vertical.xml): The tag <drag-and-drop-v2 url_name='studio_mess2' display_name='This is my title'> has an error in the data JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1). (InvalidSetting)",
                      "ERROR (vertical/vertical.xml): The tag <drag-and-drop-v2 url_name='studio_mess3' display_name='This is my title'> data JSON is not a dictionary. (InvalidSetting)",
                      "ERROR (vertical/vertical.xml): The tag <lti_consumer url_name='meep'> does not have the required setting 'launch_url'. (InvalidSetting)",
                      "ERROR (vertical/vertical.xml): The tag <problem display_name='no url_name'> has an invalid setting 'showanswer=hah!'. (InvalidSetting)",
                      "INFO (vertical/vertical.xml): The tag <discussion url_name='discussion'> should be included inline rather than through the discussion directory. (Obsolete)",
                      "WARNING (vertical/vertical.xml): The <drag-and-drop-v2 url_name='studio_mess' display_name='This is my title'> tag contains a reference to a missing static file: /static/ex34_dnd.png (MissingFile)",
                      "WARNING (vertical/vertical.xml): The <drag-and-drop-v2 url_name='studio_mess' display_name='This is my title'> tag contains a reference to a missing static file: /static/ex34_dnd_label1.png (MissingFile)",
                      "WARNING (vertical/vertical.xml): The <drag-and-drop-v2 url_name='studio_mess' display_name='This is my title'> tag contains a reference to a missing static file: /static/ex34_dnd_label2.png (MissingFile)",
                      "WARNING (vertical/vertical.xml): The tag <lti_consumer url_name='meep'> is missing the display_name attribute. (MissingDisplayName)",
                      "WARNING (vertical/vertical.xml): The tag <problem display_name='no url_name'> has a date out of order: due date must be before course end date (DateOrdering)",
                      "WARNING (vertical/vertical.xml): The tag <problem display_name='no url_name'> has no url_name. (MissingURLName)",
                      "WARNING (vertical/vertical.xml): The tag <vertical url_name='vertical' display_name='Hi mom!'> has a date out of order: due date must be before course end date (DateOrdering)",
                      "WARNING (video/video1.xml): The tag <video url_name='video1'> is missing the display_name attribute. (MissingDisplayName)",
                      "WARNING (video/video2.xml): The tag <video url_name='video2'> is missing the display_name attribute. (MissingDisplayName)"]

def test_report_error_summary():
    course, errorstore, _ = validate("testcourses/testcourse1")
    summary = report_error_summary(errorstore)

    assert summary == ['Summary:',
                       'WARNINGs: 1',
                       '    MissingDisplayName: 1',
                       'ERRORs: 5',
                       '    PolicyNotFound: 2',
                       '    InvalidSetting: 3']

    course, errorstore, _ = validate("testcourses/testcourse9")
    summary = report_error_summary(errorstore)

    assert summary == ['Summary:',
                       'INFOs: 2',
                       '    Obsolete: 2',
                       'WARNINGs: 19',
                       '    MissingURLName: 1',
                       '    MissingFile: 4',
                       '    DateOrdering: 5',
                       '    MissingDisplayName: 9',
                       'ERRORs: 19',
                       '    InvalidSetting: 15',
                       '    LTIError: 4']

def test_report_statistics():
    course, _, _ = validate("testcourses/testcourse1")
    summary = report_statistics(course)

    assert summary == ['Number of each type of object:',
                       '  - course: 1',
                       '  - chapter: 1',
                       '  - sequential: 1',
                       '  - vertical: 1',
                       '  - html: 1',
                       'Number of exams: 0']

    course, _, _ = validate("testcourses/testcourse10")
    summary = report_statistics(course)

    assert summary == ['Number of each type of object:',
                       '  - course: 1',
                       '  - chapter: 1',
                       '  - sequential: 1',
                       '  - vertical: 4',
                       '  - html: 2',
                       '  - discussion: 2',
                       '  - openassessment: 1',
                       '  - problem: 1',
                       '  - drag-and-drop-v2: 1',
                       'Number of exams: 0',
                       'Problem statistics:',
                       '    Number of problems: 1',
                       '    Number of problems with solutions: 1',
                       '    Number of problems with python scripts: 0',
                       '    response_types used*:',
                       '      - customresponse: 1',
                       '    input_types used*:',
                       '      - drag_and_drop_input: 1',
                       '    * Multiple uses within a single problem only count once']

    course, _, _ = validate("testcourses/testcourse9")
    summary = report_statistics(course)

    assert summary == ['Number of each type of object:',
                       '  - course: 1',
                       '  - chapter: 1',
                       '  - sequential: 2',
                       '  - vertical: 3',
                       '  - html: 1',
                       '  - problem: 3',
                       '  - video: 2',
                       '  - discussion: 2',
                       '  - lti: 1',
                       '  - lti_consumer: 1',
                       '  - drag-and-drop-v2: 4',
                       '  - openassessment: 1',
                       'Number of exams: 1',
                       'Problem statistics:',
                       '    Number of problems: 3',
                       '    Number of problems with solutions: 1',
                       '    Number of problems with python scripts: 1',
                       '    response_types used*:',
                       '      - customresponse: 1',
                       '      - multiplechoiceresponse: 1',
                       '    input_types used*:',
                       '      - choicegroup: 1',
                       '      - textline: 1',
                       '    * Multiple uses within a single problem only count once']

    course, _, _ = validate("testcourses/testcourse1", steps=1)
    summary = report_statistics(course)

    assert summary == ['Number of each type of object:',
                       '  - course: 1',
                       '  - chapter: 1',
                       '  - sequential: 1',
                       '  - vertical: 1',
                       '  - html: 1',
                       'Number of exams: 0']

def test_error_reporting():
    """Ensure that errorstore reports error levels correctly"""
    _, errorstore, _ = validate("testcourses/testcourse1", steps=1)
    assert not errorstore.return_error(0)
    assert not errorstore.return_error(1)
    assert not errorstore.return_error(2)
    assert not errorstore.return_error(3)
    assert not errorstore.return_error(4)

    _, errorstore, _ = validate("testcourses/testcourse1", steps=2)
    assert errorstore.return_error(0)
    assert errorstore.return_error(1)
    assert errorstore.return_error(2)
    assert errorstore.return_error(3)
    assert not errorstore.return_error(4)
