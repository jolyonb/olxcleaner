# edx-xml-clean

Validates the XML code for an edX course

Version 0.0.1

Copyright (C) 2018 Jolyon Bloomfield

## Links

* [Error Listing](errors.md)
* [Wishlist](wishlist.md)
* [License](LICENSE)

## Requirements

This code uses features of python 3.6.

## Usage

Currently, you need to clone the repository; no installer is provided.

Run the file `./edx-xml-clean/edx-xml-clean.py` with the following command line options:

```bash
./edx-xml-clean.py [-h] 
                   [-c COURSE] 
                   [-t TREE] [-l {0,1,2,3,4}]
                   [-q] [-e] [-s] 
                   [-f {0,1,2,3,4}]
                   [-i IGNORE [IGNORE ...]]
```

* `-h`: Display help.
* `-c`: Specify the course file to analyze. If not specified, looks for `course.xml` in the current directory. If given a directory, looks for `course.xml` in that directory.
* `-t TREE`: Specify a file to output the tree structure to.
* `-l`: Specify the depth level to output the tree structure to. Only used if the `-t` option is set. 0 = Course, 1 = Chapter, 2 = Sequential, 3 = Vertical, 4 = Content. 
* `-q`: Quiet mode. Does not output anything to the screen.
* `-e`: Suppress error listing. Implied by `-q`.
* `-s`: Suppress summary of errors. Implied by `-q`.
* `-f`: Select the error level at which to exit with an error code. 0 = DEBUG, 1 = INFO, 2 = WARNING, 3 = ERROR (default), 4 = NEVER. Exit code is set to `1` if an error at the specified level or higher is present.
* `-i`: Specify a space-separated list of error names to ignore. See [Error Listing](errors.md).
