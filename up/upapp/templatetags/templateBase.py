import json

from django import template
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
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

    baseUrl = get_current_site(request).domain
    protocol = 'http://' if settings.DEBUG else 'https://'

    # Lever requires the www. for non-local sites
    leverProtocol = 'http://' if settings.LEVER_DEBUG else 'https://'
    if ('localhost' not in baseUrl) and ('www.' not in baseUrl):
        leverProtocol += 'www.'
    leverRedirectUrl = f'{leverProtocol}{baseUrl}{settings.LEVER_CALLBACK_URL}'

    baseVariables = json.dumps({
        'uproveUser': uproveUser,
        'BASE_URL': protocol + baseUrl,
        'STATIC_URL': static,
        'MEDIA_URL': media,
        'LEVER_REDIRECT_URL': f'{settings.LEVER_REDIRECT_BASE}?client_id={settings.LEVER_CLIENT_ID}&redirect_uri={leverRedirectUrl}&state={settings.LEVER_STATE}&response_type=code&scope={settings.LEVER_SCOPE}&prompt=consent&audience={settings.LEVER_BASE_URL}'
    })

    return mark_safe(baseVariables)