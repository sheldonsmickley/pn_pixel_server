from django.db import models
from django_unixdatetimefield import UnixDateTimeField

PIXEL_ACTIONS = (
    ('v','VIEW'),
    ('c','CONVERT'),
)

class PixelEvent(models.Model):
    occurred_at = UnixDateTimeField(auto_now_add=True)
    member_id = models.IntegerField()
    action = models.CharField(choices=PIXEL_ACTIONS, max_length=200)
    pn_cookie_id = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    referring_url = models.CharField(max_length=200, null=True, blank=True, default="None")
    user_agent = models.CharField(max_length=200)