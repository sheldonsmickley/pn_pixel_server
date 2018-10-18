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
    ps_cookie_id = get_random_string(length=32)

    pixel_event_fields = {
        "member_id": request.query_params.get('member_id'),
        "action": request.query_params.get('action'),
        "pn_cookie_id": pn_cookie_id,
        "session_id": request.query_params.get('sess') if request.query_params.get('sess') else 'None',
        "ga_cookie_id": request.query_params.get('ga_cookie') if request.query_params.get('ga_cookie') else 'None',
        "ip_address": request.META['REMOTE_ADDR'],
        "referring_url": request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') else 'None',
        "user_agent": request.META['HTTP_USER_AGENT']
        }

    if request.META.get('HTTP_REFERER') is not None:
        try:
            queryParamsHash_ref = {}
            queryParamsHash_uri = {}
            if "?" in request.META.get('HTTP_REFERER'):
                queryParamsHash_ref = {item.split("=")[0]:item.split("=")[1] for item in request.META['HTTP_REFERER'].split("?")[1].split("&")}

            elif "?" in request.build_absolute_uri():
                queryParamsHash_uri = {item.split("=")[0]:item.split("=")[1] for item in request.build_absolute_uri().split("?")[1].split("&")}

            pixel_event_fields['params'] = {**queryParamsHash_ref, **queryParamsHash_uri}

        except:
            e = sys.exc_info()
            client.captureException()

    try:
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