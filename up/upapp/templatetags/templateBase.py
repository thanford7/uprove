import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def initBaseVariables(context):
    request = context['request']
    uproveUser = getattr(request, 'uproveUser', None)

    if 'http' in (static := settings.STATIC_URL):
        static = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{settings.STATIC_ROOT}'

    baseVariables = json.dumps({
        'uproveUser': uproveUser,
        'STATIC_URL': static
    })

    return mark_safe(baseVariables)