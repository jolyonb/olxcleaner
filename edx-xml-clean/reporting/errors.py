# -*- coding: utf-8 -*-
"""
errors.py

Routines to report on errors found in a course
"""
from errors.errors import ErrorLevel

def report_errors(errorstore):
    """Gives a simple report of all errors that were found"""
    if errorstore.errors:
        for error in errorstore.errors:
            print(f"{error.level} ({error.filename}): {error.description} ({error.name})")

def report_summary(errorstore):
    """Reports summary statistics on the errors found"""
    print("Summary:")
    counter = errorstore.summary()
    for level in ErrorLevel:
        if level.name in counter:
            print(f"{level.name}s: {counter[level.name]}")
    if not counter:
        print("No errors found!")
