"""
objects subpackage

Contains classes to describe various edX objects

Note that each edX object has its own file

Use the EdxCourse.get_object method to create objects of appropriate tags
"""
from edx_xml_clean.objects.common import EdxObject
from edx_xml_clean.objects.chapter import EdxChapter
from edx_xml_clean.objects.course import EdxCourse
from edx_xml_clean.objects.discussion import EdxDiscussion
from edx_xml_clean.objects.html import EdxHtml
from edx_xml_clean.objects.lti import EdxLti
from edx_xml_clean.objects.lti_consumer import EdxLtiConsumer
from edx_xml_clean.objects.problem import EdxProblem
from edx_xml_clean.objects.sequential import EdxSequential
from edx_xml_clean.objects.vertical import EdxVertical
from edx_xml_clean.objects.video import EdxVideo
from edx_xml_clean.objects.draganddropv2 import EdxDragAndDropV2
