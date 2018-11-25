# -*- coding: utf-8 -*-
"""
utils.py

Routines to assist with loading files
"""
import os

def file_exists(filename):
    """Returns True if filename exists, or False if not"""
    if os.path.isfile(filename):
        return True
    return False
