# from django.db import models
import uuid

from django.contrib.gis.db import models
from candidates.models import Terms

# Create your models here.
class Boards(models.Model):
    # 必填 照片連結，座標，上傳者
    image = models.URLField(null=False, blank=False)
    coordinates = models.PointField(null=False)
    
    county = models.CharField(max_length=15, blank=True)
    district = models.CharField(max_length=15, blank=True)
    road = models.CharField(max_length=75, blank=True)
    
    candidates = models.ManyToManyField(Terms, related_name='boards')

    took_at = models.DateTimeField(null=True)
    uploaded_at = models.DateTimeField(null=True, auto_now_add=True)
    uploaded_by = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, blank=False, null=False)

    verified_amount = models.IntegerField(default=0)

    class Meta:
        ordering = ['-uploaded_at']