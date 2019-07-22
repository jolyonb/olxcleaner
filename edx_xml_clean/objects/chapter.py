"""
chapter.py

Object description for an OLX chapter tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxChapter(EdxObject):
    """edX chapter object"""
    type = 'chapter'
    depth = 1
    display_name = True

    @property
    def allowed_children(self):
        return ['sequential']

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # Check start/due dates
        # Check showanswer, show_correctness, rerandomize
        # TODO: Perform validation
        pass
