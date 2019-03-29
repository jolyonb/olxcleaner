"""
objects subpackage

Contains classes to describe various edX objects

Note that each edX object has its own file

Use the EdxCourse.get_object method to create objects
of appropriate tags
"""
from loader.objects.common import EdxObject
from loader.objects.chapter import EdxChapter
from loader.objects.course import EdxCourse
from loader.objects.discussion import EdxDiscussion
from loader.objects.html import EdxHtml
from loader.objects.lti import EdxLti
from loader.objects.lti_consumer import EdxLtiConsumer
from loader.objects.problem import EdxProblem
from loader.objects.sequential import EdxSequential
from loader.objects.vertical import EdxVertical
from loader.objects.video import EdxVideo

__all__ = ["EdxObject"]
