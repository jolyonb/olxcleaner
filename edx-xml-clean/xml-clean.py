#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xml-clean.py

A validator for XML edX courses
"""
from edxloader import load_course
from output import print_tree

# Point to a course
working = "../course/course.xml"

# Load the course
course = load_course(working)

# Print the structure
print_tree(course, 2)
