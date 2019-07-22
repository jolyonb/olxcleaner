"""
longvalidators.py

Validation routines that act on the course as a whole,
but may require significant time to carry out
"""
from edx_xml_clean.parser.validators import GlobalValidator
# from edx_xml_clean.utils import traverse
# from edx_xml_clean.parser.parser_exceptions import ...

class LongValidator(GlobalValidator):
    """Abstract base class for time-consuming validators"""

# class Example(LongValidator):
#     """Example LongValidator"""
#
#     def __call__(self, course, errorstore, url_names):
#         pass
