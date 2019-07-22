"""
draganddropv2.py

Object description for the "new" drag and drop interface
"""
from edx_xml_clean.objects.common import EdxContent

class EdxDragAndDropV2(EdxContent):
    """edX drag-and-drop-v2 object"""
    type = "drag-and-drop-v2"
    display_name = False
    can_be_pointer = False
    can_be_empty = True
    depth = 4

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # There is nothing to validate here; this Xblock isn't exported in OLX :-(
        pass
