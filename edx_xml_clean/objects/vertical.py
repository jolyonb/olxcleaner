"""
vertical.py

Object description for an OLX vertical tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxVertical(EdxObject):
    """edX vertical object"""
    type = "vertical"
    depth = 3
    display_name = True

    @property
    def allowed_children(self):
        return ['html',
                'video',
                'discussion',
                'problem',
                'lti',
                'lti_consumer']

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
