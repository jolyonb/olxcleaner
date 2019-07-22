"""
sequential.py

Object description for an OLX sequential tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxSequential(EdxObject):
    """edX sequential object"""
    type = "sequential"
    depth = 2
    display_name = True

    @property
    def allowed_children(self):
        return ['vertical']

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # TODO: Perform validation
        pass
