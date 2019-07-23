# edx-xml-clean

[![Build Status](https://api.travis-ci.org/jolyonb/edx-xml-clean.svg?branch=master)](https://travis-ci.org/jolyonb/edx-xml-clean) [![Coverage Status](https://codecov.io/gh/jolyonb/edx-xml-clean/branch/master/graphs/badge.svg)](https://codecov.io/gh/jolyonb/edx-xml-clean)

Validates the XML code for an edX course, reporting errors found and statistics.

Version 0.1.0

Copyright (C) 2018-2019 Jolyon Bloomfield

## Links

* [Error Listing](errors.md)
* [Wishlist](wishlist.md)
* [Vision](vision.md)
* [Changelog](changelog.md)
* [License](LICENSE)

## Requirements

This code uses features of python 3.6. We recommend installing a virtual environment, and running `pip install -r requirements.txt`. Afterwards, tests may be run by running `pytest`.

## Installation

Currently, you need to clone the repository, as no installer is provided.

## edx-cleaner Usage

Used to validate OLX (edX XML) code. This is a very light wrapper around the edx_xml_cleaner library, but exposes all of the functionality thereof.

Run the file `./edx-cleaner.py` with the following command line options:

```text
./edx-cleaner.py [-h] 
                 [-c COURSE]
                 [-p {1,2,3,4,5,6,7,8}] 
                 [-t TREE] [-l {0,1,2,3,4}]
                 [-q] [-e] [-s] [-S]
                 [-f {0,1,2,3,4}]
                 [-i IGNORE [IGNORE ...]]
```

* `-h`: Display help.
* `-c`: Specify the course file to analyze. If not specified, looks for `course.xml` in the current directory. If given a directory, looks for `course.xml` in that directory.
* `-p`: Specify the validation level you wish analyze the course at:
  * 1: Load the course
  * 2: Load the policy and grading policy
  * 3: Validate url_names
  * 4: Merge policy data with course, ensuring that all references are valid
  * 5: Validate the grading policy
  * 6: Have every object validate itself
  * 7: Parse the course for global errors
  * 8: Parse the course for detailed global errors (default)
* `-t TREE`: Specify a file to output the tree structure to.
* `-l`: Specify the depth level to output the tree structure to. Only used if the `-t` option is set. 0 = Course, 1 = Chapter, 2 = Sequential, 3 = Vertical, 4 = Content. 
* `-q`: Quiet mode. Does not output anything to the screen.
* `-e`: Suppress error listing. Implied by `-q`.
* `-s`: Suppress summary of errors. Implied by `-q`.
* `-S`: Suppress course statistics. Implied by `-q`.
* `-f`: Select the error level at which to exit with an error code. 0 = DEBUG, 1 = INFO, 2 = WARNING, 3 = ERROR (default), 4 = NEVER. Exit code is set to `1` if an error at the specified level or higher is present.
* `-i`: Specify a space-separated list of error names to ignore. See [Error Listing](errors.md).

## edx-reporter Usage

The edx_xml_clean library includes modules that parse a course into python objects. This can be useful if you want to scan a course to generate a report. We exploit this in `edx-reporter.py` to generate LaTeX reports of course structure.

Run the file `./edx-reporter.py` with the following command line options:

```text
./edx-reporter.py [-h] 
                  [-c COURSE]
                  [> latexfile.tex]
```

* `-h`: Display help.
* `-c`: Specify the course file to analyze. If not specified, looks for `course.xml` in the current directory. If given a directory, looks for `course.xml` in that directory.
* `> latexfile.tex`: Output the report to a file using a bash pipe.
