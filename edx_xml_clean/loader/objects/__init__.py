"""
objects subpackage

Contains classes to describe various edX objects

Note that each edX object has its own file

Use the EdxCourse.get_object method to create objects
of appropriate tags
"""
from edx_xml_clean.loader.objects.common import EdxObject
from edx_xml_clean.loader.objects.chapter import EdxChapter
from edx_xml_clean.loader.objects.course import EdxCourse
from edx_xml_clean.loader.objects.discussion import EdxDiscussion
from edx_xml_clean.loader.objects.html import EdxHtml
from edx_xml_clean.loader.objects.lti import EdxLti
from edx_xml_clean.loader.objects.lti_consumer import EdxLtiConsumer
from edx_xml_clean.loader.objects.problem import EdxProblem
from edx_xml_clean.loader.objects.sequential import EdxSequential
from edx_xml_clean.loader.objects.vertical import EdxVertical
from edx_xml_clean.loader.objects.video import EdxVideo

__all__ = ["EdxObject"]
