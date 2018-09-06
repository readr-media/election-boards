# from django.db import models
import uuid

from django.contrib.gis.db import models
from candidates.models import Candidates

# Create your models here.
class Boards(models.Model):
    # 必填 照片連結，座標，上傳者
    address = models.CharField(max_length=150, blank=True)
    image = models.URLField(null=False, blank=False)
    candidates = models.ManyToManyField(Candidates, related_name='board_candidates')
    coordinates = models.PointField(null=False)
    took_at = models.DateTimeField(null=True)
    uploaded_at = models.DateTimeField(null=True, auto_now_add=True)
    uploader = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, blank=False, null=False)
