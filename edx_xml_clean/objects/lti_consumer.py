"""
lti_consumer.py

Object description for an OLX lti_consumer tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxLtiConsumer(EdxObject):
    """edX lti_consumer object"""
    can_be_pointer = False
    type = "lti_consumer"
    depth = 4
    can_be_empty = True
    display_name = True

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
