"""
video.py

Object description for an OLX video tag
"""
from edx_xml_clean.objects.common import EdxContent

class EdxVideo(EdxContent):
    """edX video object"""
    type = "video"
    can_be_empty = True
    display_name = True

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
