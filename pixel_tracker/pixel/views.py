from django.shortcuts import render
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from raven.contrib.django.raven_compat.models import client
from rest_framework.decorators import api_view
from pixel.models import PixelEvent

import base64
import sys

@api_view(['GET'])
def pixel(request):
    pn_cookie_key = "pn"
    pn_cookie_id = request.COOKIES.get(pn_cookie_key) or get_random_string(length=32)

    pixel_event_fields = {
        "member_id": request.query_params.get('member_id'),
        "action": request.query_params.get('action'),
        "pn_cookie_id": pn_cookie_id,
        "ip_address": request.META['REMOTE_ADDR'],
        "url": request.META['HTTP_HOST'],
        "referring_url": request.META.get('HTTP_REFERER'),
        "user_agent": request.META['HTTP_USER_AGENT'], 
    }

    try:
        import pdb; pdb.set_trace();
        pixel_event = PixelEvent(**pixel_event_fields)
        pixel_event.save()
    except:
        e = sys.exc_info()
        client.captureException()

    PIXEL_PNG_DATA = base64.b64decode(
        b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    response = HttpResponse(PIXEL_PNG_DATA, content_type='image/png')
    response.set_cookie(pn_cookie_key, pn_cookie_id)

    return response