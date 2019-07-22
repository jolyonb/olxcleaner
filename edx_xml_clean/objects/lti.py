"""
lti.py

Object description for an OLX lti tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxLti(EdxObject):
    """edX lti object (obsolete)"""
    type = "lti"
    depth = 4
    can_be_empty = True
    display_name = True

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # TODO: Perform validation
        pass
