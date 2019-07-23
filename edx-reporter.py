#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edx-reporter.py

This script crawls through a course and produces a LaTeX document
containing the course structure. Note that this script assumes
that your course is error free.

Recommended usage:
edx-reporter.py > report.tex
"""
import sys
import argparse
import datetime
import re

from edx_xml_clean import validate

def handle_arguments():
    """Look after all command-line arguments"""
    parser = argparse.ArgumentParser(description="edX XML Reporter")

    # Required arguments
    # Location of course.xml
    parser.add_argument("-c", "--course", help="Location of course.xml (default=./course.xml)", default="course.xml")

    # Parse the command line
    return parser.parse_args()

# Read the command line arguments
args = handle_arguments()

# Load the course
# We only need the XML structure, no policy or property information, so use steps=1
course, _, url_names = validate(args.course, steps=1)

# Make sure we have a course to crawl
if not course:
    print("Cannot load course - aborting")
    sys.exit(0)

# Here's the header of the LaTeX file we'll produce
header = r"""\documentclass{article}

\usepackage[english]{babel}
\usepackage{helvet}
\usepackage{microtype}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[landscape,twocolumn]{geometry}
\usepackage{fullpage}

\special{papersize=8.5in,11in}
\setlength{\pdfpageheight}{\paperheight}
\setlength{\pdfpagewidth}{\paperwidth}

\parskip = 1mm

\titleformat*{\section}{\large\bfseries\raggedright}
\setlist{topsep=0pt}

\begin{document}

\title{Overview of Course Content}

\date{}

\maketitle

\vspace{-1.5cm}

Each page represents one chapter of material.

"""

# And here's the footer
footer = r"""
\end{document}"""

# Crawl the course extracting the desired information
chapters = []
for chapter in course.children:
    chapter_log = {'title': chapter.attributes["display_name"], 'sequentials': []}

    for seq in chapter.children:
        seq_log = {'title': seq.attributes["display_name"], 'verticals': []}

        # Total up the duration of all videos in the sequential
        duration = datetime.timedelta()
        for vert in seq.children:
            seq_log['verticals'].append(vert.attributes["display_name"])

            for entry in vert.children:
                if entry.type == "video":
                    # Search for a duration at the end of a video name of the form "(mins:seconds)"
                    length = re.search(r'\(([0-9]+):([0-9]+)\)', entry.attributes["display_name"])
                    if length:
                        minutes = int(length.group(1))
                        seconds = int(length.group(2))
                        duration += datetime.timedelta(minutes=minutes, seconds=seconds)

        if duration.total_seconds() > 0:
            # Report the total time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            if hours == 0:
                seq_log['title'] += f" ({minutes}:{seconds:02})"
            else:
                seq_log['title'] += f" ({hours}:{minutes:02}:{seconds:02})"

        chapter_log['sequentials'].append(seq_log)
    chapters.append(chapter_log)

def sanitize(text):
    """
    This is a helper function that should be used to sanitize text for LaTeX output.
    You'll probably need to edit the LaTeX slightly afterwards, but it should look pretty good!
    """
    # Fix quotation marks
    results = text.replace(' "', ' ``')
    results = results.replace('"', "''")
    # Example of fixing unicode
    results = results.replace('ö', r'\"o')
    return results

# Now do the output
print(header)

# Iterate over the content
needsnewpage = False
for chapter in chapters:

    # Each chapter should be on its own page
    if needsnewpage:
        print("\n" + r"\newpage" + "\n")

    print(r"\section*{" + sanitize(chapter['title']) + "}")

    for sequential in chapter['sequentials']:
        print("\n" + r"\section*{" + sanitize(sequential['title']) + "}\n")
        print(r"\begin{itemize}")

        for vertical in sequential['verticals']:
            print(r"\item " + sanitize(vertical))

        print(r"\end{itemize}")

    needsnewpage = True

print(footer)
