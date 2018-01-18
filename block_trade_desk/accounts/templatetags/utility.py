from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from accounts.settings import WIDGET_TO_TEMPLATE_MAP

register = template.Library()


@register.assignment_tag
def get_template_for_field(field):
    widget_name = field.field.widget.__class__.__name__
    try:
        template_name = WIDGET_TO_TEMPLATE_MAP[widget_name]
    except KeyError:
        template_name = 'form/fields/dummy.html'
    return template_name


@register.simple_tag
def multiply(first, second, seprator=False):
    if first and second:
        return intcomma("%.2f" % (first * second)) if seprator else "%.2f" % (first * second)
