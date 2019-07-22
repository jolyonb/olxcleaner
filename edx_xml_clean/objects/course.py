"""
course.py

Object description for an OLX course tag
"""
from edx_xml_clean.objects.common import EdxObject

class EdxCourse(EdxObject):
    """edX course object"""
    type = "course"
    depth = 0

    # course pointer tags need three attributes:
    pointer_attr = {'url_name', 'course', 'org'}

    @property
    def allowed_children(self):
        return ["chapter"]

    def validate(self, course, errorstore):
        """
        Perform validation on this object.

        :param course: The course object, which may contain settings relevant to the validation of this object
        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # TODO: Perform validation
        # Check showanswer, show_correctness, rerandomize
        # Tabs (files might need to warn not parsed, use debug to warn, can validate all types, esp. textbooks!)
        # Check textbook setup, textbook links to existing files
        # Check start and end date (convert to dates for later usage)
        # Check course_image exists
        # Check enrollment_end, enrollment_start
        # Check graceperiod parcing
        # Three required properties
        pass
