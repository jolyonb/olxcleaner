"""
discussion.py

Object description for an OLX discussion tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxDiscussion(EdxObject):
    """edX discussion object"""
    type = "discussion"
    depth = 4
    can_be_empty = True
    needs_url_name = False

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
