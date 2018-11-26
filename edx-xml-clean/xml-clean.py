#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xml-clean.py

A validator for XML edX courses
"""
from errors.errorstore import ErrorStore
from loader.xml import load_course
from reporting.structure import print_tree
from reporting.errors import report_errors

# Point to a course
working = "../course/course.xml"

# TODO: Implement argparse for filename loading and options

# Construct the error store
errorstore = ErrorStore()

# Load the course
course = load_course(working, errorstore)

# Print the structure
print_tree(course)

# Report any errors that were found
report_errors(errorstore)

vert = course.children[0].children[0].children[0]

for child in vert.children:
    print(child.content)
