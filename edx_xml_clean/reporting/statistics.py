"""
statistics.py

Generates course-wide statistics
"""
from collections import Counter
from edx_xml_clean.utils import traverse
from edx_xml_clean.objects import EdxProblem, EdxSequential

def report_statistics(course):
    """
    Report course statistics to the screen.

    :param course:
    :return: None
    """
    # Compute statistics
    typecounter, exams, response_types, input_types, python_problems, problem_solutions = construct_statistics(course)

    # Now print to screen
    print("Number of each type of object:")
    for entry in typecounter:
        print(f"  - {entry}: {typecounter[entry]}")

    print(f"Number of exams: {exams}")

    if typecounter['problem'] > 0:
        print("Problem statistics:")
        print(f"    Number of problems: {typecounter['problem']}")
        print(f"    Number of problems with solutions: {problem_solutions}")
        print(f"    Number of problems with python scripts: {python_problems}")
        print(f"    response_types used*:")
        for entry in response_types:
            print(f"      - {entry}: {response_types[entry]}")
        print(f"    input_types used*:")
        for entry in input_types:
            print(f"      - {entry}: {input_types[entry]}")
        print(f"    * Multiple uses within a single problem only count once")

def construct_statistics(course):
    """
    Compute course statistics.

    :param course: A validated course.
    :return: typecounter (dict),
             exams (int),
             response_types (dict),
             input_types (dict),
             python_problems (int),
             problem_solutions (int)
    """
    # Track how many of each type of object we have
    typecounter = Counter()

    # Track the number of sequentials that are time-limited (i.e., exams)
    exams = 0

    # Track the number of each type of response type and input type in problems
    response_types = Counter()
    input_types = Counter()

    # Track the number of problems using python scripts
    python_problems = 0

    # Track the number of problems with solutions
    problem_solutions = 0

    for edxobj in traverse(course):
        # Track the object type
        typecounter[edxobj.type] += 1

        if isinstance(edxobj, EdxSequential):
            # Check for exams
            if edxobj.is_exam:
                exams += 1

        elif isinstance(edxobj, EdxProblem):
            # Check for the 4 problem settings
            if edxobj.has_solution:
                problem_solutions += 1

            for response_type in edxobj.response_types:
                response_types[response_type] += 1

            for input_type in edxobj.input_types:
                input_types[input_type] += 1

            if 'python' in edxobj.scripts:
                python_problems += 1

    return typecounter, exams, response_types, input_types, python_problems, problem_solutions
