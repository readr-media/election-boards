# from django.db import models
import uuid

from django.contrib.gis.db import models
from candidates.models import Terms
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Boards(models.Model):

    image = models.CharField(max_length=256, null=False, blank=False)
    coordinates = models.PointField(null=False)

    county = models.CharField(max_length=15, blank=True)
    district = models.CharField(max_length=15, blank=True)
    road = models.CharField(max_length=75, blank=True)

    candidates = models.ManyToManyField(Terms, related_name='boards')

    took_at = models.DateTimeField(null=True)
    uploaded_at = models.DateTimeField(null=True, auto_now_add=True)
    uploaded_by = models.UUIDField(editable=False, blank=False, null=False)

    has_price_info = models.BooleanField(default=False)
    price = models.IntegerField(null=True)
    has_receipt_info = models.BooleanField(default=False)
    receipt = ArrayField(
        models.CharField(max_length=256),
        null=True,
        default=None
    )

    verified_amount = models.IntegerField(default=0)
    is_board = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

class Checks(models.Model):

    board = models.ForeignKey(Boards, related_name='board_checks', on_delete=models.CASCADE)
    candidates = models.ManyToManyField(Terms, related_name='check_candidates')
    slogan = models.CharField(max_length=128, null=True)
    is_board = models.BooleanField(default=False, null=False)
    type = models.IntegerField(null=False, default=0)  # Check type: 1=single check, 2=multiple check

    headcount = models.IntegerField(null=True, default=None)
    is_original = models.BooleanField(null=True, default=False)

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.UUIDField(editable=False, blank=False, null=False)

