"""
chapter.py

Object description for an OLX chapter tag
"""
from loader.objects.common import EdxObject

class EdxChapter(EdxObject):
    """edX chapter object"""
    type = 'chapter'
    depth = 1
    display_name = True

    @property
    def allowed_children(self):
        return ['sequential']

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
