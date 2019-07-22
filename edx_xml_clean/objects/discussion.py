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
    display_name = 'optional'

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # Check for obsolete invocation
        # Check for attributes: discussion_id, discussion_category, discussion_target
        # TODO: Perform validation
        pass
