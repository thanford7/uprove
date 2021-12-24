import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def initBaseVariables(context):
    request = context['request']
    try:
        uproveUser = request.session['uproveUser']
    except KeyError:
        uproveUser = None

    media = '/media/'
    if 'http' in (static := settings.STATIC_URL):
        static = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{settings.AWS_LOCATION}/'
        media = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{settings.MEDIA_LOCATION}/'

    baseVariables = json.dumps({
        'uproveUser': uproveUser,
        'STATIC_URL': static,
        'MEDIA_URL': media
    })

    return mark_safe(baseVariables)