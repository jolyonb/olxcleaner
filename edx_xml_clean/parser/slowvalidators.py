"""
slowvalidators.py

Validation routines that act on the course as a whole,
but may require significant time to carry out
"""
from edx_xml_clean.objects import EdxDragAndDropV2
from edx_xml_clean.parser.validators import GlobalValidator
from edx_xml_clean.utils import traverse

class SlowValidator(GlobalValidator):
    """Abstract base class for time-consuming validators"""

class CheckLinks(SlowValidator):
    """Searches the course for broken internal links (including static links)"""

    def __call__(self, course, errorstore, url_names):
        for edxobj in traverse(course):
            if edxobj.content_store:
                links = find_links(edxobj)
            elif isinstance(edxobj, EdxDragAndDropV2):
                pass
            # Check all internal links (/static/, /course/, /jump_to_id) appearing in xml attributes
            # Links can appear in: link, src, href, img, icon, special dataness for dndv2

def find_links(edxobj):
    """Find all internal links in the given object"""
    return []
