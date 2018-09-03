from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Councilors(models.Model):
    
    uid = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    former_names = models.CharField(max_length=100, blank=True, null=True)
    identifiers = JSONField(null=True)
    data = JSONField(null=True)
    
    def __unicode__(self):
        return self.name

class CouncilorsDetail(models.Model):
    councilor = models.ForeignKey(Councilors, to_field="uid", related_name='each_terms', on_delete=models.PROTECT)
    election_year = models.CharField(db_index=True, max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True, null=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.TextField(db_index=True, blank=True, null=True)
    in_office = models.BooleanField(db_index=True)
    contact_details = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    param = JSONField(null=True)

    class Meta:
        unique_together = ("councilor", "election_year")

    def __unicode__(self):
        return self.name

    def _in_office_year(self):
        return CouncilorsDetail.objects.filter(councilor_id=self.councilor_id).values_list('election_year', flat=True).order_by('-election_year')
    in_office_year = property(_in_office_year)