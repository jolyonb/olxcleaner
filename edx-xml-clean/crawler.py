#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edX XML Cleaner - Crawler example

Given that we have tools to load a course into memory, we can
now crawl courses and construct reports based on it. This is an
example script that does so, outputting a LaTeX file
tailored to a specific course format.
"""
import sys
import argparse
import datetime
import re
from loader.xml import load_course
from errors.errorstore import ErrorStore

def handle_arguments():
    """Look after all command-line arguments"""
    parser = argparse.ArgumentParser(description="edX XML cleaner -- Crawler example")

    # Required arguments
    # Location of course.xml
    parser.add_argument("-c", "--course", help="Location of course.xml (default=./course.xml)", default="course.xml")

    # Parse the command line
    return parser.parse_args()

# Read the command line arguments
args = handle_arguments()

# Load the course
course = load_course(args.course, ErrorStore([]), True)

# Make sure we have a course to crawl
if not course:
    print("Cannot load course - aborting")
    sys.exit(0)

# Crawl the course looking for lectures and problem sets
objects = []
contents = []
for chapter in course.children:
    for seq in chapter.children:
        if seq.attributes["display_name"].startswith("Lecture"):
            objects.append(seq.attributes["display_name"])
            contents.append([])
            duration = datetime.timedelta()
            for vert in seq.children:
                for entry in vert.children:
                    if entry.type == "video":
                        vidname = entry.attributes["display_name"]
                        contents[-1].append(entry.attributes["url_name"] + ": " + vidname)
                        length = re.search(r'\(([0-9]+):([0-9]+)\)', vidname)
                        if length:
                            minutes = int(length.group(1))
                            seconds = int(length.group(2))
                            duration += datetime.timedelta(minutes=minutes, seconds=seconds)
                    elif entry.type == "problem":
                        contents[-1].append((entry.attributes["url_name"] + ": " + entry.attributes["display_name"], ))
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            if hours == 0:
                objects[-1] += f" ({minutes}:{seconds:02})"
            else:
                objects[-1] += f" ({hours}:{minutes:02}:{seconds:02})"
        elif seq.attributes["display_name"].startswith("Problem"):
            objects.append(seq.attributes["display_name"])
            contents.append([])
            for vert in seq.children:
                contents[-1].append(vert.attributes["url_name"][2:] + ": " + vert.attributes["display_name"])

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

\title{Overview of 8.06x Content}

\date{}

\maketitle

\vspace{-1.5cm}

Each page represents one week of material.

"""
footer = r"""
\end{document}"""

lecturetemplate = r"""\section*{}

\begin{itemize}
    \item Video
\end{itemize}

"""

def sanitize(text):
    results = text.replace("p^2", "$p^2$").replace("p^4", "$p^4$")
    results = results.replace(' "', ' ``')
    results = results.replace('"', "''")
    results = results.replace('ö', r'\"o')
    results = results.replace('S_z', '$\hat{S}_z$')
    return results

print(header)
needsnewpage = False
for idx, item in enumerate(objects):

    if needsnewpage:
        needsnewpage = False
        print()
        print(r"\newpage")

    if idx > 0:
        print()

    if item.startswith("Problem"):
        print(r"\newpage")
        print()

    print(r"\section*{" + item + "}\n")
    print(r"\begin{itemize}")

    indented = False
    for entry in contents[idx]:
        if isinstance(entry, tuple):
            if not indented:
                indented = True
                print(r"\begin{itemize}")
            print(r"\item " + sanitize(entry[0]))
        else:
            if indented:
                print(r"\end{itemize}")
                indented = False
            print(r"\item " + sanitize(entry))
    if indented:
        print(r"\end{itemize}")

    print(r"\end{itemize}")

    if item.startswith("Problem"):
        needsnewpage = True

print(footer)
