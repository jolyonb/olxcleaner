"""
html.py

Object description for an OLX html tag
"""
from edx_xml_clean.objects.common import EdxContent

class EdxHtml(EdxContent):
    """edX html object"""
    type = "html"
    html_content = False  # Was the content set by slurping up an HTML file directly?
    # If True, content does not contain the wrapping html tag
    display_name = True

    def validate(self, errorstore):
        """
        Perform validation on this object.

        :param errorstore: An ErrorStore object to which errors should be reported
        :return: None
        """
        # TODO: Perform validation
        pass
