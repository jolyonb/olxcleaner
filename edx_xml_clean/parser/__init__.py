# -*- coding: utf-8 -*-
"""
parser submodule

Handles global error sleuthing
"""
from edx_xml_clean.parser.parser import (
    find_url_names,
    check_display_names,
    merge_policy,
    validate_grading_policy
)

checkers = [
    check_display_names
]
