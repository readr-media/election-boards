import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from councilors.models import CouncilorsDetail
# Create your models here.
class Candidates(models.Model):
    
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    former_names = ArrayField(
        models.CharField(max_length=100),
        null=True,
        default=None,
    )
    identifiers = JSONField(null=True)
    data = JSONField(null=True)
    
    def __unicode__(self):
        return self.name

class Terms(models.Model):
    
    uid = models.CharField(max_length=70, unique=True)
    type = models.CharField(db_index=True, max_length=20)
    candidate = models.ForeignKey(Candidates, to_field='uid', related_name='each_terms', on_delete=models.PROTECT)
    elected_councilor = models.OneToOneField('councilors.Councilorsdetail', blank=True, null=True, related_name='elected_candidate', on_delete=models.PROTECT)
    councilor_terms = JSONField(null=True)
    election_year = models.CharField(db_index=True, max_length=100)
    number = models.IntegerField(db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.TextField(db_index=True, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    votes_percentage = models.CharField(max_length=100, blank=True, null=True)
    votes_detail = JSONField(null=True)
    elected = models.NullBooleanField(db_index=True)
    occupy = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    politicalcontributions = JSONField(null=True)
    data = JSONField(null=True)
    
    class Meta:
        unique_together = ("candidate", "election_year")
        index_together = ['election_year', 'county', 'constituency']
        ordering = ['id']
    def __unicode__(self):
        return self.name