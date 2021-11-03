import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def initBaseVariables(context):
    request = context['request']
    uproveUser = getattr(request, 'uproveUser', None)

    baseVariables = json.dumps({
        'uproveUser': uproveUser,
        'STATIC_URL': f'{settings.STATIC_URL}'
    })

    return mark_safe(baseVariables)