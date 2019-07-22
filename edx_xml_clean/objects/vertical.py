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

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # TODO: Perform validation
        pass
