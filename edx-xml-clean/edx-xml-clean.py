#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edX XML Cleaner

A validator for XML edX courses
Copyright (C) 2018 Jolyon Bloomfield

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import os
import argparse
from __version__ import version
from errors.errorstore import ErrorStore
from loader.xml import load_course
from reporting.structure import write_tree
from reporting.errors import report_errors, report_summary

def handle_arguments():
    """Look after all command-line arguments"""
    parser = argparse.ArgumentParser(description="edX XML cleaner -- A validator for XML edX courses")

    # Required arguments
    # Location of course.xml
    parser.add_argument("-c", "--course", help="Location of course.xml (default=./course.xml)", default="course.xml")

    # Optional arguments
    # Output file for structure
    parser.add_argument("-t", "--tree", help="File to output course structure to")

    # Level to output structure to
    parser.add_argument("-l", "--level", help="Depth level to output structure to",
                        default=4, choices=[0, 1, 2, 3, 4], type=int)

    # Quiet mode
    parser.add_argument("-q", "--quiet", help="Quiet mode (no screen output)", action="store_true")

    # Error output
    parser.add_argument("-e", "--noerrors", help="Suppress error output", action="store_true")

    # Error summary
    parser.add_argument("-s", "--nosummary", help="Suppress error summary", action="store_true")

    # Failure level
    parser.add_argument("-f", "--failure", default=3, choices=[0, 1, 2, 3, 4], type=int,
                        help="Level of errors at which to declare failure: 0=DEBUG, 1=INFO, 2=WARNING, 3=ERROR (default), 4=NEVER")

    # Ignore list
    parser.add_argument('-i', '--ignore', nargs='+', help='List of errors to ignore')

    # Parse the command line
    return parser.parse_args()

# Read the command line arguments
args = handle_arguments()

if not args.quiet:
    print(f'edX XML cleaner {version} -- A validator for XML edX courses')

# Save current directory
current_dir = os.getcwd()

# Construct the error store
errorstore = ErrorStore(args.ignore)

# Load the course
course = load_course(args.course, errorstore, args.quiet)

# Report any errors that were found
if not args.quiet:
    if not args.noerrors:
        report_errors(errorstore)
    if not args.nosummary:
        report_summary(errorstore)

# Output the structure to file
if args.tree and course is not None:
    if not args.quiet:
        print(f"Writing structure to {args.tree}")
    os.chdir(current_dir)
    write_tree(course, args.tree, args.level)

# Exit with the appropriate error level
if errorstore.return_error(args.failure):
    sys.exit(1)
else:
    sys.exit(0)
