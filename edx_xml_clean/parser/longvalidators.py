"""
longvalidators.py

Validation routines that act on the course as a whole,
but may require significant time to carry out
"""
from abc import ABCMeta
from edx_xml_clean.parser.validators import GlobalValidator
# from edx_xml_clean.parser.parser_exceptions import ...
# from edx_xml_clean.utils import traverse

class LongValidator(GlobalValidator, metaclass=ABCMeta):
    """Abstract base class for long validators"""

# class Example(LongValidator):
#     """Example long validator"""
#
#     def __call__(self, course, errorstore, url_names):
#         pass
