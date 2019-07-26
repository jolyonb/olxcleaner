# -*- coding: utf-8 -*-
"""
setup.py

Contains setup information for the olxcleaner library.
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="olxcleaner",
    version="0.1.0",
    author="Jolyon Bloomfield",
    author_email="jolyon@mit.edu",
    description="Tool to validate edX XML courses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jolyonb/olxcleaner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
