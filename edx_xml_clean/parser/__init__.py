# -*- coding: utf-8 -*-
"""
parser submodule

Handles global error sleuthing
"""
from edx_xml_clean.parser.parser import find_url_names, find_display_names

checkers = [
    find_display_names
]

__all__ = [
    "find_url_names",
    "checkers"
]
