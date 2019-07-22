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

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # Video XML is such a mess, I'm not even going to try parsing it.
        pass
