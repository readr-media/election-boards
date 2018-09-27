# from django.db import models
import uuid

from django.contrib.gis.db import models
from candidates.models import Terms

# Create your models here.
class Boards(models.Model):

    image = models.CharField(max_length=256,null=False, blank=False)
    coordinates = models.PointField(null=False)
    
    county = models.CharField(max_length=15, blank=True)
    district = models.CharField(max_length=15, blank=True)
    road = models.CharField(max_length=75, blank=True)
    
    candidates = models.ManyToManyField(Terms, related_name='boards')

    took_at = models.DateTimeField(null=True)
    uploaded_at = models.DateTimeField(null=True, auto_now_add=True)
    uploaded_by = models.UUIDField(editable=False, blank=False, null=False)

    has_price_info = models.BooleanField(default=False)
    has_receipt_inof = models.BooleanField(default=False)

    verified_amount = models.IntegerField(default=0)
    is_board = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

class Checks(models.Model):

    board = models.ForeignKey(Boards, related_name='board_checks', on_delete=models.CASCADE)
    candidates = models.ManyToManyField(Terms, related_name='check_candidates', blank=True)
    slogan = models.CharField(max_length=128, null=True)
    is_board = models.BooleanField(default=False, blank=False)
    created_by = models.UUIDField(editable=False, blank=False, null=False)
