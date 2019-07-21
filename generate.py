#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py

Script to generate errors.md
"""
from edx_xml_clean.exceptions import CourseError

names = ["Debug", "Information", "Warnings", "Errors"]
errors = [[], [], [], []]

for child in CourseError.__subclasses__():
    errors[child._level.value].append(f"- `{child.__name__}`: {child.__doc__}")

with open("errors.md", "w") as f:
    f.write('# Error Listing\n\n')
    f.write('Each error has a name that can be used in the `-i` flag to ignore it.\n')

    for i in range(3, -1, -1):
        f.write(f"\n## {names[i]}\n\n")
        for error in sorted(errors[i]):
            f.write(f"{error}\n\n")

print("Error listing written to errors.md")
