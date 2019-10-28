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
        blank=True
    )
    identifiers = JSONField(null=True, blank=True)
    data = JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Set uid to uuid ver.4 if it's not set. This is for inline form when using admin"""
        
        if self.uid is None:
            self.uid = uuid.uuid4()

        super(Candidates, self).save(*args, **kwargs)

class Terms(models.Model):
    
    uid = models.CharField(max_length=70, unique=True, editable=False)
    type = models.CharField(db_index=True, max_length=20)
    candidate = models.ForeignKey(Candidates, to_field='uid', related_name='each_terms', on_delete=models.PROTECT)
    elected_councilor = models.OneToOneField('councilors.Councilorsdetail', blank=True, null=True, related_name='elected_candidate', on_delete=models.PROTECT)
    councilor_terms = JSONField(null=True, blank=True)
    election_year = models.CharField(db_index=True, max_length=100)
    number = models.IntegerField(db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.TextField(db_index=True, blank=False, null=True)
    votes = models.IntegerField(blank=True, null=True)
    votes_percentage = models.CharField(max_length=100, blank=True, null=True)
    votes_detail = JSONField(null=True, blank=True)
    elected = models.NullBooleanField(db_index=True)
    occupy = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True, blank=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True, blank=True)
    platform = models.TextField(blank=True, null=True)
    politicalcontributions = JSONField(null=True, blank=True)
    status = models.CharField(db_index=True, default='', max_length=100, blank=True)
    data = JSONField(null=True, blank=True)
    
    class Meta:
        unique_together = ("candidate", "election_year")
        index_together = ['election_year', 'county', 'constituency']
        ordering = ['county','type','id']
    
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Alter uid for Terms manually"""
        self.uid = str(self.candidate.uid) + "-" + self.election_year

        super(Terms, self).save(*args, **kwargs)
