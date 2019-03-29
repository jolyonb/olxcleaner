"""
lti.py

Object description for an OLX lti tag
"""
from loader.objects.common import EdxObject

class EdxLti(EdxObject):
    """edX lti object (obsolete)"""
    type = "lti"
    depth = 4
    obsolete_msg = "<lti> entries are obsolete and should be replaced by <lti_consumer>"
    can_be_empty = True
    display_name = True

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        pass
